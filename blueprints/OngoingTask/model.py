from blueprints import db
from flask_restful import fields


class OngoingPosition(db.Model):
    __tablename__ = "ongoing_task"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    intern_id = db.Column(db.Integer, db.ForeignKey('interns.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False)
    done = db.Column(db.Boolean, nullable=True, default=False)
    attachment = db.Column(db.String(1024), nullable=True)
    approve = db.Column(db.Boolean, nullable=True, default=False)
    score = db.Column(db.Integer, nullable=False)

    response_field = {
        'id': fields.Integer,
        'intern_id': fields.Integer,
        'company_id': fields.Integer,
        'position_id': fields.Integer,

        'created_at': fields.DateTime,
        'done': fields.Boolean,
        'attachment': fields.Integer,
        'approve': fields.Integer,
        'score': fields.Integer,

    }

    def __init__(self, intern_id, company_id, position_id, created_at, done, attachment, approve, score):
        self.intern_id = intern_id
        self.company_id = company_id
        self.position_id = position_id

        self.created_at = created_at
        self.done = done
        self.attachment = attachment
        self.approve = approve
        self.score = score

    def __repr__(self):
        return '<OngoingTask %r>' % self.id