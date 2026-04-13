from sqlalchemy import Column, String, ForeignKey, Text, Numeric, Integer,DateTime,Boolean,Enum
from sqlalchemy.orm import relationship
from core.database import Base
import uuid
#Importamos fecha
from datetime import datetime,timezone
#Importamos enum
import enum

#Clase para controlar estado del pedido (delivred,pending,confiremed,cancelled,returned)
class ProductStatus(enum.Enum):
    active = "active"                  
    pending = "pending"              
    out_of_stock = "out_of_stock"      
    discontinued = "discontinued"    

#Tabla completa de productos,relacion uno a muchos entre imagenes y Productimage para carrusel
class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    price = Column(Numeric(10, 2), nullable=False)

    store_id = Column(String(36), ForeignKey("stores.id"), nullable=False)

    store = relationship("Store", back_populates="products")

    #Columna para activar/desactivar el producto
    is_active = Column(Boolean,default=True)

    #Columna para fecha de eliminacion
    deleted_at = Column(DateTime,nullable=True)

    #Columna relacion con la clase de estado del producto
    status = Column(Enum(ProductStatus),nullable=False,default=ProductStatus.active)
    
    #Columna para registrar ultima fecha de modificacion
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))  

    # Relación con imágenes
    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete"
    )

    # Relación con variantes (tallas, colores)
    variants = relationship(
        "ProductVariant",
        back_populates="product",
        cascade="all, delete"
    )

#Tabla variante de productos
class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Campos para variantes
    size = Column(String(50), nullable=True)      
    color = Column(String(50), nullable=True)
    stock = Column(Integer, default=0)

    #Precio por variante
    price = Column(Numeric(10,2),nullable=True)
    
    sku = Column(String(100), unique=True, nullable=True)

    # Relación con producto
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    product = relationship("Product", back_populates="variants")


#Tabla de productos relacionada con la tabla de productos para contener muchas imagenes
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    image_url = Column(String(255), nullable=False)

    #Tipo de objeto (puede ser video o imagen),por defecto imagen
    media_type = Column(String(255),default="image") 
    
    # orden del carrusel
    position = Column(Integer, default=0)

    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)

    product = relationship("Product", back_populates="images")