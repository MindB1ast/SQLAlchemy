from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base

from sqlalchemy import Table, Index, Integer, String, Column, Text, \
                       DateTime, Boolean, PrimaryKeyConstraint, \
                       UniqueConstraint, ForeignKeyConstraint
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
    __tablename__="renter"
    accaunt=Column(Integer, unique=True, index=True, nullable=False)
    name=Column(String, nullable=False)
    second_name=Column(String, nullable=False)
    middle_name=Column(String, nullable=True)
    phone_number=Column(String, nullable=True)
##Поменять nullable
    #apartment=relationship("Apartment", uselist=False)


class Apartment(BaseModel):
    __tablename__="apartment"
    street=Column(String)
    house=Column(String)
    apartment=Column(String)
    resedents=Column(Integer)
    area=Column(Integer)
    
    #owner_id=Column(Integer, ForeignKey("renter.id"))
    #owner= relationship("Renter", backref="apartment", uselist=False)
    
class service_type(BaseModel):
    __tablename__="service_type"
    name=Column(String)
    mesure=Column(String)

class service(BaseModel):
    __tablename__="service"
    service_number=Column(Integer)
    tariff=Column(Integer)
    service_type_id=Column(Integer, ForeignKey("renter.id"))

    
