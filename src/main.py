from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    """
    Задаем зависимость к БД. При каждом запросе будет создаваться новое
    подключение.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/renter/", response_model=schemas.Renter)
def create_renter(renter: schemas.RenterCreate, db: Session = Depends(get_db)):
    """
    Создание пользователя, если такой email уже есть в БД, то выдается ошибка
    """
    db_renter = crud.get_renter_by_account(db, account=renter.account)
    if db_renter:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_renter(db=db, renter=renter)


@app.get("/renter/", response_model=list[schemas.Renter])
def read_renters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка владельцев
    """
    renters = crud.get_renters(db, skip=skip, limit=limit)
    return renters


@app.get("/renters/accaunt/{accaunt}", response_model=schemas.Renter)
def read_reanter_by_accaunt(account: int, db: Session = Depends(get_db)):
    """
    Получение владельца по номеру лицевого счёта, если такого нет, то выдается ошибка
    """
    db_renter = crud.get_renter_by_account(db, account=account)

    if db_renter is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_renter


@app.get("/renters/id/{id}", response_model=schemas.Renter)
def read_reanter_by_id(id: int, db: Session = Depends(get_db)):
    """
    Получение Владельца по id, если такого id нет, то выдается ошибка
    """
    db_renter = crud.get_renter(db, renter_id=id)
    if db_renter is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_renter


@app.get("/apartment/", response_model=list[schemas.Apartment])
def read_apartments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка владельцев
    """
    apartments = crud.get_apartments(db, skip=skip, limit=limit)
    return apartments


@app.get("/apartment/{id}", response_model=schemas.Apartment)
def read_apartment(id: int, db: Session = Depends(get_db)):
    """
    Получение Квартиры по id, если такого id нет, то выдается ошибка
    """
    db_apartment = crud.get_apartment(db, apartment_id=id)
    if db_apartment is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_apartment


@app.post("/renter/{renter_id}/apartment/", response_model=schemas.Apartment)
def create_apartment_for_renter(owner_id: int, apartment: schemas.ApertmentCreate, db: Session = Depends(get_db)):
    """
    Добавление квартиросёмщику придмета
    """

    renter = crud.get_renter(db, renter_id=owner_id)

    if (renter is None):
        raise HTTPException(status_code=404, detail="User not found, create user first or use other user")
    if (renter.apartment is not None):
        raise HTTPException(status_code=404, detail="User alredy have apartment")
    return crud.create_apartment(db=db, apartment=apartment, renter_id=owner_id)


# Не закончено
# @app.get("/apartment/search", response_model=schemas.Apartment)
# def apartment_find(search: schemas.ApartmentSearch, db: Session = Depends(get_db)):
#
#    apartment = crud.get_apartment_by_shn(db=db, Street=search.Street, House=search.House, Number=search)
#
#    if apartment is None:
#        raise HTTPException(status_code=404, detail="Apartment does not exist")
#
#    return apartment

@app.post("/renter/{renter_id}/payment/", response_model=schemas.Payment)
def create_payment_for_renter(renter_id: int, service_id: int, payment: schemas.PaymentCreate,
                              db: Session = Depends(get_db)):
    """
    Добавление квартиросёмщику оплаты
    """
    # print(renter_id)
    renter = crud.get_renter(db=db, renter_id=renter_id)
    service = crud.get_service_by_id(db=db, service_id=service_id)
    if (renter is None):
        raise HTTPException(status_code=404, detail="Renter not found, create user first or use other user")

    if (service is None):
        raise HTTPException(status_code=404, detail="Service is not found")

    payment = crud.create_payment(db=db, payment=payment, Renter_id=renter_id, Service_id=service_id)

    return payment


# @app.get("/renter/{renter_id}/payment/")
# def get_payments_by_renter( db: Session = Depends(get_db), renter_id: int):
#    print(renter_id)
#    return crud.get_payments_by_renter( db=db )#,renter_id=renter_id )

@app.get("/Services/", response_model=list[schemas.Service])
def read_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение услуг
    """
    Services = crud.get_services(db, skip=skip, limit=limit)
    return Services


@app.post("/Service_types/{service_type_id}/Service/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, service_type_id: int, db: Session = Depends(get_db)):
    """
    Создание пользователя, если такой email уже есть в БД, то выдается ошибка
    """
    # db_service = crud.get_renter_by_account(db, account=renter.account)
    # if db_renter:
    #    raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_service(db=db, service=service, service_type_id=service_type_id)


@app.get("/Service_types/", response_model=list[schemas.ServiceType])
def read_service_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение видов услуг
    """
    Services_types = crud.get_service_types(db, skip=skip, limit=limit)
    return Services_types


@app.post("/Service_type/", response_model=schemas.ServiceType)
def create_service_id(service_type: schemas.ServiceTypeCreate, db: Session = Depends(get_db)):
    """
    Создать тип услуг
    """
    db_service_type = crud.create_service_type(db=db, service_type=service_type)

    return db_service_type
