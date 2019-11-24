import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from .model import Task
from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

#password Encription
from password_strength import PasswordPolicy

# 'task' penamaan (boleh diganti)
bp_task = Blueprint('task', __name__)
api = Api(bp_task)

class TaskResource(Resource):

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        qry = Task.query.get(args["id"])
        if qry is not None:
            return {"status":"success", "result":marshal(qry, Task.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', location='json', type=list, required=True)
        args = parser.parse_args()

        parser = reqparse.RequestParser()
        parser["data"].add_argument('hello', location='json', required=True)
        args = parser.parse_args()

        result = []
        for iterate, value in enumerate(args["data"]):
            print (iterate)
            print (value)


        return args["data"]
        task = Task(datetime.datetime.now(), args['name'], args['username'], password_digest, args['image'], args['address'], True, 'intern')
            
        db.session.add(task)
        db.session.commit()

        app.logger.debug('DEBUG : %s ', task )

        return {"status":"success", "result":marshal(task, Task.response_field)}, 200, {'Content-Type':'application/json'}
    
    @jwt_required
    @company_only
    def put(self):
        claims = get_jwt_claims()

        qry = Task.query.get(claims["id"])

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
        parser.add_argument('active',location='args', type=inputs.boolean, help='invalid active', choices=(True,False))
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Task.query

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row,Task.response_field))
        
        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}



api.add_resource(TaskResource, '', '')
api.add_resource(TaskListWithCompany,'','/list')