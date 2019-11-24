from blueprints import db
from flask_restful import fields


class OngoingPosition(db.Model):
    __tablename__ = "ongoing_position"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    intern_id = db.Column(db.Integer, db.ForeignKey('interns.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False)
    done = db.Column(db.Boolean, nullable=True, default=False)
    total_score = db.Column(db.Integer, nullable=False)
    total_task = db.Column(db.Integer, nullable=False)
    average_score = db.Column(db.Integer, nullable=False)
    completed_task = db.Column(db.Integer, nullable=False)

    response_field = {
        'id': fields.Integer,
        'intern_id': fields.Integer,
        'company_id': fields.Integer,
        'position_id': fields.Integer,

        'created_at': fields.DateTime,
        'done': fields.Boolean,
        'total_score': fields.Integer,
        'total_task': fields.Integer,
        'average_score': fields.Integer,
        'completed_task': fields.Integer,

    }

    def __init__(self, intern_id, company_id, position_id, created_at, done, total_score, total_task, average_score, completed_task):
        self.intern_id = intern_id
        self.company_id = company_id
        self.position_id = position_id

        self.created_at = created_at
        self.done = done
        self.total_score = total_score
        self.total_task = total_task
        self.average_score = average_score
        self.completed_task = completed_task

    def __repr__(self):
        return '<OngoingPosition %r>' % self.id