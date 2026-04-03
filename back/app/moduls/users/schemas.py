from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum
import re


class UserRole(str, Enum):
    admin = "admin"
    owner = "owner"
    customer = "customer"

#Clase que valida la creacion de usuario
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: UserRole
    bag: int
    
    # Validacion de username
    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        value = value.strip()

        # no espacios internos raros
        if " " in value:
            raise ValueError("Le nom d'utilisateur ne peut pas contenir d'espaces")

        # solo letras, números y _
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError("Le nom d'utilisateur ne peut contenir que des lettres, des chiffres et des underscores")

        return value

    # Validacion de la contraseña que tengo formato correcto
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Le mot de passe doit contenir au moins une lettre majuscule")

        if not re.search(r"[a-z]", value):
            raise ValueError("Le mot de passe doit contenir au moins une lettre minuscule")

        if not re.search(r"[0-9]", value):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Le mot de passe doit contenir au moins un caractère spécial")

        return value
