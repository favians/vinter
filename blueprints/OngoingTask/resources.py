import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from blueprints.Company.model import Company

from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

#import all blueprints
from .model import OngoingPosition
from blueprints.Company.model import Company
from blueprints.Position.model import Position
from blueprints.Intern.model import Intern
from blueprints.Task.model import Task

# 'ongoing_task' penamaan (boleh diganti)
bp_ongoing_task = Blueprint('ongoing_task', __name__)
api = Api(bp_ongoing_task)

class OngoingTaskResource(Resource):

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        ongoingTaskQry = OngoingTask.query.get(args["id"])

        if ongoingTaskQry is None:
            return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}

        result = marshal(ongoingTaskQry, OngoingTask.response_field)

        qry = db.session.query(OngoingTask, Intern, Company, Position)
        qry = qry.join(Intern, OngoingTask.task_id == Task.id)
        qry = qry.join(Company, OngoingTask.company_id == Company.id)
        qry = qry.join(Position, OngoingTask.position_id == Position.id).first()

        result["intern_name"] = qry[1].name
        result["intern_images"] = qry[1].images
        result["intern_address"] = qry[1].address
        result["company_name"] = qry[2].name
        result["company_address"] = qry[2].address
        result["position_name"] = qry[3].name
        result["position_description"] = qry[3].description
        result["position_certificate_trigger_score"] = qry[3].certificate_trigger_score

        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

api.add_resource(OngoingTaskResource, '', '')
