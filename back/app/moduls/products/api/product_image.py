from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
#Importamos schemas
from moduls.products.schemas import ProductImageCreate, ProductImageResponse
#Importamos servicios
from moduls.products.services.product_images import (
    add_product_image_service,
    update_position_service,
    delete_product_image_service
)
#Importamos base de datos
from core.database import get_db
#Importamos dependencia para obtener usuario autenticado
from core.dependencies import get_current_user
#Importamos modulo de usuario
from moduls.users.modules import User
#Importamos schema para actualizar posicion
from pydantic import BaseModel
#Schema para actualizar posicion
from moduls.products.schemas import UpdatePosition

router = APIRouter(tags=["ProductImages"])

#Endpoint para añadir imagen o video al producto — protegido solo owners
@router.post("/{product_id}", response_model=ProductImageResponse, status_code=201)
def add_image(
    product_id: str,
    image_data: ProductImageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return add_product_image_service(db, product_id, image_data, current_user.id)

#Endpoint para reordenar imagen en el carrusel — protegido solo owners
@router.patch("/{image_id}/position", response_model=ProductImageResponse)
def update_position(
    image_id: str,
    position_data: UpdatePosition,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_position_service(db, image_id, position_data.position, current_user.id)

#Endpoint para eliminar imagen o video del producto — protegido solo owners
@router.delete("/{image_id}", status_code=204)
def delete_image(
    image_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_product_image_service(db, image_id, current_user.id)