from blueprints import db
from flask_restful import fields


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=False)
    role = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(2048), nullable=True)
    industry = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)

    response_field = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'name': fields.String,
        'email': fields.String,
        'image': fields.String,
        'address': fields.String,
        'active': fields.Boolean,
        'role': fields.String,
        'description': fields.String,
        'industry': fields.String,
        'location': fields.String,
    }

    def __init__(self, created_at, name, email,password, image, address, active, role, description, industry, location):
        self.created_at = created_at
        self.name = name
        self.email = email
        self.password = password
        self.image = image
        self.address = address
        self.active = active
        self.role = role
        self.description = description
        self.industry = industry
        self.location = location

    def __repr__(self):
        return '<Company %r>' % self.id