from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#SQLALCHEMY_DATABASE_URL = environ.get('DATABASE_URL')

#engine = create_engine(SQLALCHEMY_DATABASE_URL)

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

######################3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_base.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


