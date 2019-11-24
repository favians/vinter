import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from .model import Position
from blueprints.Company.model import Company

from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

# 'position' penamaan (boleh diganti)
bp_position = Blueprint('position', __name__)
api = Api(bp_position)

class PositionResource(Resource):

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        positionQry = Position.query.get(args["id"])

        if positionQry is None:
            return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}

        result = marshal(positionQry, Position.response_field)
        qry = db.session.query(Position, Company).join(Position, Position.company_id == Company.id).first()
        result["company_name"] = qry[1].name
        result["company_address"] = qry[1].address

        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

    @jwt_required
    @company_only
    def post(self):
        claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('description', location='json')
        parser.add_argument('active', location='json', type=inputs.boolean, help='invalid active', choices=(True,False))
        parser.add_argument('certificate_trigger_score', location='json', type=int, required=True)
        args = parser.parse_args()

        qry = Position(claims["id"], datetime.datetime.now(), args["name"], args["description"], args["active"] , args["certificate_trigger_score"])

        db.session.add(qry)
        db.session.commit()

        app.logger.debug("DEBUG : %s ", qry)

        return {"status":"success", "result":marshal(qry, Position.response_field)}, 200, {"Content-Type":"application/json"}

    
    @jwt_required
    @company_only
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id",location="args", help="invalid id", required=True)
        args = parser.parse_args()

        qry = Position.query.get(args["id"])

        if qry is None:
            return {'status':'failed',"result":"id not found"}, 404, {'Content-Type':'application/json'}

        defaultdata = marshal(qry, Position.response_field)

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', default=defaultdata["name"])
        parser.add_argument('description', location='json', default=defaultdata["description"])
        parser.add_argument('active', location='json', type=inputs.boolean, help='invalid active', choices=(True,False))
        parser.add_argument('certificate_trigger_score', location='json', type=int, default=defaultdata["certificate_trigger_score"])
        args = parser.parse_args()

        qry.name = args["name"]
        qry.description = args["description"]
        qry.active = args["active"]
        qry.certificate_trigger_score = args["certificate_trigger_score"]
        db.session.commit()

        return {"status":"success", "result":marshal(qry, Position.response_field)}, 200, {'Content-Type':'application/json'}

class PositionList(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('company_id', location='args')
        parser.add_argument('active',location='args', type=inputs.boolean, help='invalid active', choices=(True,False))
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Position.query

        if args['company_id'] is not None:
            qry = qry.filter_by(company_id=args['company_id'])

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row, Position.response_field))

        results = {}
        results["page"] = args["p"]
        results["total_page"] = len(result) // args["rp"] +1
        results["per_page"] = args["rp"]
        results["data"] = result

        return {"status":"success", "result":results}, 200, {'Content-Type':'application/json'}

class PositionListFull(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('company_id', location='args')
        parser.add_argument('active',location='args', type=inputs.boolean, help='invalid active', choices=(True,False))
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = db.session.query(Position, Company).join(Position, Position.company_id == Company.id)

        if args['company_id'] is not None:
            qry = qry.filter_by(company_id=args['company_id'])

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        result = []
        for data in qry.limit(args['rp']).offset(offset).all():
            holder = marshal(data[0], Position.response_field)
            holder["company_name"] = data[1].name
            holder["company_address"] = data[1].address
            result.append(holder)

        results = {}
        results["page"] = args["p"]
        results["total_page"] = len(result) // args["rp"] +1
        results["per_page"] = args["rp"]
        results["data"] = result

        return {"status":"success", "result":results}, 200, {'Content-Type':'application/json'}


api.add_resource(PositionResource, '', '')
api.add_resource(PositionList,'','/list')
api.add_resource(PositionListFull,'','/listfull')