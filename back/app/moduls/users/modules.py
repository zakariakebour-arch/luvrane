from sqlalchemy import Column, String, Boolean, Enum
from core.database import Base
import enum
import uuid


class UserRole(enum.Enum):
    admin = "admin"
    owner = "owner"
    customer = "customer"


class User(Base):
    __tablename__ = "users"

    # ID seguro (no incremental)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # username visible
    username = Column(String(50), unique=True, nullable=False, index=True)

    # email para login
    email = Column(String(255), unique=True, nullable=False, index=True)

    # contraseña hasheada
    hashed_password = Column(String(255), nullable=False)

    # rol del usuario
    role = Column(Enum(UserRole), nullable=False, default=UserRole.customer)

    # estado
    is_active = Column(Boolean, default=True)


    