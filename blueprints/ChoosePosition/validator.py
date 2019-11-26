from blueprints import db, app
from flask_restful import Resource, marshal
from blueprints.Position.model import Position

from blueprints.Position.model import Position
from blueprints.OngoingPosition.model import OngoingPosition

class Validation(Resource):

    def ValidateOnGoingPositionExistence(self, PositionValue, claimsID):

        qry = OngoingPosition.query.filter_by(position_id=PositionValue).filter_by(intern_id=claimsID).all()
        if len(qry) < 1:
            return True

        return False