from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime, timezone
import enum
import uuid

#Estados del pedido
class OrderStatus(enum.Enum):
    pending = "pending"           
    confirmed = "confirmed"       
    preparing = "preparing"      
    shipped = "shipped"           
    delivered = "delivered"       
    cancelled = "cancelled"       
    returned = "returned"  
           
#Tabla principal de pedidos
class Order(Base):
    __tablename__ = "orders"

    #Identificador del pedido
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    #Relacion con el usuario que realiza el pedido
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    #Relacion con la direccion de envio
    address_id = Column(String(36), ForeignKey("user_addresses.id"), nullable=False)
    address = relationship("UserAddress")

    #Estado del pedido
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.pending)

    #Precio total del pedido
    total_price = Column(Numeric(10, 2), nullable=False)

    #Notas del pedido (instrucciones especiales)
    notes = Column(String(500), nullable=True)

    #Relacion con los items del pedido
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

    #Fecha de creacion del pedido
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    #Fecha de ultima modificacion
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    #Fecha de entrega
    delivered_at = Column(DateTime, nullable=True)

    #Fecha de cancelacion
    cancelled_at = Column(DateTime, nullable=True)

#Tabla de items del pedido
class OrderItem(Base):
    __tablename__ = "order_items"

    #Identificador del item
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    #Relacion con el pedido
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="items")

    #Relacion con el producto
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    product = relationship("Product")

    #Relacion con la variante del producto
    variant_id = Column(String(36), ForeignKey("product_variants.id"), nullable=True)
    variant = relationship("ProductVariant")

    #Cantidad del producto
    quantity = Column(Integer, nullable=False)

    #Precio unitario en el momento del pedido
    unit_price = Column(Numeric(10, 2), nullable=False)

    #Precio total del item
    total_price = Column(Numeric(10, 2), nullable=False)