from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.schemas import newTask, validate_status
from db.tables import Task

# Las funciones que manejar los requests
def create_Task(task: newTask, db: Session):
    validate_status(task.status)
    new_T = Task(title = task.title,
                 description = task.description,
                 status = task.status)
    db.add(new_T)
    db.commit()
    db.refresh(new_T)
    return new_T

def show_Tasks(category: str, db: Session):
    validate_status(category)
    return db.query(Task).filter(Task.status == category).all()

def show_All(db: Session):
    return db.query(Task).all()

def delete_Task(id: int, db: Session):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()
    return {"OK", 200}

def change_status(id: int, category: str, db: Session):
    validate_status(category)
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = category
    db.add(task)
    db.commit()
    db.refresh(task)
    return newTask(title=task.title,
                   description=task.description,
                   status=task.status)
