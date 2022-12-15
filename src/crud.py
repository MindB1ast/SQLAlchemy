from datetime import datetime

from sqlalchemy.orm import Session

from src import models, schemas
from sqlalchemy import select

from fastapi import HTTPException





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


#def get_apartment_by_shn(db: Session, Street: str, House: str, Number: str):
#    apartment = db.query(models.Apartment).filter_by(street=Street, house=House, number=Number).first()
#    return apartment


def get_apartment(db: Session, apartment_id: int):
    """
    Получить владельцев квартиры по id
    """
    return db.query(models.Apartment).filter(models.Apartment.id == apartment_id).first()


# добавить проверку на наличие квартиры у renterа
def create_apartment(db: Session, apartment: schemas.ApertmentCreate, renter_id: int):
    """
    Добавление нового пользователя
    """
    # renter= get_renter(db, apartment.owner_id)

    #if get_apartment_by_shn(db, apartment.street, apartment.house, apartment.number) is not None:
    #    raise HTTPException(status_code=404, detail="Apartment with this location already exist")

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


def create_payment(db: Session, payment: schemas.PaymentBase, Renter_id: int, Service_id: int
                   ):
    db_payment = models.Payment(**payment.dict(), renter_id=Renter_id, service_id=Service_id
                                )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


#def get_payments(db: Session, skip: int = 0, limit: int = 100):
#   """
#    Получить владельцев квартир
#    """
#    return db.query(models.Payment).offset(skip).limit(limit).all()


#def get_payments_by_renter(db: Session, renter_id: int):
#    return db.query(models.Payment).filter_by(renter_id=renter_id).all()


def create_service(db: Session, service: schemas.ServiceCreate, service_type_id: int):
    #db_service = models.Service(**service.dict(),  service_type_id=service_type_id )
    db_service = models.Service(
        service_number=service.service_number,
        tariff=service.tariff,
        service_type_id=  service_type_id
    )

    #print(db_service.__dict__)

    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_services(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить услуги
    """
    return db.query(models.Service).offset(skip).limit(limit).all()


def get_service_by_id(db: Session, service_id: int):
    """
    Получить услугу по id
    """
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def get_service_types(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить виды услуг
    """
    return db.query(models.Service_type).offset(skip).limit(limit).all()

def get_service_type_by_id(db: Session, service_type_id: int):
    """
    Получить услугу по id
    """
    return db.query(models.Service_type).filter(models.Service_type.id == service_type_id).first()


def create_service_type(db: Session, service_type: schemas.ServiceTypeCreate):
    """
    Добавление новый тип услуг
    """
    db_service_type = models.Service_type(name=service_type.name, mesure=service_type.mesure)
    #print(service_type.__dict__)
    # db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_service_type)
    # db.add(db_user)
    db.commit()
    db.refresh(db_service_type)
    return db_service_type
