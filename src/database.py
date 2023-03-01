from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = environ.get('DB_USER')
DB_PASSWD = environ.get('DB_PASSWD')
DB_NAME = environ.get('DB_NAME')
DB_HOST = environ.get('DB_HOST')

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

######################3
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_base.db"


#engine = create_engine(
#    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


