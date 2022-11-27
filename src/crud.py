from sqlalchemy.orm import Session

from src import models, schemas


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
    db_renter = models.Renter(accaunt=renter.accaunt, name=renter.name, second_name=renter.second_name,
                              middle_name=renter.middle_name, phone_number=renter.phone_number,
                              # apartment=null
                              )
    # db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_renter)
    # db.add(db_user)
    db.commit()
    db.refresh(db_renter)
    return db_renter


def get_renter_by_accaunt(db: Session, accaunt: int):
    """
    Получить пользователя по его email
    """
    return db.query(models.Renter).filter(models.Renter.accaunt == accaunt).first()


def get_apartments(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить владельцев квартир
    """
    return db.query(models.Apartment).offset(skip).limit(limit).all()


def get_apartment(db: Session, apartment_id: int):
    """
    Получить владельцев квартиры по id
    """
    return db.query(models.Renter).filter(models.Renter.id == apartment_id).first()


# добавить проверку на наличие квартиры у renterа
def create_apartment(db: Session, apartment: schemas.ApertmentCreate):
    """
    Добавление нового пользователя
    """

    db_apartment = models.Apartment(


        street=apartment.street,
        house=apartment.house,
        number=apartment.number,
        resedents=apartment.resedents,
        area=apartment.area,
        owner_id=apartment.owner_id)

    #db_item = models.Item(**item.dict(), owner_id=user_id)
    print(db_apartment)
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment


# def create_user_item2(db: Session, item: schemas.ItemCreate, user_id: int):
#    """
#    Добавление нового Item пользователю
#    """
#    db_item = models.Item(**item.dict(), owner_id=user_id)
#    db.add(db_item)
#    db.commit()
#    db.refresh(db_item)
#    return db_item
