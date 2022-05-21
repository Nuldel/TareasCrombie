from pydantic import BaseModel, EmailStr
from typing import Optional

# clases usadas exclusivamente para corroborar tipos (pydantic)
class NewTask(BaseModel):
    title: str
    description: Optional[str]
    status: str = 'Problemas'
    visibility: str = 'Público'
#    collabs: [int]

    class Config:
        orm_mode = True

class NewUser(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class LoginUser(BaseModel):
    email: str
    password: str

class CookieUser(BaseModel):
    id: int
    name: str
    email: EmailStr

# una funcion separada para validar el status
def validate_status(status: str) -> str:
    if not status in ['Problemas', 'Trabajando', 'Listo']:
        raise ValueError(f"Opción inválida: {status}")
    return status

def validate_visibility(vis: str) -> str:
    if not vis in ['Público', 'Privado']:
        raise ValueError(f"Opción Inválida: {vis}")
    return vis
