from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, String, Enum

# Declaracion de clase base (buena practica)
@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

# (Separar en mas archivos si se agregan mas modelos a la db)
class Task(Base):
    title = Column(String(50))
    description = Column(String(500))
    state = Column(Enum('Problemas', 'Trabajando', 'Listo', name='Estado'))
