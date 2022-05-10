from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Launches(db.Model):
    __tablename__ = 'launches'

    id = db.Column(db.Integer, primary_key=True)
    m1 = db.Column(db.Float)
    m2 = db.Column(db.Float)
    l1 = db.Column(db.Float)
    l2 = db.Column(db.Float)
    drive_id = db.Column(db.String(60))

    def __init__(self, m1, m2, l1, l2, drive_id):
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2
        self.drive_id = drive_id

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
