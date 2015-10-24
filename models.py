from app import db

from sqlalchemy import text

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(64), unique=False)
    service_type  = db.Column(db.String(64))
    house = db.Column(db.String(64), unique=False)
    street = db.Column(db.String(120), unique=True)
    schedule = db.relationship('Schedule', backref='service')

    def __repr__(self):
        return '<Service %r>' % (self.name)
    def get_id(self):
        return str(self.id)  # python 3


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key = True)
    open_on = db.Column(db.DateTime)
    close_on = db.Column(db.DateTime)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))

