import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Integer

Base = declarative_base()


class LuCarType(Base):
    __tablename__ = 'LU_TRADE_MARK_TYPE'
    __table_args__ = {'schema': 'cooler_car'}

    trade_mark_type_id = Column(Integer, primary_key=True)
    code = Column(String)
    description_us = Column(String)
    description_es = Column(String)
    is_active = Column(Boolean)
