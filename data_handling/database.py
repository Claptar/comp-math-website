from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
# db = SQLAlchemy(app)

db = SQLAlchemy()


class Launches(db.Model):
    __tablename__ = 'launches'

    id = db.Column(db.Integer, primary_key=True)
    x1 = db.Column(db.Float)
    y1 = db.Column(db.Float)
    x2 = db.Column(db.Float)
    y2 = db.Column(db.Float)
    vx1 = db.Column(db.Float)
    vy1 = db.Column(db.Float)
    vx2 = db.Column(db.Float)
    vy2 = db.Column(db.Float)
    lambda1 = db.Column(db.Float)
    lambda2 = db.Column(db.Float)
    interval_num = db.Column(db.Integer)
    drive_id = db.Column(db.String(60))
    demonstration_name = db.Column(db.String(30))

    def __init__(self, x1, y1, x2, y2, vx1, vy1, vx2, vy2, lambda1, lambda2, interval_num, drive_id, demonstration_name):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.vx1 = vx1
        self.vy1 = vy1
        self.vx2 = vx2
        self.vy2 = vy2
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.interval_num = interval_num
        self.drive_id = drive_id
        self.demonstration_name = demonstration_name

    @classmethod
    def check_launch(cls, initials):
        return cls.query.filter_by(**initials).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


if __name__ == '__main__':
    x10, y10 = 3., -4.3
    x20, y20 = 3., -6.
    vx10, vy10 = 0., 0.
    vx20, vy20 = 0., 0.
    lambda10, lambda20 = 100., 100.
    M = 2000
    drive_id = '1ZoSydMxknjPMkVf-Gz8Qge5Cc_5M4Ztf'

    launch1 = Launches(x10, y10, x20, y20, vx10, vy10, vx20, vy20, lambda10, lambda20, M, drive_id, 'pendulum')
    launch1.save_to_db()
    initials = dict(x1=x10, y1=y10,
                    x2=x20, y2=y20,
                    vx1=vx10, vy1=vy10,
                    vx2=vx20, vy2=vy20,
                    lambda1=lambda10, lambda2=lambda20,
                    interval_num=M)

    print(Launches.check_launch(initials))
    print(initials)
