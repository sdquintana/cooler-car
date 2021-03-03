from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer

Base = declarative_base()


class PayPalAccount(Base):
    __tablename__ = 'CAT_PAYPAL_ACCOUNT'
    __table_args__ = {'schema': 'cooler_car'}

    paypal_account_id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)


class RelPayPalAccount(Base):
    __tablename__ = 'REL_PAYPAL_ACCOUNT'
    __table_args__ = {'schema': 'cooler_car'}

    payment_method_id = Column(Integer, primary_key=True)
    paypal_account_id = Column(Integer)
    hash_key = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)



