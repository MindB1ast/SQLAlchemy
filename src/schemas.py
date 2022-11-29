
from pydantic import BaseModel
from datetime import datetime

class ItemBase(BaseModel):
    """
    Базовый класс для Item
    """
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    """
    Класс для создания Item, наследуется от базового ItemBase, но не содержит
    дополнительных полей, пока что
    """
    pass


class Item(ItemBase):
    """
    Класс для отображения Item, наследуется от базового ItemBase
    поля значения для полей id и owner_id будем получать из БД
    """
    id: int
    owner_id: int

    class Config:
        """
        Задание настройки для возможности работать с объектами ORM
        """
        orm_mode = True


class UserBase(BaseModel):
    """
    Базовый класс для User
    """
    email: str


class UserCreate(UserBase):
    """
    Класс для создания User. Пароль мы не должны нигде отображать, поэтому
    это поле есть только в классе для создания.
    """
    password: str


class User(UserBase):
    """
    Класс для отображения информации о User. Все значения полей будут браться
    из базы данных
    """
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    """
    Базовый класс для оплаты за услугу
    """
    actualy_spent: float
    border_date: datetime = None
    payed_in_time: bool
    date_of_payement: datetime = None



class Payment(PaymentBase):
    id: int
    renter_acount: int

    class Config:
        """
        Задание настройки для возможности работать с объектами ORM
        """
        orm_mode = True


class PaymentCreate(PaymentBase):
    pass



class ApartmentBase(BaseModel):
    street: str
    house: str
    number: str
    resedents: int
    area: int


class ApertmentCreate(ApartmentBase):
    # owner_id:int
    pass


class Apartment(ApartmentBase):
    id: int
    owner_id: int

    class Config:
        """
        Задание настройки для возможности работать с объектами ORM
        """
        orm_mode = True


class RenterBase(BaseModel):
    """
    Базовый класс для Renter
    """
    name: str
    second_name: str
    middle_name: str | None = None


class RenterCreate(RenterBase):
    """
    Класс для создания владельца
    """
    account: int
    phone_number: int


class Renter(RenterBase):
    """
    Класс для отображения владельца
    """
    id: int
    account: int
    phone_number: int

    payment: list[Payment] = []
    apartment: Apartment | None

    class Config:
        """
        Задание настройки для возможности работать с объектами ORM
        """
        orm_mode = True


class ApartmentSearch(BaseModel):
    """
    Форма для поиска дома
    """
    Street: str
    House: str
    Number: str


