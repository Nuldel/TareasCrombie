from fastapi import FastAPI, Depends
from core.config import settings
from db.session import engine, get_db
from db.tables import Base
from db.repository import create_Task, show_Tasks, show_All, delete_Task, change_status
from db.schemas import newTask
from sqlalchemy.orm import Session

# creamos tablas en base al esquema farbicado en db/
def create_tables():
    Base.metadata.create_all(bind=engine)

def start_app():
    taskApp = FastAPI(tittle=settings.PROJECT_NAME)
    create_tables()
    return taskApp

taskApp = start_app()

@taskApp.get("/tareas")
def fetch_all(db: Session = Depends(get_db)):
    return show_All(db)

@taskApp.get("/tareas/{category}")
def filter_category(category, db: Session = Depends(get_db)):
    return show_Tasks(category, db)

@taskApp.post("/tareas/")
def add_Task(task: newTask, db: Session = Depends(get_db)):
    return create_Task(task, db)

@taskApp.put("/tareas/{id}")
def update_Task(id, category, db: Session = Depends(get_db)):
    return change_status(int(id), category, db)

@taskApp.delete("/tareas/{id}")
def remove_Task(id, db: Session = Depends(get_db)):
    return delete_Task(int(id), db)
