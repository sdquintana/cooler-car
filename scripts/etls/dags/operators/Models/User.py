from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer

Base = declarative_base()


class User(Base):
    __tablename__ = 'CAT_USER'
    __table_args__ = {'schema': 'cooler_car'}

    user_id = Column(Integer, primary_key=True)
    email = Column(String)


class HistUser(Base):
    __tablename__ = 'HIST_USER'
    __table_args__ = {'schema': 'cooler_car'}

    user_id = Column(Integer, primary_key=True)
    hash_key = Column(String)
    password = Column(String)
    phone = Column(String)
    user_type_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)
