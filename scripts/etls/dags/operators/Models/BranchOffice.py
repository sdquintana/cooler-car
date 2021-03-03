from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer

Base = declarative_base()


class BranchOffice(Base):
    __tablename__ = 'CAT_BRANCH_OFFICE'
    __table_args__ = {'schema': 'cooler_car'}

    branch_office_id = Column(Integer, primary_key=True)
    branch_code = Column(Integer)


class HistBranchOffice(Base):
    __tablename__ = 'HIST_BRANCH_OFFICE'
    __table_args__ = {'schema': 'cooler_car'}

    branch_office_id = Column(Integer, primary_key=True)
    hash_key = Column(String, primary_key=True)
    name = Column(String)
    address_1 = Column(String)
    address_2 = Column(String)
    cp = Column(String)
    city = Column(String)
    state = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)
