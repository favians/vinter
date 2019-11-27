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

    def options(self):
        return {},200

    @jwt_required
    @intern_only
    def get(self):
        claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('intern_id', location='args', type=int, required=True)
        args = parser.parse_args()
        
        ongoingPositionQry = OngoingPosition.query.filter_by(intern_id = args["intern_id"]).all()
        
        if ongoingPositionQry is None:
            return {'status':'failed', "result" : "intern_id not found"}, 404, {'Content-Type':'application/json'}

        result = []
        for onPosValue in ongoingPositionQry:
            onpos = marshal(onPosValue, OngoingPosition.response_field)

            findPos = self.findPosition(onpos)
            findComp = self.findCompany(onpos)

            ongoingTaskQry = OngoingTask.query.filter_by(ongoing_position_id=onpos["id"]).all()
            ongoingTask = marshal(ongoingTaskQry, OngoingTask.response_field)
            
            onpos['position_name'] = findPos['name']
            onpos['position_image'] = findPos['image']
            onpos['company_name'] = findComp['name']
            onpos['ongoing_task'] = ongoingTask

            result.append(onpos)

        return {"status":"success", "result":result}, 200, {"Content-Type":"application/json"}

    def findPosition(self,onpos):
        qry = Position.query.get(onpos['position_id'])
        return marshal(qry, Position.response_field)

    def findCompany(self,onpos):
        qry = Company.query.get(onpos['company_id'])
        return marshal(qry, Position.response_field)


api.add_resource(OnGoingPositionTaskResource, '', '')
