from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum
import re


class UserRole(str, Enum):
    admin = "admin"
    owner = "owner"
    customer = "customer"


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: UserRole

    # Validacion de username
    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        value = value.strip()

        # no espacios internos raros
        if " " in value:
            raise ValueError("Username cannot contain spaces")

        # solo letras, números y _
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError("Username can only contain letters, numbers and underscores")

        return value

    # Validacion de la contraseña que tengo formato correcto
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")

        return value