from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship

# Declaracion de clase base (buena practica)
@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, nullable=False)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__

# Los modelos que forman el esquema de la BBDD
class User(Base):
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(72), nullable=False)
    ownership = relationship("Task")

class Task(Base):
    title = Column(String(50), nullable=False)
    description = Column(String(500))
    status = Column(Enum('Problemas', 'Trabajando', 'Listo', name='Estado'), nullable=False)
    visibility = Column(Enum('Público', 'Privado', name='Visibilidad'), nullable=False)
    owner = Column(Integer, ForeignKey('User.id'))
#    collabs = relationship("User", secondary=association_table)

#association_table = Table('association', Base.metadata,
#    Column('left_id', ForeignKey('left.id'), primary_key=True),
#    Column('right_id', ForeignKey('right.id'), primary_key=True)
#)
