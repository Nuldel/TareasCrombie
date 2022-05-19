from sqlalchemy.orm import Session
from .schemas import newTask, status
from .tables import Task
from .session import SessionLocal

def create_Task(task: newTask, db: Session = SessionLocal()):
    new_T = Task(title = task.title,
                 description = task.description,
                 status = task.status)
    db.add(new_T)
    db.commit()
    db.refresh(new_T)
    return new_T

def show_Tasks(category: status, db: Session = SessionLocal()):
    status.validate_status(category)
    return db.query(Task).filter(Task.status == category).all()

def show_All(db: Session = SessionLocal()):
    return db.query(Task).all()

def delete_Task(id: int, db: Session = SessionLocal()):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()
    return 0

def change_status(id: int, category: status, db: Session = SessionLocal()):
    status.validate_status(category)
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.status = category
    db.add(task)
    db.commit()
    db.refresh(task)
    return newTask(title=task.title,
                   description=task.description,
                   status=task.status)
