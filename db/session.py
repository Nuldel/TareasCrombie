from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Crear la abstraccion de db de sqlalchemy para reducir la dependencia de
# una db en particular
engine = create_engine(settings.DB_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
