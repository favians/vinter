import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from .model import Certificate
from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

from blueprints.Company.model import Company
from blueprints.Position.model import Position
from blueprints.Intern.model import Intern

# 'certificate' penamaan (boleh diganti)
bp_certificate = Blueprint('certificate', __name__)
api = Api(bp_certificate)

class CertificateResource(Resource):

    def options(self):
        return {},200

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        certificateQry = Certificate.query.get(args["id"])

        if certificateQry is None:
            return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}

        result = marshal(certificateQry, Certificate.response_field)

        qry = db.session.query(Certificate, Position, Intern, Company).filter(Certificate.id == args["id"])
        qry = qry.join(Position, Certificate.position_id == Position.id)
        qry = qry.join(Intern, Certificate.intern_id == Intern.id)
        qry = qry.join(Company, Certificate.company_id == Company.id).first()

        result["position_name"] = qry[1].name
        result["position_description"] = qry[1].description
        result["position_certificate_trigger_score"] = qry[1].certificate_trigger_score
        result["intern_email"] = qry[2].email
        result["intern_name"] = qry[2].name
        result["intern_image"] = qry[2].image
        result["intern_address"] = qry[2].address
        result["intern_pendidikan"] = qry[2].pendidikan
        result["intern_deskripsi"] = qry[2].deskripsi
        result["company_name"] = qry[3].name
        result["company_address"] = qry[3].address

        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}


class CertificateList(Resource):

    def options(self):
        return {},200

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('company_id', location='args', type=int)
        parser.add_argument('position_id', location='args', type=int)
        parser.add_argument('intern_id', location='args', type=int)
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Certificate.query

        if args['company_id'] is not None:
            qry = qry.filter_by(company_id=args['company_id'])

        if args['position_id'] is not None:
            qry = qry.filter_by(position_id=args['position_id'])

        if args['intern_id'] is not None:
            qry = qry.filter_by(intern_id=args['intern_id'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row, Certificate.response_field))
        
        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

class CertificateListFull(Resource):

    def options(self):
        return {},200

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
        parser.add_argument('intern_id', location='args', type=int)
        parser.add_argument('active', location='json', type=inputs.boolean, help='invalid active', choices=(True,False))
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Certificate.query

        if args['company_id'] is not None:
            qry = qry.filter_by(company_id=args['company_id'])

        if args['position_id'] is not None:
            qry = qry.filter_by(position_id=args['position_id'])

        if args['intern_id'] is not None:
            qry = qry.filter_by(intern_id=args['intern_id'])

        if args['active'] is not None:
            qry = qry.filter_by(active=args['active'])

        result = []
        for data in qry.limit(args['rp']).offset(offset).all():
            holder = marshal(data, Certificate.response_field)
            
            companyQry = Company.query.get(holder['company_id'])
            positionQry = Position.query.get(holder['position_id'])
            internQry = Intern.query.get(holder['intern_id'])

            companyQryMarshal = marshal(companyQry, Company.response_field)
            positionQryMarshal = marshal(positionQry, Position.response_field)
            internQryMarshal = marshal(internQry, Intern.response_field)

            holder["company"] = companyQryMarshal
            holder["position"] = positionQryMarshal
            holder["intern"] = internQryMarshal

            result.append(holder)

        results = {}
        results["page"] = args["p"]
        results["total_page"] = len(result) // args["rp"] +1
        results["per_page"] = args["rp"]
        results["data"] = result

        return {"status":"success", "result":results}, 200, {'Content-Type':'application/json'}

api.add_resource(CertificateResource, '', '')
api.add_resource(CertificateList,'','/list')
api.add_resource(CertificateListFull,'','/list/full')
