from fastapi import APIRouter, Depends, Cookie, Response
from sqlalchemy.orm import Session
from db.schemas import NewUser, LoginUser
from db.repository.user import add_user, check_in

user_router = APIRouter()

# creamos una dependencia de la BBDD para poder reemplazarla en los tests
# (inyeccion de dependencias)
@user_router.post("/usuarios/registrar/")
def register(newUser: NewUser, user: Union[CookieUser, None] = Cookie(default=None),
             db: Session = Depends(get_db)):
    return add_user(newUser, (user != None), db)

@user_router.post("/usuarios/entrar")
def login(loginUser: LoginUser, user: Union[CookieUser, None] = Cookie(default=None),
          db: Session = Depends(get_db), response: Response):
    cookieUser = check_in(loginUser, (user != None), db)
    response.set_cookie(key="user", value=cookieUser)
    return cookieUser

@user_router.post("/usuarios/salir")
def logout(user: Union[CookieUser, None] = Cookie(default=None), response: Response):
    response.set_cookie(key="user", value=None)
    return {"OK", 200}
