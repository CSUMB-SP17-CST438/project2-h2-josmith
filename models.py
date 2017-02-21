from app import db
from sqlalchemy.dialects.postgresql import JSON


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    massage = db.Column(JSON)

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return '<id {}>'.format(self.id)
