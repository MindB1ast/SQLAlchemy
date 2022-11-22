from pydantic import BaseModel


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

class RenterBase(BaseModel):
    """
    Базовый класс для Renter
    """
    name:str
    second_name:str
    middle_name:str | None = None
    
    
class RenterCreate(RenterBase):
    """
    Класс для создания владельца
    """
    accaunt:int
    phone_number:int

class Renter(RenterBase):
    """
    Класс для отображения владельца
    """
    id:int
    accaunt:int
    phone_number:int
    #apartment:
    class Config:
        """
        Задание настройки для возможности работать с объектами ORM
        """
        orm_mode = True

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


