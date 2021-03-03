from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer

Base = declarative_base()


class CreditCard(Base):
    __tablename__ = 'CAT_CREDIT_CARD'
    __table_args__ = {'schema': 'cooler_car'}

    credit_card_id = Column(Integer, primary_key=True)
    number = Column(String)
    expiry_date = Column(String)


class RelCreditCard(Base):
    __tablename__ = 'REL_CREDIT_CARD'
    __table_args__ = {'schema': 'cooler_car'}

    payment_method_id = Column(Integer, primary_key=True)
    credit_card_id = Column(Integer)
    hash_key = Column(String, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)

