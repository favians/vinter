from blueprints import db
from flask_restful import fields


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(2048), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=True, default=False)
    order = db.Column(db.String(255), nullable=True)

    response_field = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'name': fields.String,
        'description': fields.String,
        'active': fields.Boolean,
        'order': fields.String,
    }

    def __init__(self, created_at, name, description, active, order):
        self.created_at = created_at
        self.name = name
        self.description = description
        self.active = active
        self.order = order

    def __repr__(self):
        return '<Task %r>' % self.id