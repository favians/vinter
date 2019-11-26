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

# 'on_going_pos_task' penamaan (boleh diganti)
bp_on_going_pos_task = Blueprint('on_going_pos_task', __name__)
api = Api(bp_on_going_pos_task)

class OnGoingPositionTaskResource(Resource):

    @jwt_required
    @intern_only
    def get(self):
        claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('intern_id', location='json', type=int, required=True)
        args = parser.parse_args()
        
        ongoingPositionQry = OngoingPosition.query.filter_by(intern_id = args["intern_id"]).all()
        
        if ongoingPositionQry is None:
            return {'status':'failed', "result" : "position_id not found"}, 404, {'Content-Type':'application/json'}

        result = []
        for onPosValue in ongoingPositionQry:
            onpos = marshal(onPosValue, OngoingPosition.response_field)

            ongoingTaskQry = OngoingTask.query.filter_by(position_id=onpos["position_id"]).filter_by(intern_id=claims["id"]).all()
            ongoingTask = marshal(ongoingTaskQry, OngoingTask.response_field)

            onpos['ongoing_task'] = ongoingTask

            result.append(onpos)

        return {"status":"success", "result":result}, 200, {"Content-Type":"application/json"}

api.add_resource(OnGoingPositionTaskResource, '', '')
