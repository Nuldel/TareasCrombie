from fastapi import FastAPI
from core.config import settings
from db.session import engine
from db.tables import Base, Task
from db.repository import create_Task, show_Tasks, show_All, delete_Task, change_status
from db.schemas import newTask

# creamos tablas en base al esquema farbicado en db/
def create_tables():
    Base.metadata.create_all(bind=engine)

def start_app():
    taskApp = FastAPI(tittle=settings.PROJECT_NAME)
    create_tables()
    return taskApp

taskApp = start_app()

@taskApp.get("/tareas")
def fetch_all():
    return show_All()

@taskApp.get("/tareas/{category}")
def filter_category(category):
    return show_Tasks(category)

@taskApp.post("/tareas/")
def add_Task(task: newTask):
    return create_Task(task)

@taskApp.put("/tareas/{id}")
def update_Task(id, category):
    return change_status(int(id), category)

@taskApp.delete("/tareas/{id}")
def remove_Task(id):
    return delete_Task(int(id))
