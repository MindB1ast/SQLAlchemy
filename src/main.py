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


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Создание пользователя, если такой email уже есть в БД, то выдается ошибка
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка пользователей
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получение пользователя по id, если такого id нет, то выдается ошибка
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """
    Добавление пользователю нового предмета
    """
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка предметов
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


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
def read_reanter_by_accaunt(accaunt: int, db: Session = Depends(get_db)):
    """
    Получение владельца по номеру лицевого счёта, если такого нет, то выдается ошибка
    """
    db_renter = crud.get_renter_by_accaunt(db, accaunt=accaunt)
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
def create_payment_for_renter(owner_id: int, payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    """
    Добавление квартиросёмщику оплаты
    """

    renter = crud.get_renter(db, renter_id=owner_id)

    if (renter is None):
        raise HTTPException(status_code=404, detail="User not found, create user first or use other user")

    return crud.create_payment(db=db, payment=payment, Renter_acount=renter.account)


@app.get("/payment/", response_model=list[schemas.Payment])
def read_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка оплат
    """
    payments = crud.get_payments(db, skip=skip, limit=limit)
    return payments
