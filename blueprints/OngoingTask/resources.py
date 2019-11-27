import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from blueprints.Company.model import Company

from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

#import all blueprints
from .model import OngoingTask
from blueprints.Company.model import Company
from blueprints.Position.model import Position
from blueprints.Intern.model import Intern
from blueprints.Task.model import Task

# 'ongoing_task' penamaan (boleh diganti)
bp_ongoing_task = Blueprint('ongoing_task', __name__)
api = Api(bp_ongoing_task)

class OngoingTaskResource(Resource):

    def options(self):
        return {},200

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        ongoingTaskQry = OngoingTask.query.get(args["id"])

        if ongoingTaskQry is None:
            return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}

        result = marshal(ongoingTaskQry, OngoingTask.response_field)

        qry = db.session.query(OngoingTask, Intern, Company, Position, Task).filter(OngoingTask.id == args["id"])
        qry = qry.join(Intern, OngoingTask.intern_id == Intern.id)
        qry = qry.join(Company, OngoingTask.company_id == Company.id)
        qry = qry.join(Position, OngoingTask.position_id == Position.id)
        qry = qry.join(Task, OngoingTask.task_id == Task.id).first()

        result["intern_email"] = qry[1].email
        result["intern_name"] = qry[1].name
        result["intern_image"] = qry[1].image
        result["intern_address"] = qry[1].address
        result["intern_pendidikan"] = qry[1].pendidikan
        result["intern_deskripsi"] = qry[1].deskripsi
        result["company_name"] = qry[2].name
        result["company_address"] = qry[2].address
        result["position_name"] = qry[3].name
        result["position_description"] = qry[3].description
        result["position_certificate_trigger_score"] = qry[3].certificate_trigger_score
        result["task_name"] = qry[4].name
        result["task_description"] = qry[4].description
        result["task_active"] = qry[4].active
        result["task_order"] = qry[4].order

        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

api.add_resource(OngoingTaskResource, '', '')
