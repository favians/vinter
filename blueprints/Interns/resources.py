import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from .model import Interns
from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

#password Encription
from password_strength import PasswordPolicy

# 'interns' penamaan (boleh diganti)
bp_interns = Blueprint('interns', __name__)
api = Api(bp_interns)

class InternResource(Resource):

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        qry = Interns.query.get(args["id"])
        if qry is not None:
            return {"status":"success", "result":marshal(qry, Interns.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}

    def post(self):
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('image', location='json')
        parser.add_argument('address', location='json')
        args = parser.parse_args()

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()

            intern = Interns(datetime.datetime.now(), args['username'], password_digest, args['image'], args['address'], True, 'intern')
            
            try:
                db.session.add(intern)
                db.session.commit()
            except Exception as e:
                return {"status":"failed", "result": "intern already exist"}, 400, {'Content-Type':'application/json'}

            app.logger.debug('DEBUG : %s ', intern )

            return {"status":"success", "result":marshal(intern, Interns.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {"status":"failed", "result": "Wrong Password Length"}, 400, {'Content-Type':'application/json'}
    
    @jwt_required
    @intern_only
    def put(self):
        claims = get_jwt_claims()

        qry = Interns.query.get(claims["id"])

        if qry is None:
            return {'status':'failed',"result":"id not found"}, 404, {'Content-Type':'application/json'}

        defaultdata = marshal(qry, Interns.response_field)

        parser = reqparse.RequestParser()
        parser.add_argument('image', location='json', default=defaultdata["image"])
        parser.add_argument('address', location='json', default=defaultdata["address"])
        args = parser.parse_args()

            
        qry.image = args["image"]
        qry.address = args["address"]
        db.session.commit()

        return {"status":"success", "result":marshal(qry, Interns.response_field)}, 200, {'Content-Type':'application/json'}

class InternList(Resource):

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

        qry = Interns.query

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row,Interns.response_field))
        
        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}



api.add_resource(InternResource, '', '')
api.add_resource(InternList,'','/list')