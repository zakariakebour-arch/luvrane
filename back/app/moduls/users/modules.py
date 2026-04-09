from sqlalchemy import Column, String, Boolean, Enum, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime, timezone
import enum
import uuid


class UserRole(enum.Enum):
    admin = "admin"
    owner = "owner"
    customer = "customer"


# Tabla principal de usuarios
class User(Base):
    __tablename__ = "users"

    # ID seguro (no incremental)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Username visible
    username = Column(String(50), unique=True, nullable=False, index=True)

    # Email para login
    email = Column(String(255), unique=True, nullable=False, index=True)

    # Contraseña hasheada
    hashed_password = Column(String(255), nullable=False)

    # Rol del usuario
    role = Column(Enum(UserRole), nullable=False, default=UserRole.customer)

    # Estado de la cuenta
    is_active = Column(Boolean, default=True)

    # Fecha de creacion de la cuenta
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Fecha de ultima modificacion
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    # Fecha de desactivacion de la cuenta
    deleted_at = Column(DateTime, nullable=True)

    # Relacion con direcciones del usuario
    addresses = relationship("UserAddress", back_populates="user", cascade="all, delete")

    # Relacion con carrito del usuario
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete")

    # Relacion con likes del usuario
    likes = relationship("ProductLike", back_populates="user", cascade="all, delete")


# Tabla de direcciones del usuario, un usuario puede tener varias direcciones
class UserAddress(Base):
    __tablename__ = "user_addresses"

    # ID de la direccion
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Relacion con usuario
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="addresses")

    # Calle y numero
    street = Column(String(255), nullable=False)

    # Ciudad
    city = Column(String(100), nullable=False)

    # Wilaya (region)
    wilaya = Column(String(100), nullable=False)

    # Codigo postal
    postal_code = Column(String(20), nullable=True)

    # Indica si es la direccion principal del usuario
    is_default = Column(Boolean, default=False)

    # Fecha de creacion
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# Tabla de carrito, cada fila es un producto en el carrito del usuario
class CartItem(Base):
    __tablename__ = "cart_items"

    # ID del item del carrito
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Relacion con usuario
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="cart_items")

    # Relacion con producto
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    product = relationship("Product")

    # Relacion con variante del producto (talla, color)
    variant_id = Column(String(36), ForeignKey("product_variants.id"), nullable=True)
    variant = relationship("ProductVariant")

    # Cantidad del producto en el carrito
    quantity = Column(Integer, default=1)

    # Fecha en que se añadio al carrito
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# Tabla de likes, cada fila es un like de un usuario a un producto
class ProductLike(Base):
    __tablename__ = "product_likes"

    # ID del like
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Relacion con usuario
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="likes")

    # Relacion con producto
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    product = relationship("Product")

    # Fecha en que se dio like
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))