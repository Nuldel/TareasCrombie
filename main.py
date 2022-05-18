from fastapi import FastAPI
from core.config import settings
from db.session import engine, get_db
from db.tables import Base
from db.repository import create_Task, show_Tasks, show_All

# creamos tablas en base al esquema farbicado en db/
def create_tables():
    Base.metadata.create_all(bind=engine)

def start_app():
    taskApp = FastAPI(tittle=settings.PROJECT_NAME)
    create_tables()

taskApp = start_app()

@taskApp.get("/tareas")
def fetch_all():
    return show_All(get_db())

@taskApp.get("/tareas/{category}")
def filter_category(category):
    return show_Tasks(category, get_db())
