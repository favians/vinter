import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from .model import Company
from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints.Position.model import Position

#password Encription
from password_strength import PasswordPolicy

# 'company' penamaan (boleh diganti)
bp_company = Blueprint('company', __name__)
api = Api(bp_company)

class CompanyResource(Resource):

    def options(self):
        return {},200

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        qry = Company.query.get(args["id"])
        if qry is not None:
            return {"status":"success", "result":marshal(qry, Company.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}

    def post(self):
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('image', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('description', location='json')
        parser.add_argument('industry', location='json')
        parser.add_argument('location', location='json')

        args = parser.parse_args()

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()

            company = Company(datetime.datetime.now(), args['name'], args['email'], password_digest, args['image'], args['address'], True, 'company',args['description'],args['industry'],args['location'])
            
            try:
                db.session.add(company)
                db.session.commit()
            except Exception as e:
                return {"status":"failed", "result": "company already exist"}, 400, {'Content-Type':'application/json'}

            app.logger.debug('DEBUG : %s ', company )

            return {"status":"success", "result":marshal(company, Company.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {"status":"failed", "result": "Wrong Password Length"}, 400, {'Content-Type':'application/json'}
    
    @jwt_required
    @company_only
    def put(self):
        claims = get_jwt_claims()

        qry = Company.query.get(claims["id"])

        if qry is None:
            return {'status':'failed',"result":"id not found"}, 404, {'Content-Type':'application/json'}

        defaultdata = marshal(qry, Company.response_field)

        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', default=defaultdata["name"])
        parser.add_argument('image', location='json', default=defaultdata["image"])
        parser.add_argument('address', location='json', default=defaultdata["address"])
        parser.add_argument('description', location='json', default=defaultdata["description"])
        parser.add_argument('industry', location='json', default=defaultdata["industry"])
        parser.add_argument('location', location='json', default=defaultdata["location"])
        args = parser.parse_args()

        qry.name = args["name"]
        qry.image = args["image"]
        qry.address = args["address"]
        qry.description = args["description"]
        qry.industry = args["industry"]
        qry.location = args["location"]

        db.session.commit()

        return {"status":"success", "result":marshal(qry, Company.response_field)}, 200, {'Content-Type':'application/json'}

class CompanyList(Resource):

    def options(self):
        return {},200

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

        qry = Company.query

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            marComp = marshal(row, Company.response_field)
            posQry = Position.query.filter_by(company_id=marComp['id']).all()
            marComp["oportunity"] = len(posQry)

            result.append(marComp)
        
        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}



api.add_resource(CompanyResource, '', '')
api.add_resource(CompanyList,'','/list')