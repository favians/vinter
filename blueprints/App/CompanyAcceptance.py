import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

#import all blueprints
from blueprints.Company.model import Company
from blueprints.Position.model import Position
from blueprints.Intern.model import Intern
from blueprints.Task.model import Task
from blueprints.OngoingTask.model import OngoingTask
from blueprints.OngoingPosition.model import OngoingPosition

# 'company_accept' penamaan (boleh diganti)
bp_company_accept = Blueprint('company_accept', __name__)
api = Api(bp_company_accept)

class CompanyAcceptanceResource(Resource):
    
    def options(self):
        return {},200

    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('ongoing_task_id', location='json', type=int, required=True)
        parser.add_argument('score', location='json', type=int, required=True)
        args = parser.parse_args()
        
        ongoingTaskQry = OngoingTask.query.get(args['ongoing_task_id'])
        
        if ongoingTaskQry is None:
            return {'status':'failed', "result" : "ongoing_task_id not found"}, 404, {'Content-Type':'application/json'}
        
        ongoingTValue = marshal(ongoingTaskQry, OngoingTask.response_field)
        ongoingTaskQry.approve = True
        ongoingTaskQry.score = args["score"]

        db.session.commit()

        ongoingPosQry = OngoingPosition.query.filter_by(intern_id = ongoingTValue["intern_id"]).filter_by(position_id = ongoingTValue["position_id"]).first()
        ongoingPosValue = marshal(ongoingPosQry, OngoingPosition.response_field)

        self.Certificate(ongoingPosValue, ongoingTValue)

        return {"status":"success", "result": ongoingTValue}, 200, {"Content-Type":"application/json"}

    def Certificate(self, OnPos, OnTask):
        return True


api.add_resource(CompanyAcceptanceResource, '', '')