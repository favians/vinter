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

# 'done_task' penamaan (boleh diganti)
bp_done_task = Blueprint('done_task', __name__)
api = Api(bp_done_task)

class ProcessDoneResource(Resource):

    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('ongoing_task_id', location='json', type=int, required=True)
        parser.add_argument('attachment', location='json')
        args = parser.parse_args()
        
        ongoingTaskQry = OngoingTask.query.get(args['ongoing_task_id'])
        
        if ongoingTaskQry is None:
            return {'status':'failed', "result" : "ongoing_task_id not found"}, 404, {'Content-Type':'application/json'}

        ongoingTaskQry.done = True
        ongoingTaskQry.attachment = args["attachment"]

        db.session.commit()

        return {"status":"success", "result":marshal(ongoingTaskQry, OngoingTask.response_field)}, 200, {"Content-Type":"application/json"}

api.add_resource(ProcessDoneResource, '', '')