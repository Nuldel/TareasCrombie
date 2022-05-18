import os
from dotenv import load_dotenv
from pathlib import Path

crombie_path = Path('.')/'.crombie1'
load_dotenv(dotenv_path=crombie_path)

class Settings:
    PROJECT_NAME: str = "Organizador de Tareas"
    PROJECT_VERSION: str = "1.0.0"

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_SERVER: str = os.getenv("DB_SERVER")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

settings = Settings()
