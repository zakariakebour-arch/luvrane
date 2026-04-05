from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

#Clase completa para validacion de entrada y salida de los datos para la creacion de la tienda
class CreateStore(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    photo_profile: Optional[str] = None
    image: Optional[str] = None

    # Validation validacion para el nombre
    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères")
        if len(value) > 255:
            raise ValueError("Le nom ne peut pas dépasser 255 caractères")
        return value

    # Validacion para la descripcion
    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if value is not None and len(value) > 1000:
            raise ValueError("La description ne peut pas dépasser 1000 caractères")
        return value


class StoreResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    photo_profile: Optional[str]
    image: Optional[str]
    products: List = []  

    class Config:
        from_attributes = True