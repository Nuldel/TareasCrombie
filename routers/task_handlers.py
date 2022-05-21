from fastapi import APIRouter, Depends, Cookie
from db.repository.task import create_Task, show_Tasks, show_All, delete_Task, edit_task
from sqlalchemy.orm import Session
from db.schemas import NewTask, CookieUser
from db.session import get_db
from typing import Union

task_router = APIRouter()

# funcion chiquita para extraer user_id de la cookie
def id_extract(user: Union[CookieUser, None]) -> Union[int, None]:
    if user != None:
        return user.id
    return None

# creamos una dependencia de la BBDD para poder reemplazarla en los tests
# (inyeccion de dependencias)
@task_router.get("/tareas")
def fetch_all(user_id: Union[int, None] = Cookie(default=None),
              db: Session = Depends(get_db)):
    return show_All(user_id, db)

@task_router.get("/tareas/{category}")
def filter_category(category, user_id: Union[int, None] = Cookie(default=None),
                    db: Session = Depends(get_db)):
    return show_Tasks(category, user_id, db)

@task_router.post("/tareas/")
def add_Task(task: NewTask, user_id: Union[int, None] = Cookie(default=None),
             db: Session = Depends(get_db)):
    return create_Task(task, user_id, db)

@task_router.put("/tareas/{id}")
def edit_task(id, category, visibility, user_id: Union[int, None] = Cookie(default=None),
              db: Session = Depends(get_db)):
    return change_status(int(id), user_id, category, visibility, db)

@task_router.delete("/tareas/{id}")
def remove_Task(id, user_id: Union[int, None] = Cookie(default=None),
                db: Session = Depends(get_db)):
    return delete_Task(int(id), user_id, db)
