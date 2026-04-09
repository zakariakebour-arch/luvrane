#Importamos sesion
from sqlalchemy.orm import Session
#Importamos todas las clases de tablas del modelo de usurio
from moduls.users.modules import *

#Metodo que crea un usuario que nos entra un diccionario como parametro
def create_user(db: Session,user_data: dict) -> dict:
    user = User(
        **user_data
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#Metodo para guardar direcciones de usuario 
def create_directions(db: Session,direction_data: dict) -> dict:
    direction = UserAddress(
        **direction_data
    )
    db.add(direction)
    db.commit()
    db.refresh(direction)
    return direction

#Metodo para listar direcciones del usuario
def get_directions(db: Session) -> list:
    #Realizamos la consulta
    return db.query(UserAddress).all()

#Creamos metodo para modificar direccion
def update_direction(db: Session,user_adress: UserAddress,direction_data: dict) -> UserAddress:
    for field,value in direction_data.items():
       if value is not None:
           setattr(user_adress,field,value)
    
    db.commit()
    db.refresh(user_adress)

    return user_adress

#Metodo eliminar direccion
def delete_direction(db: Session,direction_id: str) -> UserAddress:
    #Hacemos una consulta a la base de datos para la direccion exacta segun el identificador
    direction = db.query().filter_by(UserAddress.id == direction_id)

    #Eliminamos la direccion segun el identificador recibido
    db.delete(direction)
    db.commit()
    return direction

#Metodo para crear una lista de productos guardados por like
def like_products():
    pass


