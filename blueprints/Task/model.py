from blueprints import db
from flask_restful import fields


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(2048), nullable=False)
    active = db.Column(db.Boolean, nullable=True, default=False)
    order = db.Column(db.Integer, nullable=False)

    response_field = {
        'id': fields.Integer,
        'company_id': fields.Integer,
        'position_id': fields.Integer,

        'created_at': fields.DateTime,
        'name': fields.String,
        'description': fields.String,
        'active': fields.Boolean,
        'order': fields.Integer,
    }

    def __init__(self, company_id, position_id, created_at, name, description, active, order):
        self.company_id = company_id
        self.position_id = position_id

        self.created_at = created_at
        self.name = name
        self.description = description
        self.active = active
        self.order = order

    def __repr__(self):
        return '<Task %r>' % self.id