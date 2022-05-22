from fastapi import FastAPI
from core.config import settings
from db.session import engine
from db.tables import Base
from routers.task_handlers import task_router
from routers.user_handlers import user_router

# creamos tablas en base al esquema farbicado en db/
def create_tables():
    Base.metadata.create_all(bind=engine)

# empezamos la app
def start_app():
    taskApp = FastAPI(tittle=settings.PROJECT_NAME)
    create_tables()
    # las rutas se manejan por separado
    taskApp.include_router(task_router)
    taskApp.include_router(user_router)
    return taskApp

taskApp = start_app()
