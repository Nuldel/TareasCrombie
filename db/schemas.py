from pydantic import BaseModel
from typing import Optional

class newTask(BaseModel):
    title: str
    description: Optional[str]
    status: str = 'Problemas'

    class Config:
        orm_mode = True

class status(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_status

    @classmethod
    def validate_status(cls, status: str) -> str:
        if not isinstance(status, str):
            raise TypeError('Se requiere string')
        if not status in ['Problemas', 'Trabajando', 'Listo']:
            raise ValueError(f"Opción inválida: {status}")
        return status
