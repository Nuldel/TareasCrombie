from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from typing import Any
from typing import Generator
from ..db.base import Base
from fastapi.testclient import TestClient
from ..db.session import get_db

def start_app():
    taskApp = FastAPI()
    return taskApp

DB_URL = "sqlite:///./test_db.db"
engine = create_engine(DB_URL)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    app = start_app()
    yield app
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[TestSession, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSession(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(app: FastAPI, session: TestSession) -> Generator[TestClient, Any, None]:
    def get_test_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client
