from fastapi import FastAPI
from core.config import settings
from db.session import engine
from db.tables import Base

# creamos tablas en base al esquema farbicado en db/
def create_tables():
    Base.metadata.create_all(bind=engine)

def start_app():
    taskApp = FastAPI(tittle=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()

taskApp = start_app()
