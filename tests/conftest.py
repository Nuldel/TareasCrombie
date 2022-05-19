from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from typing import Any
from typing import Generator
from fastapi.testclient import TestClient

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.tables import Base
from db.session import get_db
from routers.task_handlers import task_router

# creamos una nueva app, pero con el enrutamiento original
def start_app():
    taskApp = FastAPI()
    taskApp.include_router(task_router)
    return taskApp

# usamos SQLite en lugar de la BBDD original
DB_URL = "sqlite:///tests/test_db.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# corremos la app con las mismas tablas de la BBDD original. reseteamos la
# BBDD luego de cada test (assegurando independencia, entre otras cosas).
@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    taskApp = start_app()
    yield taskApp
    Base.metadata.drop_all(engine)

# similarmente, reseteamos la sesion luego de cada test
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
def client(app: FastAPI, db_session: TestSession) -> Generator[TestClient, Any, None]:
    def get_test_db():
        try:
            yield db_session
        finally:
            pass

    # inyeccion de dependencia: cambiamos la BBDD que se usa en la app
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client
