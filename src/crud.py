from datetime import datetime

from sqlalchemy.orm import Session

from src import models, schemas
from sqlalchemy import select

from fastapi import HTTPException


def create_user(db: Session, user: schemas.UserCreate):
    """
    Добавление нового пользователя
    """
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """
    Добавление нового Item пользователю
    """
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_user(db: Session, user_id: int):
    """
    Получить пользователя по его id
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Получить пользователя по его email
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список предметов из БД
    skip - сколько записей пропустить
    limit - маскимальное количество записей
    """
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список пользователей из БД
    skip - сколько записей пропустить
    limit - маскимальное количество записей
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def get_renters(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить владельцев квартир
    """
    return db.query(models.Renter).offset(skip).limit(limit).all()


def get_renter(db: Session, renter_id: int):
    """
    Получить владельцев квартиры по id
    """
    return db.query(models.Renter).filter(models.Renter.id == renter_id).first()


def create_renter(db: Session, renter: schemas.RenterCreate):
    """
    Добавление нового пользователя
    """
    db_renter = models.Renter(account=renter.account, name=renter.name, second_name=renter.second_name,
                              middle_name=renter.middle_name, phone_number=renter.phone_number
                              # apartment=null
                              )
    # db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_renter)
    # db.add(db_user)
    db.commit()
    db.refresh(db_renter)
    return db_renter


def get_renter_by_account(db: Session, account: int):
    """
    Получить пользователя по его email
    """
    return db.query(models.Renter).filter(models.Renter.account == account).first()


def get_apartments(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить владельцев квартир
    """
    return db.query(models.Apartment).offset(skip).limit(limit).all()


def get_apartment_by_shn(db: Session, Street: str, House: str, Number: str):
    apartment = db.query(models.Apartment).filter_by(street=Street, house=House, number=Number).first()
    return apartment


def get_apartment(db: Session, apartment_id: int):
    """
    Получить владельцев квартиры по id
    """
    return db.query(models.Renter).filter(models.Renter.id == apartment_id).first()


# добавить проверку на наличие квартиры у renterа
def create_apartment(db: Session, apartment: schemas.ApertmentCreate, renter_id: int):
    """
    Добавление нового пользователя
    """
    # renter= get_renter(db, apartment.owner_id)

    if get_apartment_by_shn(db, apartment.street, apartment.house, apartment.number) is not None:
        raise HTTPException(status_code=404, detail="Apartment with this location already exist")

    db_apartment = models.Apartment(
        street=apartment.street,
        house=apartment.house,

        number=apartment.number,
        resedents=apartment.resedents,
        area=apartment.area,
        owner_id=renter_id
    )
    # db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment


def create_payment(db: Session, payment: schemas.PaymentBase, Renter_id: int #, Service_id: int
                   ):
    db_payment = models.Payment(**payment.dict(), renter_id=Renter_id#, service_id=Service_id
                                )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payments(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить владельцев квартир
    """
    return db.query(models.Payment).offset(skip).limit(limit).all()


def get_payments_by_renter(db: Session, renter_id: int):
    return db.query(models.Payment).filter_by(renter_id=renter_id).all()


def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(
        service_number=service.service_number,
        tariff=service.tariff,
    )

    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_services(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить услуги
    """
    return db.query(models.Service).offset(skip).limit(limit).all()