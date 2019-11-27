from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
import json, hashlib
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.Intern.model import Intern
from blueprints.Company.model import Company

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateInternTokenResource(Resource):
    
    def options(self):
        return {},200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()

        ###### from database ########
        qry = Intern.query

        qry = qry.filter_by(email = args['email'])
        qry = qry.filter_by(password = password).first()
         

        claim = marshal(qry, Intern.response_field)

        if qry is not None:
            token = create_access_token(identity=args['email'], user_claims=claim)
        else:
            return {'status':'failed', 'result': 'UNAUTHORIZED | invalid key or secret'}, 401

        return {"status":"success",'result': token}, 200, {'Content-Type':'application/json'}

class CreateCompanyTokenResource(Resource):

    def options(self):
        return {},200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()

        ###### from database ########
        qry = Company.query

        qry = qry.filter_by(email = args['email'])
        qry = qry.filter_by(password = password).first()
         

        claim = marshal(qry, Company.response_field)

        if qry is not None:
            token = create_access_token(identity=args['email'], user_claims=claim)
        else:
            return {'status':'failed', 'result': 'UNAUTHORIZED | invalid key or secret'}, 401

        return {"status":"success",'result': token}, 200, {'Content-Type':'application/json'}

class CheckSelf(Resource):

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return {"status":"success", 'result': claims}, 200, {'Content-Type':'application/json'}

api.add_resource(CreateInternTokenResource,'/intern')
api.add_resource(CreateCompanyTokenResource,'/company')
api.add_resource(CheckSelf,'')
