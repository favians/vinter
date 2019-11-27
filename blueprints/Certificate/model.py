from blueprints import db
from flask_restful import fields


class Certificate(db.Model):
    __tablename__ = "certificate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    intern_id = db.Column(db.Integer, db.ForeignKey('interns.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String(2048), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    response_field = {
        'id': fields.Integer,
        'position_id': fields.Integer,
        'company_id': fields.Integer,
        'intern_id': fields.Integer,

        'created_at': fields.DateTime,
        'image': fields.String,
        'score': fields.Integer,
    }

    def __init__(self, position_id, company_id, intern_id, created_at, image, score):
        self.position_id = position_id
        self.company_id = company_id
        self.intern_id = intern_id

        self.created_at = created_at
        self.image = image
        self.score = score

    def __repr__(self):
        return '<Certificate %r>' % self.id