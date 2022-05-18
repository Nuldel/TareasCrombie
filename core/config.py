import os
from dotenv import load_dotenv
from pathlib import Path

crombie_path = Path('.')/'.env'
load_dotenv(dotenv_path=crombie_path)

class Settings:
    PROJECT_NAME: str = "Organizador de Tareas"

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_SERVER: str = os.getenv("DB_SERVER", default="localhost")
    DB_PORT: str = os.getenv("DB_PORT", default="5432")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_DIALECT: str = os.getenv("DB_DIALECT", default="postgresql")
    DB_DRIVER: str = os.getenv("DB_DRIVER")
    DB_URL: str = f"{DB_DIALECT}{f'+{DB_DRIVER}' if DB_DRIVER is not None else ''}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

settings = Settings()
