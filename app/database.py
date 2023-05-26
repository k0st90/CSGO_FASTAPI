from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import config

SQLALCHEMY_DATABASE_URL = f'postgresql://{config.database_username.get_secret_value()}:{config.database_password.get_secret_value()}@{config.database_hostname.get_secret_value()}:{config.database_port.get_secret_value()}/{config.database_name.get_secret_value()}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()