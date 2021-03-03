from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer

Base = declarative_base()


class Person(Base):
    __tablename__ = 'CAT_PERSON'
    __table_args__ = {'schema': 'cooler_car'}

    person_id = Column(Integer, primary_key=True)


class HistPerson(Base):
    __tablename__ = 'HIST_PERSON'
    __table_args__ = {'schema': 'cooler_car'}

    person_id = Column(Integer, primary_key=True)
    hash_key = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    second_name = Column(String)
    last_name = Column(String)
    second_last_name = Column(String)
    curp = Column(String)
    rfc = Column(String)
    ine_number = Column(String)
    person_type_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)
