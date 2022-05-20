from pydantic import BaseModel
from typing import Optional

# clases usadas exclusivamente para corroborar tipos (pydantic)
class newTask(BaseModel):
    title: str
    description: Optional[str]
    status: str = 'Problemas'

    class Config:
        orm_mode = True

# una funcion separada para validar el status
def validate_status(status: str) -> str:
    if not status in ['Problemas', 'Trabajando', 'Listo']:
        raise ValueError(f"Opción inválida: {status}")
    return status
