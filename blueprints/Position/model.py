from blueprints import db
from flask_restful import fields


class Position(db.Model):
    __tablename__ = "position"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(2048), nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=False)
    certificate_trigger_score = db.Column(db.Integer, nullable=False)

    response_field = {
        'id': fields.Integer,
        'company_id': fields.Integer,

        'created_at': fields.DateTime,
        'name': fields.String,
        'description': fields.String,
        'active': fields.Boolean,
        'certificate_trigger_score': fields.Integer,
    }

    def __init__(self, company_id, created_at, name, description, active, certificate_trigger_score):
        self.company_id = company_id

        self.created_at = created_at
        self.name = name
        self.description = description
        self.active = active
        self.certificate_trigger_score = certificate_trigger_score

    def __repr__(self):
        return '<Position %r>' % self.id