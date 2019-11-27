import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import db, app
from sqlalchemy import desc

from blueprints import intern_only, company_only
from flask_jwt_extended import jwt_required, get_jwt_claims

#import all blueprints
from blueprints.Company.model import Company
from blueprints.Certificate.model import Certificate
from blueprints.Position.model import Position
from blueprints.Intern.model import Intern
from blueprints.Task.model import Task
from blueprints.OngoingTask.model import OngoingTask
from blueprints.OngoingPosition.model import OngoingPosition

# 'company_accept' penamaan (boleh diganti)
bp_company_accept = Blueprint('company_accept', __name__)
api = Api(bp_company_accept)

class CompanyAcceptanceResource(Resource):
    
    def options(self):
        return {},200

    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('ongoing_task_id', location='json', type=int, required=True)
        parser.add_argument('score', location='json', type=int, required=True)
        args = parser.parse_args()
        
        ongoingTaskQry = OngoingTask.query.get(args['ongoing_task_id'])
        
        if ongoingTaskQry is None:
            return {'status':'failed', "result" : "ongoing_task_id not found"}, 404, {'Content-Type':'application/json'}
        
        ongoingTValue = marshal(ongoingTaskQry, OngoingTask.response_field)

        if ongoingTValue["approve"] == True:
            return {'status':'failed', "result" : "already accepted"}, 404, {'Content-Type':'application/json'}

        ongoingTaskQry.approve = True
        ongoingTaskQry.score = args["score"]

        db.session.commit()

        ongoingPosQry = OngoingPosition.query.get(ongoingTValue["ongoing_position_id"])
        ongoingPosValue = marshal(ongoingPosQry, OngoingPosition.response_field)

        ongoingPosQry.completed_task = ongoingPosValue["completed_task"]+1
        ongoingPosQry.total_score = ongoingPosValue["total_score"]+args["score"]
        ongoingPosQry.average_score = (((ongoingPosValue["average_score"]*(ongoingPosValue["completed_task"]+1))+args["score"]) / (ongoingPosValue["total_task"]))

        db.session.commit()

        ongoingPosValue = marshal(ongoingPosQry, OngoingPosition.response_field)

        self.AfterCompanyAccept(ongoingPosValue, ongoingPosQry, ongoingTValue)

        return {"status":"success", "result": ongoingPosValue}, 200, {"Content-Type":"application/json"}

    def AfterCompanyAccept(self, ongoingPosValue, ongoingPosQry, ongoingTaskValue):
        if ongoingPosValue["completed_task"] == ongoingPosValue["total_task"]:
            ongoingPosQry.done = True

            db.session.commit()

            qry = Position.query.get(ongoingPosValue["position_id"])
            value = marshal(qry, Position.response_field)
            print(value["certificate_trigger_score"])
            print(ongoingPosValue["average_score"])

            if ongoingPosValue["average_score"] >= value["certificate_trigger_score"]:
                self.MakeCertificate(ongoingPosValue, ongoingTaskValue)


    def MakeCertificate(self, OnPos, OnTask):
        certificateLink = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu15fBle4UZCpl_PFaRd15V4Sm_n8Ir2-9JBhcH-xm87UNWFko&s"
        certificate = Certificate(OnTask['position_id'], OnTask['company_id'], OnTask['intern_id'],  datetime.datetime.now(), certificateLink, OnPos['average_score'])

        db.session.add(certificate)
        db.session.commit()

        app.logger.debug('DEBUG : %s ', certificate )


api.add_resource(CompanyAcceptanceResource, '', '')