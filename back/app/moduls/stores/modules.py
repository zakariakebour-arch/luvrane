from sqlalchemy import Column, String, ForeignKey,Text,Numeric
from sqlalchemy.orm import relationship
from core.database import Base
import uuid


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # precio en dinares argelinos
    price = Column(Numeric, nullable=False)

    # relación con tienda
    store_id = Column(String(36), ForeignKey("stores.id"), nullable=False)

    store = relationship("Store", back_populates="products")

    #relación con imágenes
    images = relationship("ProductImage", back_populates="product", cascade="all, delete")