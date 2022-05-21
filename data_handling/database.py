from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
# db = SQLAlchemy(app)

db = SQLAlchemy()


class Init_values(db.Model):
    """
    Class for interacting with DB
    """
    __tablename__ = 'init_values'

    id = db.Column(db.Integer, primary_key=True)
    m1 = db.Column(db.Float)
    m2 = db.Column(db.Float)
    l1 = db.Column(db.Float)
    l2 = db.Column(db.Float)
    alpha1 = db.Column(db.Float)
    alpha2 = db.Column(db.Float)
    drive_id = db.Column(db.String(60))

    def __init__(self, m1, m2, l1, l2, alpha1, alpha2, drive_id):
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.drive_id = drive_id

    @classmethod
    def check_launch(cls, initials):
        """
        Check whether there is such object in DB
        :param initials:
        :return: list of objects
        """
        return cls.query.filter_by(**initials).all()

    def save_to_db(self):
        """
        Save object to DB
        :return:
        """
        db.session.add(self)
        db.session.commit()


if __name__ == '__main__':
    l1, l2 = 5., 2.
    m1, m2 = 1.0, 0.1
    alpha1, alpha2 = 30, 50
    drive_id = '1ZoSydMxknjPMkVf-Gz8Qge5Cc_5M4Ztf'

    launch1 = Init_values(m1, m2, l1, l2, alpha1, alpha2, drive_id)
    launch1.save_to_db()
    initials = dict(m1=m1, m2=m2, l1=l1, l2=l2, alpha1=alpha1, alpha2=alpha2)

    print(Init_values.check_launch(initials))
    print(initials)
