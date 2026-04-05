#Importamos el modelo de productos con todas las tablas
from moduls.products.modules import (Product,ProductImage,ProductVariant)
#Importamos ORM con la sesion
from sqlalchemy.orm import Session

#Creamos el metodo que se encarga de insertar los datos del producto creado
def create_product(db: Session,product_data: dict) -> dict:
    product = Product(
        **product_data
    )
    db.add()
    db.refresh(product)
    db.commit()
    return product


