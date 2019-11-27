from blueprints import db
from flask_restful import fields


class Intern(db.Model):
    __tablename__ = "interns"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=True, default=True)
    role = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(1024), nullable=True)
    pendidikan = db.Column(db.String(1024), nullable=True)
    deskripsi = db.Column(db.String(2048), nullable=True)

    response_field = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'name': fields.String,
        'image': fields.String,
        'address': fields.String,
        'active': fields.Boolean,
        'role': fields.String,
        'email': fields.String,
        'pendidikan': fields.String,
        'deskripsi': fields.String,
    }

    def __init__(self, created_at, name, password, image, address, active, role, email, pendidikan, deskripsi):
        self.created_at = created_at
        self.name = name
        self.password = password
        self.image = image
        self.address = address
        self.active = active
        self.role = role
        self.email = email
        self.pendidikan = pendidikan
        self.deskripsi = deskripsi

    def __repr__(self):
        return '<Intern %r>' % self.id