from pydantic import BaseModel
from typing import Optional

# clases usadas exclusivamente para corroborar tipos (pydantic)
class newTask(BaseModel):
    title: str
    description: Optional[str]
    status: str = 'Problemas'

    class Config:
        orm_mode = True

# esta clase seria más util si se usara en un atributo de otra clase
class status(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_status

    @classmethod
    def validate_status(cls, status: str) -> str:
        if not status in ['Problemas', 'Trabajando', 'Listo']:
            raise ValueError(f"Opción inválida: {status}")
        return status
