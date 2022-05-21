from fastapi import APIRouter, Depends, Cookie, Response
from sqlalchemy.orm import Session
from db.schemas import NewUser, LoginUser
from db.repository.user import add_user, check_in
from db.session import get_db
from typing import Union

user_router = APIRouter()

# creamos una dependencia de la BBDD para poder reemplazarla en los tests
# (inyeccion de dependencias)
@user_router.post("/usuarios/registrar/")
def register(newUser: NewUser, user_id: Union[int, None] = Cookie(default=None),
             db: Session = Depends(get_db)):
    return add_user(newUser, (user_id != None), db)

@user_router.post("/usuarios/entrar")
def login(response: Response, loginUser: LoginUser, user_id: Union[int, None] = Cookie(default=None),
          db: Session = Depends(get_db)):
    cookieUser = check_in(loginUser, (user_id != None), db)
    response.set_cookie(key="user_id", value=cookieUser.id)
    return cookieUser

@user_router.post("/usuarios/salir")
def logout(response: Response, user_id: Union[int, None] = Cookie(default=None)):
    response.delete_cookie("user_id")
    return {"OK", 200}
