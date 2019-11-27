import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc
from .validator import Validation

from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

#import all blueprints
from blueprints.Company.model import Company
from blueprints.Position.model import Position
from blueprints.Intern.model import Intern
from blueprints.Task.model import Task
from blueprints.OngoingTask.model import OngoingTask
from blueprints.OngoingPosition.model import OngoingPosition

# 'choose_position' penamaan (boleh diganti)
bp_choose_position = Blueprint('choose_position', __name__)
api = Api(bp_choose_position)

class ChoosePositionResource(Resource):

    def options(self):
        return {},200

    @jwt_required
    @intern_only
    def post(self):
        claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('position_id', location='json', type=int, required=True)
        args = parser.parse_args()
        
        posQry = Position.query.get(args["position_id"])
        
        if posQry is None:
            return {'status':'failed', "result" : "position_id not found"}, 404, {'Content-Type':'application/json'}

        position = marshal(posQry, Position.response_field)

        if not Validation.ValidateOnGoingPositionExistence(self, args['position_id'], claims['id']):
            return {'status':'failed', "result":"already exist"}, 404, {'Content-Type':'application/json'}

        taskQry = Task.query.filter_by(position_id=args["position_id"]).all()
        task = marshal(taskQry, Task.response_field)
    
        qry = OngoingPosition(claims["id"], position["company_id"], args["position_id"], datetime.datetime.now(), False, 0, len(taskQry), 0, 0)

        db.session.add(qry)
        db.session.commit()

        self.InsertToOngoingTask(task, claims['id'], position["company_id"], args["position_id"])

        app.logger.debug("DEBUG : %s ", qry)

        return {"status":"success", "result":marshal(qry, OngoingPosition.response_field)}, 200, {"Content-Type":"application/json"}

    def InsertToOngoingTask(self, task, internID, companyID, positionID):
        for TaskValue in task:
            qry = OngoingTask(TaskValue["id"], internID, companyID, positionID, datetime.datetime.now(), False, "", False, 0)

            db.session.add(qry)
            db.session.commit()


api.add_resource(ChoosePositionResource, '', '')
