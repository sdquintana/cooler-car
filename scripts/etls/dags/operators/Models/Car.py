from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer

Base = declarative_base()


class Car(Base):
    __tablename__ = 'CAT_CAR'
    __table_args__ = {'schema': 'cooler_car'}

    car_id = Column(Integer, primary_key=True)


class HistCar(Base):
    __tablename__ = 'HIST_CAR'
    __table_args__ = {'schema': 'cooler_car'}

    car_id = Column(Integer, primary_key=True)
    hash_key = Column(Integer, primary_key=True)
    motor_type_id = Column(Integer)
    trade_mark_type_id = Column(Integer)
    car_type_id = Column(Integer)
    niv = Column(String)
    year = Column(String)
    model = Column(String)
    expedition = Column(String)
    capacity = Column(String)
    user_id = Column(Integer)
    branch_office_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)
