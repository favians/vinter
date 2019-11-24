import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from .model import Task
from .validator import Validation
from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

from blueprints.Company.model import Company
from blueprints.Position.model import Position


# 'task' penamaan (boleh diganti)
bp_task = Blueprint('task', __name__)
api = Api(bp_task)

class TaskResource(Resource):

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        taskQry = Task.query.get(args["id"])

        if taskQry is None:
            return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}

        result = marshal(taskQry, Task.response_field)

        qry = db.session.query(Task, Company, Position).join(Company, Task.company_id == Company.id)
        qry = qry.join(Position, Task.position_id == Position.id).first()

        result["company_name"] = qry[1].name
        result["company_address"] = qry[1].address
        result["position_name"] = qry[2].name
        result["position_description"] = qry[2].description
        result["position_certificate_trigger_score"] = qry[2].certificate_trigger_score

        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

    @jwt_required
    @company_only
    def post(self):
        claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('task_data', location='json', type=list, required=True)
        parser.add_argument('position_id', location='json', type=int, required=True)
        args = parser.parse_args()

        if not Validation.ValidatePositionOwnership(self, args['position_id'], claims['id']):
            return {'status':'failed', "result":"not yours"}, 404, {'Content-Type':'application/json'}

        if not Validation.ValidateExistence(self, args['position_id'], claims['id']):
            return {'status':'failed', "result":"already Exist"}, 404, {'Content-Type':'application/json'}

        for iterate, value in enumerate(args["task_data"]):

            task = Task(claims['id'], args['position_id'], datetime.datetime.now(), value['name'], value['description'], value["active"], iterate+1)

            db.session.add(task)
            db.session.commit()

            app.logger.debug('DEBUG : %s ', task )

        return {"status":"success", "result":args['task_data']}, 200, {'Content-Type':'application/json'}

    @jwt_required
    @company_only
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id",location="args", help="invalid id", required=True)
        args = parser.parse_args()

        qry = Task.query.get(args["id"])

        if qry is None:
            return {'status':'failed',"result":"id not found"}, 404, {'Content-Type':'application/json'}

        defaultdata = marshal(qry, Task.response_field)

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', default=defaultdata["name"])
        parser.add_argument('description', location='json', default=defaultdata["description"])
        parser.add_argument('active', type=inputs.boolean, location='json', default=defaultdata["active"])
        args = parser.parse_args()

        qry.name = args["name"]
        qry.description = args["description"]
        qry.active = args["active"]
        db.session.commit()

        return {"status":"success", "result":marshal(qry, Task.response_field)}, 200, {'Content-Type':'application/json'}

class TaskListWithCompany(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('company_id', location='args', type=int)
        parser.add_argument('position_id', location='args', type=int)
        parser.add_argument('active',location='args', type=inputs.boolean, help='invalid active', choices=(True,False))
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Task.query

        if args['company_id'] is not None:
            qry = qry.filter_by(company_id=args['company_id'])

        if args['position_id'] is not None:
            qry = qry.filter_by(position_id=args['position_id'])

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row,Task.response_field))
        
        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

class TaskListFull(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('company_id', location='args', type=int)
        parser.add_argument('position_id', location='args', type=int)
        parser.add_argument('active',location='args', type=inputs.boolean, help='invalid active', choices=(True,False))
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = db.session.query(Task, Position, Company).join(Position, Position.company_id == Company.id)
        qry = qry.join(Task, Task.position_id == Position.id)

        if args['company_id'] is not None:
            qry = qry.filter_by(company_id=args['company_id'])

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        if args['position_id'] is not None:
            qry = qry.filter_by(position_id=args['position_id'])

        result = []
        for data in qry.limit(args['rp']).offset(offset).all():
            holder = marshal(data[0], Task.response_field)
            holder["company_name"] = data[2].name
            holder["company_address"] = data[2].address
            holder["position_name"] = data[1].name
            holder["position_description"] = data[1].description
            holder["position_certificate_trigger_score"] = data[1].certificate_trigger_score
            result.append(holder)

        results = {}
        results["page"] = args["p"]
        results["total_page"] = len(result) // args["rp"] +1
        results["per_page"] = args["rp"]
        results["data"] = result

        return {"status":"success", "result":results}, 200, {'Content-Type':'application/json'}

api.add_resource(TaskResource, '', '')
api.add_resource(TaskListWithCompany,'','/list')
api.add_resource(TaskListFull,'','/list/full')


#single data type
    # @jwt_required
    # @company_only
    # def post(self):
    #     claims = get_jwt_claims()

    #     parser = reqparse.RequestParser()
    #     parser.add_argument('position_id', location='json', type=int, required=True)
    #     parser.add_argument('name', location='json', required=True)
    #     parser.add_argument('description', location='json', required=True)
    #     parser.add_argument('active', location='json', type=inputs.boolean, help='invalid active', choices=(True,False))
    #     args = parser.parse_args()


    #     qry = Task(claims['id'], args['position_id'], datetime.datetime.now(), args['name'], args['description'], args["active"])

    #     db.session.add(qry)
    #     db.session.commit()

    #     app.logger.debug('DEBUG : %s ', qry )

    #     return {"status":"success", "result":marshal(qry, Task.response_field)}, 200, {'Content-Type':'application/json'}

#request form

# {
# 	"position_id":4,
# 	"name": "Pembuatan design pattern dan koding 22",
# 	"description": "tolong buatkan koding untuk golangg 22",
# 	"active": true
# }
