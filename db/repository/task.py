from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.schemas import NewTask, validate_status, validate_visibility
from db.tables import Task, User
from typing import Union

# funcion chiquita para comprobar el usuario en caso de que la tarea sea privada
def can_see(user_id: Union[int, None], task: Task):
    return task.visibility == "Público" or user_id == task.owner

# Las funciones que manejar los requests
def create_Task(task: NewTask, user_id: Union[int, None], db: Session):
    validate_status(task.status)
    validate_visibility(task.visibility)
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Usuario no autenticado"
        )
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(
            status_code=404,
            detail="Usuario asociado no encontrado"
        )
    new_T = Task(title = task.title,
                 description = task.description,
                 status = task.status,
                 visibility = task.visibility,
                 owner = user_id)
    db.add(new_T)
    db.commit()
    db.refresh(new_T)
    return new_T

def show_Tasks(category: str, user_id: Union[int, None], db: Session):
    validate_status(category)
    return db.query(Task).filter(Task.status == category and can_see(user_id, Task)).all()

def show_All(user_id: Union[int, None], db: Session):
    return db.query(Task).filter(can_see(user_id, Task)).all()

def delete_Task(id: int, user_id: Union[int, None], db: Session):
    task = db.query(Task).filter(Task.id == id).first()

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Usuario no autenticado"
        )
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )
    if not task.owner == user_id:
        raise HTTPException(
            status_code=403,
            detail="Usuario no tiene permitido editar la tarea"
        )

    db.delete(task)
    db.commit()
    return {"OK", 200}

def change_task(id: int, user_id: Union[int, None], category: str, visibility: str, db: Session):
    validate_status(category)
    validate_visibility(visibility)
    task = db.query(Task).filter(Task.id == id).first()

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Usuario no autenticado"
        )
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )
    if not task.owner == user_id:
        raise HTTPException(
            status_code=403,
            detail="Usuario no tiene permitido editar la tarea"
        )

    task.status = category
    task.visibility = visibility
    db.add(task)
    db.commit()
    db.refresh(task)
    return NewTask(title=task.title,
                   description=task.description,
                   status=task.status,
                   visibility=task.visibility)
