from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional, List
from decimal import Decimal

#Validacion de imagen de producto
class ProductImageBase(BaseModel):
    image_url: HttpUrl
    position: int = 0

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageResponse(ProductImageBase):
    id: str

    class Config:
        from_attributes = True

#Clase para validar toda la informacion del producto
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)

    # Validation pour le nom
    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Le nom du produit doit contenir au moins 2 caractères")
        if len(value) > 255:
            raise ValueError("Le nom du produit ne peut pas dépasser 255 caractères")
        return value

    # Validation pour le prix
    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Le prix doit être supérieur à 0")
        return value


class ProductCreate(ProductBase):
    store_id: str
    images: Optional[List[ProductImageCreate]] = []


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is not None:
            value = value.strip()
            if len(value) < 2:
                raise ValueError("Le nom du produit doit contenir au moins 2 caractères")
            if len(value) > 255:
                raise ValueError("Le nom du produit ne peut pas dépasser 255 caractères")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Le prix doit être supérieur à 0")
        return value


class ProductResponse(ProductBase):
    id: str
    store_id: str
    images: List[ProductImageResponse] = []

    class Config:
        from_attributes = True

