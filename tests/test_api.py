from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Тестовая БД

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    """
    Данная функция при тестах будет подменять функцию get_db() в main.py.
    Таким образом приложение будет подключаться к тестовой базе данных.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению


def test_create_renter():
    """
    Тест на создание нового владельца
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/renter/", json={
        "name": "ivan",
        "second_name": "ivanov",
        "middle_name": "ivanovich",
        "account": 1,
        "phone_number": 79088822891
    })

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "ivan"


def test_create_renter_email_exist():
    """
    Тест на создание нового владельца
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/renter/", json={
        "name": "ivan",
        "second_name": "ivanov",
        "middle_name": "ivanovich",
        "account": 1,
        "phone_number": 79088822891
    })

    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Email already registered"

def test_get_renters():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/renter/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["phone_number"] == 79088822891


def test_get_renter_acc():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/renters/account/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["phone_number"] == 79088822891


def test_get_renter_acc_not_found():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/renters/account/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Renter not found"




def test_get_renter_id():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/renters/id/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["phone_number"] == 79088822891


def test_get_renter_id_not_found():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/renters/id/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Renter not found"


def test_create_service_type():
    """
    Тест на создание типов услуги
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/Service_type/", json={
        "name": "water",
        "mesure": "string"
    })

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "water"


def test_get_service_type():
    """
    Тест на получение списка типов услуг
    """
    response = client.get("/Service_types/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["name"] == "water"


def test_create_service():
    """
    Тест на создание услуги
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/Service_types/1/Service/", json={
        "service_number": 0,
        "tariff": 0})

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["service_number"] == 0
    assert data["tariff"] == 0
    # assert data["service_type_id"] == 1

def test_create_service_service_type_not_exist():
    """
    Тест на создание услуги
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/Service_types/2/Service/", json={
        "service_number": 0,
        "tariff": 0})

    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "service type in not exsist"


def test_get_services(): # pragma: no cover
    """
    Тест на получение списка услуг
    """
    response = client.get("/Services/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["service_number"] == 0


def test_create_apartment():
    """
    Тест на создание квартиры
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/renter/1/apartment/", json={
        "street": "string",
        "house": "stsring",
        "number": "string",
        "resedents": 0,
        "area": 0
    })
    print(response.json())
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["street"] == "string"
    assert data["area"] == 0
    assert data["owner_id"] == 1



def test_create_apartment_miss_renter():
    """
    Тест на создание квартиры несуществующему владельцу
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/renter/2/apartment/", json={
        "street": "string",
        "house": "stsraing",
        "number": "string",
        "resedents": 0,
        "area": 0
    })
    print(response.json())
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User not found, create user first or use other user"




def test_get_apartments():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/apartment/")
    assert response.status_code == 200, response.text
    data = response.json()
    # print(response.__dict__)
    assert data[0]["street"] == "string"


def test_create_apartment_alredy_exist():
    """
    Тест на создание квартиры владельцу с квартирой
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})

    response = client.post("/renter/1/apartment/", json={
        "street": "string",
        "house": "stsraing",
        "number": "string",
        "resedents": 0,
        "area": 0
    })
    print(response.json())
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User alredy have apartment"


def test_get_apartment_id():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/apartment/1")
    assert response.status_code == 200, response.text
    print(response.__dict__)
    data = response.json()
    assert data["street"] == "string"


def test_get_apartment_id_miss():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/apartment/2")
    assert response.status_code == 404, response.text
    data = response.json()
    # print(response.__dict__)
    assert data["detail"] == "apartment is not exist"


def test_create_payment():
    """
    Тест на создание оплаты
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/renter/1/payment/?service_id=1", json={
        "actualy_spent": 0,
        "border_date": "2022-12-12T19:25:05",
        "payed_in_time": True,
        "date_of_payment": "2022-12-12T19:25:05"
    })
    print(response.json())
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["actualy_spent"] == 0
    assert data["border_date"] == "2022-12-12T19:25:05"
    assert data["renter_id"] == 1
    assert data["service_id"] == 1

def test_create_payment_renter_not_found():
    """
    Тест на создание оплаты
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/renter/2/payment/?service_id=1", json={
        "actualy_spent": 0,
        "border_date": "2022-12-12T19:25:05",
        "payed_in_time": True,
        "date_of_payment": "2022-12-12T19:25:05"
    })
   # print(response.json())
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Renter not found, create user first or use other user"


def test_create_payment_service_not_found():
    """
    Тест на создание оплаты
    """
    # response = client.post("/users/", json={"email": "email@example.com", "password": "qwe123"})
    response = client.post("/renter/1/payment/?service_id=2", json={
        "actualy_spent": 0,
        "border_date": "2022-12-12T19:25:05",
        "payed_in_time": True,
        "date_of_payment": "2022-12-12T19:25:05"
    })
   # print(response.json())
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Service is not found"


def test_get_services():
    """
    Тест на получение списка услуг
    """
    response = client.get("/Services/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["service_number"] == 0


