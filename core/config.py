import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Organizador de Tareas"

    JWT_KEY: str = "a6646096e9e3fe168b48a50d5b966e164030aabf75a91c989c0ed27c8d47cf90"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_SERVER: str = os.getenv("DB_SERVER", default="localhost")
    DB_PORT: str = os.getenv("DB_PORT", default="5432")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_DIALECT: str = os.getenv("DB_DIALECT", default="postgresql")
    DB_DRIVER: str = os.getenv("DB_DRIVER")
    driver_append = f'+{DB_DRIVER}' if DB_DRIVER != "None" and DB_DRIVER is not None else ''
    DB_URL: str = f"{DB_DIALECT}{driver_append}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

settings = Settings()
