from sqlalchemy import Column, String, ForeignKey, Text, Numeric, Integer, DateTime, Boolean, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base
import uuid
from datetime import datetime, timezone
import enum

# Clase para controlar estado del producto
class ProductStatus(enum.Enum):
    active = "active"
    pending = "pending"
    out_of_stock = "out_of_stock"
    discontinued = "discontinued"

# Tabla completa de productos
class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    price = Column(Numeric(10, 2), nullable=False)

    store_id = Column(String(36), ForeignKey("stores.id"), nullable=False)
    store = relationship("Store", back_populates="products")

    # Columna para activar/desactivar el producto
    is_active = Column(Boolean, default=True)

    # Columna para fecha de eliminacion
    deleted_at = Column(DateTime, nullable=True)

    # Columna relacion con estado del producto
    status = Column(Enum(ProductStatus), nullable=False, default=ProductStatus.active)

    # Columna para registrar ultima fecha de modificacion
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    # Relación con imágenes
    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete"
    )

    # Relación con variantes
    variants = relationship(
        "ProductVariant",
        back_populates="product",
        cascade="all, delete"
    )

    # Relación con opciones del producto (Color, Talla, etc)
    options = relationship(
        "ProductOption",
        back_populates="product",
        cascade="all, delete"
    )

# Tabla variante de productos
class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Stock de la variante
    stock = Column(Integer, default=0)

    # Precio por variante
    price = Column(Numeric(10, 2), nullable=True)

    # SKU único de la variante
    sku = Column(String(100), unique=True, nullable=False, index=True)

    # Firma única de la combinación (MUY IMPORTANTE)
    signature = Column(String(255), unique=True, index=True, nullable=False)

    # Relación con producto
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    product = relationship("Product", back_populates="variants")

    # Relación con valores de la variante
    values = relationship(
        "VariantValue",
        back_populates="variant",
        cascade="all, delete"
    )

    # Columna para estado de la variante
    is_active = Column(Boolean, default=True)

    # Fecha creación
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Fecha actualización
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))

# Clase Opciones de producto (Color, Talla, etc)
class ProductOption(Base):
    __tablename__ = "product_options"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)

    # Nombre de la opcion
    name = Column(String(50), nullable=False)

    # Relación con producto
    product = relationship("Product", back_populates="options")

    # Relación con valores
    values = relationship(
        "ProductOptionValue",
        back_populates="option",
        cascade="all, delete"
    )

# Clase Valores de opcion del producto (Rojo, M, etc)
class ProductOptionValue(Base):
    __tablename__ = "product_option_values"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    option_id = Column(String(36), ForeignKey("product_options.id"), nullable=False)

    # Valor de la opcion
    value = Column(String(50), nullable=False)

    # Relación con opción
    option = relationship("ProductOption", back_populates="values")

# Tabla intermedia variante - valores
class VariantValue(Base):
    __tablename__ = "variant_values"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    variant_id = Column(String(36), ForeignKey("product_variants.id"), nullable=False)

    option_value_id = Column(String(36), ForeignKey("product_option_values.id"), nullable=False)

    # Relación con variante
    variant = relationship("ProductVariant", back_populates="values")

    # Relación con valor de opción
    option_value = relationship("ProductOptionValue")

    # Evitar duplicados de la misma combinación
    __table_args__ = (
        UniqueConstraint("variant_id", "option_value_id"),
    )

# Tabla de imagenes de productos
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    image_url = Column(String(255), nullable=False)

    # Tipo de media
    media_type = Column(String(255), default="image")

    # Orden del carrusel
    position = Column(Integer, default=0)

    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)

    # Relación con producto
    product = relationship("Product", back_populates="images")