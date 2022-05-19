from fastapi import APIRouter, Depends
from db.repository import create_Task, show_Tasks, show_All, delete_Task, change_status
from sqlalchemy.orm import Session
from db.schemas import newTask
from db.session import get_db

task_router = APIRouter()

# creamos una dependencia de la BBDD para poder reemplazarla en los tests
# (inyeccion de dependencias)
@task_router.get("/tareas")
def fetch_all(db: Session = Depends(get_db)):
    return show_All(db)

@task_router.get("/tareas/{category}")
def filter_category(category, db: Session = Depends(get_db)):
    return show_Tasks(category, db)

@task_router.post("/tareas/")
def add_Task(task: newTask, db: Session = Depends(get_db)):
    return create_Task(task, db)

@task_router.put("/tareas/{id}")
def update_Task(id, category, db: Session = Depends(get_db)):
    return change_status(int(id), category, db)

@task_router.delete("/tareas/{id}")
def remove_Task(id, db: Session = Depends(get_db)):
    return delete_Task(int(id), db)
