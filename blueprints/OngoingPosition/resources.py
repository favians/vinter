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

# 'ongoing_position' penamaan (boleh diganti)
bp_ongoing_position = Blueprint('ongoing_position', __name__)
api = Api(bp_ongoing_position)

class OngoingPositionResource(Resource):

    def options(self):
        return {},200

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        ongoingPositionQry = OngoingPosition.query.get(args["id"])

        if ongoingPositionQry is None:
            return {'status':'failed', "result" : "id not found"}, 404, {'Content-Type':'application/json'}

        result = marshal(ongoingPositionQry, OngoingPosition.response_field)

        qry = db.session.query(OngoingPosition, Company, Position).filter(OngoingPosition.id == args["id"])
        qry = qry.join(Company, OngoingPosition.company_id == Company.id)
        qry = qry.join(Position, OngoingPosition.position_id == Position.id).first()
        result["company_name"] = qry[1].name
        result["company_address"] = qry[1].address
        result["position_name"] = qry[2].name
        result["position_description"] = qry[2].description
        result["position_certificate_trigger_score"] = qry[2].certificate_trigger_score

        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

api.add_resource(OngoingPositionResource, '', '')
