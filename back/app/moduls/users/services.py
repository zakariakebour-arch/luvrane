#Importamos repositorio 
from moduls.users.repositories import create_user, get_user_by_email
#Importamos los metodos de seguridad para hashear y validar la contraseña 
from core.security import hash_password, verify_password

#Logica del metodo para registrar usuario
def register_user_service(db, user_data):
    # comprobar email duplicado
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("Cet email est déjà utilisé")

    # hash password
    hashed_password = hash_password(user_data.password)

    user_dict = user_data.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]

    return create_user(db, user_dict)

#Logica para acceso a la cuenta de usuario
def login_user_service(db, email: str, password: str):
    #Metodo que selecciona el usuario segun el email que lo hemos pasado como parametro
    user = get_user_by_email(db, email)

    #Si no es correcto el correo 
    if not user:
        raise ValueError("Email ou mot de passe incorrect")

    #Si no es inválida la contraseña
    if not verify_password(password, user.hashed_password):
        raise ValueError("Email ou mot de passe incorrect")

    #Si todo correcto retornamos el usuario 
    return user