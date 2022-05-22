from fastapi import APIRouter, Depends, Cookie, Response
from db.repository.task import create_Task, show_Tasks, show_All, delete_Task, change_task
from sqlalchemy.orm import Session
from db.schemas import NewTask, CookieUser
from db.session import get_db
from typing import Union
from core.config import settings
from jose import jwt

task_router = APIRouter()

# obtener el id del usuario en caso de haber una sesion valida
def user_id(token: Union[str, None], response: Response):
    if not token:
        return None
    try:
        data = jwt.decode(token, settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        response.delete_cookie("token")
        return None
    return data.get("id")

# creamos una dependencia de la BBDD para poder reemplazarla en los tests
# (inyeccion de dependencias)
@task_router.get("/tareas")
def fetch_all(response: Response, token: Union[str, None] = Cookie(default=None),
              db: Session = Depends(get_db)):
    return show_All(user_id(token, response), db)

@task_router.get("/tareas/{category}")
def filter_category(response: Response, category, token: Union[str, None] = Cookie(default=None),
                    db: Session = Depends(get_db)):
    return show_Tasks(category, user_id(token, response), db)

@task_router.post("/tareas/")
def add_Task(response: Response, task: NewTask, token: Union[str, None] = Cookie(default=None),
             db: Session = Depends(get_db)):
    return create_Task(task, user_id(token, response), db)

@task_router.put("/tareas/{id}")
def edit_task(response: Response, id, category, visibility, token: Union[str, None] = Cookie(default=None),
              db: Session = Depends(get_db)):
    return change_task(int(id), user_id(token, response), category, visibility, db)

@task_router.delete("/tareas/{id}")
def remove_Task(response: Response, id, token: Union[str, None] = Cookie(default=None),
                db: Session = Depends(get_db)):
    return delete_Task(int(id), user_id(token, response), db)
