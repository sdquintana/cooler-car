from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Date, Float

Base = declarative_base()


class Rent(Base):
    __tablename__ = 'CAT_RENT'
    __table_args__ = {'schema': 'cooler_car'}

    trip_id = Column(Integer, primary_key=True)
    number = Column(String)


class RelUserRent(Base):
    __tablename__ = 'REL_USER_RENT'
    __table_args__ = {'schema': 'cooler_car'}

    trip_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    hash_key = Column(String, primary_key=True)
    rental_date = Column(Date)
    delivery_date = Column(Date)
    branch_office_id = Column(Integer)
    payment_method_id = Column(Integer)
    fare = Column(Float)
    damage_fee = Column(Float)
    car_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)
