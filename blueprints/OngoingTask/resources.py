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
from blueprints.OngoingPosition.model import OngoingPosition

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

        qry = db.session.query(OngoingTask, Intern, Company, Position, Task, OngoingPosition).filter(OngoingTask.id == args["id"])
        qry = qry.join(Intern, OngoingTask.intern_id == Intern.id)
        qry = qry.join(Company, OngoingTask.company_id == Company.id)
        qry = qry.join(Position, OngoingTask.position_id == Position.id)
        qry = qry.join(Task, OngoingTask.task_id == Task.id)
        qry = qry.join(OngoingPosition, OngoingTask.ongoing_position_id == OngoingPosition.id).first()

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
        result["ongoing_position_id"] = qry[5].id

        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

class OngoingTaskList(Resource):

    def options(self):
        return {},200

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('intern_id', location='args',type=int)
        parser.add_argument('company_id', location='args',type=int)
        parser.add_argument('position_id', location='args',type=int)
        parser.add_argument('ongoing_position_id', location='args',type=int)
        parser.add_argument('active',location='args', type=inputs.boolean, help='invalid active', choices=(True,False))
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = OngoingTask.query

        if args['intern_id'] is not None:
            qry = qry.filter_by(intern_id=args['intern_id'])

        if args['company_id'] is not None:
            qry = qry.filter_by(company_id=args['company_id'])

        if args['position_id'] is not None:
            qry = qry.filter_by(position_id=args['position_id'])

        if args['ongoing_position_id'] is not None:
            qry = qry.filter_by(ongoing_position_id=args['ongoing_position_id'])

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            OngoingValue = marshal(row, OngoingTask.response_field)

            qryIntern = Intern.query.get(OngoingValue["intern_id"])
            qryCompany = Company.query.get(OngoingValue["company_id"])
            qryPosition = Position.query.get(OngoingValue["position_id"])
            qryOnGoPosition = OngoingPosition.query.get(OngoingValue["ongoing_position_id"])

            MarshalqryIntern = marshal(qryIntern, Intern.response_field)
            MarshalqryCompany = marshal(qryCompany, Company.response_field)
            MarshalqryPosition = marshal(qryPosition, Position.response_field)
            MarshalqryOnGoPosition = marshal(qryOnGoPosition, OngoingPosition.response_field)

            OngoingValue["intern"] = MarshalqryIntern
            OngoingValue["company"] = MarshalqryCompany
            OngoingValue["position"] = MarshalqryPosition
            OngoingValue["ongoing_position"] = MarshalqryOnGoPosition

            result.append(OngoingValue)
        
        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

api.add_resource(OngoingTaskResource, '', '')
api.add_resource(OngoingTaskList, '', '/list')
