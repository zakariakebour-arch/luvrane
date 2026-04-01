from sqlalchemy import Column, String, ForeignKey, Text, Numeric, Integer
from sqlalchemy.orm import relationship
from core.database import Base
import uuid

#Tabla completa de productos,relacion uno a muchos entre imagenes y Productimage para carrusel
class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    price = Column(Numeric(10, 2), nullable=False)

    store_id = Column(String(36), ForeignKey("stores.id"), nullable=False)

    store = relationship("Store", back_populates="products")

    # Relación con imágenes
    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete"
    )

#Tabla de productos relacionada con la tabla de productos para contener muchas imagenes
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    image_url = Column(String(255), nullable=False)

    # orden del carrusel
    position = Column(Integer, default=0)

    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)

    product = relationship("Product", back_populates="images")