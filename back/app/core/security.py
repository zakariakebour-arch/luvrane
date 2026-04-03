from passlib.context import CryptContext

#Creamos el contexto
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Metodo para hashear contraseñas
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Metodo para verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


