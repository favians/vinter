from blueprints import db
from flask_restful import fields


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=False)
    role = db.Column(db.String(255), nullable=True)

    response_field = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'name': fields.String,
        'username': fields.String,
        'image': fields.String,
        'address': fields.String,
        'active': fields.Boolean,
        'role': fields.String,
    }

    def __init__(self, created_at, name, username,password, image, address, active, role):
        self.created_at = created_at
        self.name = name
        self.username = username
        self.password = password
        self.image = image
        self.address = address
        self.active = active
        self.role = role

    def __repr__(self):
        return '<Company %r>' % self.id