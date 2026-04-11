from moduls.users.repositories.user_repository import (
    get_user,
    get_user_by_email,
    get_user_by_username,
    create_user,
    delete_user,
    update_user
)
# Importamos metodo para hashear contraseña desde el archivo security
from core.security import hash_password, verify_password   
# Importamos excepciones
from core.exceptions import (
    ConflictException,
    AppException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    ValidationException
)

# Metodo para crear usuario
def create_user_service(db, user_data):
    # Comprobamos que el email no exista ya
    if get_user_by_email(db, user_data.email):
        raise ConflictException("Cet email est déjà utilisé")      

    # Comprobamos que el username no exista ya
    if get_user_by_username(db, user_data.username):
        raise ConflictException("Ce nom d'utilisateur est déjà utilisé")  

    # Convertimos a diccionario
    user_dict = user_data.model_dump()

    # Hasheamos la contraseña y eliminamos la original del diccionario
    user_dict["hashed_password"] = hash_password(user_dict.pop("password"))

    return create_user(db, user_dict)

#Metodo para acceso de usuario
def login_services(db,user_data):
    #Seleccionamos usuario segun correo
    if not get_user_by_email(user_data.email):
        raise NotFoundException("Utilisateur inexistant")
    
    #Si esta registrado en el sistema
    