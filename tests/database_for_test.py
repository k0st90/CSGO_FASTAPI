from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.settings import config
from app.database import get_db, Base
import pytest

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:assasin1q2w@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{config.database_username.get_secret_value()}:{config.database_password.get_secret_value()}@{config.database_hostname.get_secret_value()}:{config.database_port.get_secret_value()}/{config.database_name.get_secret_value()}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)