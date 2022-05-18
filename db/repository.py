from sqlalchemy.orm import Session
from schemas import newTask
from tables import Task

def create_Task(task: newTask, db: Session):
    new_T = Task(title = task.tittle,
                 description = task.description,
                 state = task.state)
    db.add(new_T)
    db.commit()
    db.refresh(new_T)
    return new_T

def show_Tasks(category: str, db: Session):
    pass

def show_All(db: Session):
    pass
