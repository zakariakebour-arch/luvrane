from passlib.context import CryptContext

pwd_context = CryptContext(schemas=["brycpt"],deprecated="auto")

#Metodo para hashear contraseñas
def hash_password(password: str):
    return pwd_context.hash(password)

#Metodo para verificar contraseña
def verify_password(plain_password: str,hashed_password: str):
    return pwd_context.verify(plain_password,hashed_password)