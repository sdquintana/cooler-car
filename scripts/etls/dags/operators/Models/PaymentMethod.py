from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Integer

Base = declarative_base()


class PaymentMethod(Base):
    __tablename__ = 'CAT_PAYMENT_METHOD'
    __table_args__ = {'schema': 'cooler_car'}

    payment_method_id = Column(Integer, primary_key=True)
    payment_method_type_id = Column(Integer)


class RelPaymentMethod(Base):
        __tablename__ = 'REL_PAYMENT_METHOD'
        __table_args__ = {'schema': 'cooler_car'}

        wallet_id = Column(Integer, primary_key=True)
        payment_method_id = Column(Integer)
        user_id = Column(Integer)
        hash_key = Column(String, primary_key=True)
        principal = Column(Boolean)
        created_at = Column(DateTime)
        updated_at = Column(DateTime)
        is_active = Column(Boolean)


