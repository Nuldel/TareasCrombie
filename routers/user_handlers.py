from fastapi import APIRouter, Depends, Cookie, Response
from sqlalchemy.orm import Session
from db.schemas import NewUser, LoginUser
from db.repository.user import add_user, check_in
from db.session import get_db
from typing import Union
from core.config import settings
from jose import jwt
from datetime import datetime, timedelta, timezone

user_router = APIRouter()

# verificar si hay una sesion valida
def validate_token(token: Union[str, None]):
    if not token:
        return False
    try:
        data = jwt.decode(token, settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        response.delete_cookie("token")
    return True

# crear token a partir de datos
def create_access_token(data: dict):
    expire_time = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expire_time
    data.update({"exp": expire})
    return jwt.encode(data, settings.JWT_KEY, algorithm=settings.JWT_ALGORITHM)

# creamos una dependencia de la BBDD para poder reemplazarla en los tests
# (inyeccion de dependencias)
@user_router.post("/usuarios/registrar/")
def register(newUser: NewUser, token: Union[str, None] = Cookie(default=None),
             db: Session = Depends(get_db)):
    return add_user(newUser, validate_token(token), db)

@user_router.post("/usuarios/entrar")
def login(response: Response, loginUser: LoginUser, token: Union[str, None] = Cookie(default=None),
          db: Session = Depends(get_db)):
    cookieUser = check_in(loginUser, validate_token(token), db)
    token = create_access_token(vars(cookieUser))
    response.set_cookie(key="token", value=token)
    return cookieUser

@user_router.post("/usuarios/salir")
def logout(response: Response, token: Union[str, None] = Cookie(default=None)):
    response.delete_cookie("token")
    return {"OK", 200}
