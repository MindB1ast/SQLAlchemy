from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base

from sqlalchemy import Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class BaseModel(Base):
    """
    Абстартный базовый класс, где описаны все поля и методы по умолчанию
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>"


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(BaseModel):
    __tablename__ = "items"

    title = Column(String, index=True)
    description = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")


class Renter(BaseModel):
    __tablename__ = "renter"
    account = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    ##Поменять nullable
    apartment = relationship("Apartment", back_populates="owner", uselist=False)

    payments = relationship("Payment", back_populates="renter")


class Apartment(BaseModel):
    __tablename__ = "apartment"
    street = Column(String, nullable=False)
    house = Column(String, nullable=False)
    number = Column(String, nullable=False)
    resedents = Column(Integer)
    area = Column(Integer)

    owner_id = Column(Integer, ForeignKey("renter.id"), unique=True)
    owner = relationship("Renter", back_populates="apartment")


class Service_type(BaseModel):
    __tablename__ = "service_type"
    name = Column(String)
    mesure = Column(String)

    services= relationship("Service", back_populates="service_type", uselist=False)


class Service(BaseModel):
    __tablename__ = "service"
    service_number = Column(Integer)
    tariff = Column(Float)
    payments = relationship("Payment", back_populates="service")

    service_type_id = Column(Integer, ForeignKey("service_type.id"), unique=True)
    service_type = relationship("Service_type", back_populates="services")


class Payment(BaseModel):
    __tablename__ = "payment"
    actualy_spent = Column(Float)
    border_date = Column(DateTime)
    payed_in_time = Column(Boolean)
    date_of_payment = Column(DateTime)

    renter_id = Column(Integer, ForeignKey("renter.id"))
    renter = relationship("Renter", back_populates="payments")

    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service", back_populates="payments")


