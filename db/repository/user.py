from sqlalchemy.orm import Session
from db.tables import User
from db.schemas import NewUser, LoginUser, CookieUser
from bcrypt import gensalt, hashpw, checkpw

def add_user(newUser: NewUser, is_online: bool, db: Session):
    if is_online:
        raise HTTPException(
            status_code=403,
            detail="Sesión ya iniciada"
        )
    if db.query(User).filter(User.email == newUser.email).first():
        raise HTTPException(
            status_code=403,
            detail="Email ya está registrado"
        )

    bpw = newUser.password.encode('utf-8')
    salt = gensalt()
    hash = hashpw(bpw, salt)

    new_U = User(name = newUser.name,
                 email = newUser.email,
                 password = hash)
    db.add(new_U)
    db.commit()
    db.refresh(new_U)
    return {"OK", 200}

def check_in(loginUser: LoginUser, is_online: bool, db: Session):
    db_user = db.query(User).filter(User.email == loginUser.email).first()
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Email no está registrado"
        )

    bpw = loginUser.password.encode('utf-8')
    salt = gensalt()
    if not checkpw(bpw, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Datos incorrectos"
        )

    cookieUser = CookieUser(id=db_user.id,
                            name=db_user.name,
                            email=db_user.email)
    return cookieUser
