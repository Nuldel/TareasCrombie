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
def fetch_all(user: Union[CookieUser, None] = Cookie(default=None),
              db: Session = Depends(get_db)):
    return show_All(id_extract(user), db)

@task_router.get("/tareas/{category}")
def filter_category(category, user: Union[CookieUser, None] = Cookie(default=None),
                    db: Session = Depends(get_db)):
    return show_Tasks(category, id_extract(user), db)

@task_router.post("/tareas/")
def add_Task(task: NewTask, user: Union[CookieUser, None] = Cookie(default=None),
             db: Session = Depends(get_db)):
    return create_Task(task, id_extract(user), db)

@task_router.put("/tareas/{id}")
def edit_task(id, category, visibility, user: Union[CookieUser, None] = Cookie(default=None),
              db: Session = Depends(get_db)):
    return change_status(int(id), id_extract(user), category, visibility, db)

@task_router.delete("/tareas/{id}")
def remove_Task(id, user: Union[CookieUser, None] = Cookie(default=None),
                db: Session = Depends(get_db)):
    return delete_Task(int(id), id_extract(user), db)
