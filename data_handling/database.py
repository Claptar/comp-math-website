from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, FLOAT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_URL = os.environ.get('DB_URL')
Base = declarative_base()

x10, y10 = 3., -4.
x20, y20 = 3., -6.
vx10, vy10 = 0., 0.
vx20, vy20 = 0., 0.
lambda10, lambda20 = 100., 100.
M = 2000


class Launches(Base):
    __tablename__ = 'launches'

    id = Column(Integer, primary_key=True)
    x1 = Column(FLOAT)
    y1 = Column(FLOAT)
    x2 = Column(FLOAT)
    y2 = Column(FLOAT)
    vx1 = Column(FLOAT)
    vy1 = Column(FLOAT)
    vx2 = Column(FLOAT)
    vy2 = Column(FLOAT)
    lambda1 = Column(FLOAT)
    lambda2 = Column(FLOAT)
    interval_num = Column(Integer)
    drive_id = Column(String(60))
    demonstration_name = Column(String(30))


engine = create_engine(DB_URL, echo=True)
#Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

drive_id = '1ZoSydMxknjPMkVf-Gz8Qge5Cc_5M4Ztf'
x10, y10 = 3., -4.122
x20, y20 = 3., -6.
vx10, vy10 = 0., 0.
vx20, vy20 = 0., 0.
lambda10, lambda20 = 100., 100.
M = 2000

launch_1 = Launches(x1=x10, y1=y10,
                    x2=x20, y2=y20,
                    vx1=vx10, vy1=vy10,
                    vx2=vx20, vy2=vy20,
                    lambda1=lambda10, lambda2=lambda20,
                    interval_num=M, drive_id=drive_id,
                    demonstration_name='pendulum')
session.add(launch_1)
session.commit()

