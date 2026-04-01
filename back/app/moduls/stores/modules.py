from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from core.database import Base
import uuid


class Store(Base):
    __tablename__ = "stores"

    #Identificador de la tienda
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    #Nombre de la tienda
    name = Column(String(255), nullable=False)

    #Descripcion de la tienda
    description = Column(Text, nullable=True)
    
    #Tipo de tienda, no puede ser nulo
    type = Column(String(100),nullable=False)
    
    #foto de perfil de la tienda
    photo_profile = Column(String(255),nullable=True)

    #Foto rectangular extra de la tienda 
    image = Column(String(255),nullable=True)

    #Relacion con la tabla productos
    products = relationship("Product", back_populates="store")





