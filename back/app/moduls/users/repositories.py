from sqlalchemy.orm import Session
from moduls.users.modules import User

#Metodo que crea un usuario que nos entra un diccionario como parametro
def create_user(db: Session,user_data: dict):
    user = User(
        **user_data
    )
    db.add(user)
    db.commit()
    db.refrech(user)
    return user

#Metodo que busca usuario segun correo
def get_user_by_email(db: Session,email: str):
    return db.query(User).filter(User.email == email).first()


