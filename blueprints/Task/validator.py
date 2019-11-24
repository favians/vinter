from blueprints import db, app
from .model import Task
from flask_restful import Resource, marshal
from blueprints.Position.model import Position
from blueprints.Task.model import Task

class Validation(Resource):

    def ValidatePositionOwnership(self, PositionValue, claimsID):

        qry = Position.query.get(PositionValue)
        value = marshal(qry, Task.response_field)
        if value["company_id"] == claimsID:
            return True

        return False

    def ValidateExistence(self, PositionValue, claimsID):

        qry = Task.query.filter_by(position_id=PositionValue).filter_by(company_id=claimsID).all()
        if len(qry) < 1:
            return True

        return False