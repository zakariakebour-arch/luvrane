#Importamos el modelo de productos con todas las tablas
from moduls.products.modules import (Product,ProductImage,ProductVariant)
#Importamos ORM con la sesion
from sqlalchemy.orm import Session
#Importamos fecha
from datetime import datetime,timezone

#Creamos el metodo que se encarga de insertar los datos del producto creado
def create_product(db: Session,product_data: dict) -> dict:
    product = Product(
        **product_data
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

#Metodo para listar todos los productos
def get_products(db: Session,skip: int=0,limit: int=20) -> dict:
    #Total de productos para paginacion
    total = db.query(Product).count()

    #productos a mostrar con paginacion
    products = db.query(Product).offset(skip).limit(limit).all()

    #Devolvemos resultado total y los productos
    return {"total":total,"products":products}

#Metodo para seleccionar producto segun su identificador
def get_product_by_id(db: Session,product_id: str):
    #Hacemos la consulta y devolvemos resultado
    return db.query(Product).filter(Product.id == product_id).first()

#Metodo para buscar producto segun nombre
def get_product_by_name(db: Session,product_name: str):
    #Hacemos la consulta segun el nombre
    return db.query(Product).filter(Product.name == product_name).first()
 
#Metodo para eliminar producto
def delete_product(db: Session,product: Product )-> Product:
    #Lo desactivamos
    product.is_active = False
    product.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(product)
    #Devolvemos el producto
    return product

#Metodo para actualizar el producto en la base de datos
def update_product(db: Session,product: Product,product_data: dict) -> Product:
    for field,value in product_data.items():
        if value is not None:
            setattr(product,field,value)

    #Insertamos la fecha en la que se realizo la ultima modificacion del producto
    product.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(product)
    #Devolvemos el producto
    return product


# Parte para la tabla imagenes relacionados con los productos

# Añadir imagen a producto
def add_product_image(db: Session, product_id: str, image_data: dict) -> ProductImage:
    image = ProductImage(**image_data, product_id=product_id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

# Eliminar imagen concreta
def delete_product_image(db: Session, image_id: str) -> None:
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if image:
        db.delete(image)
        db.commit()

# Reordenar imagenes del carrusel
def update_image_position(db: Session, image_id: str, position: int) -> ProductImage:
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if image:
        image.position = position
        db.commit()
        db.refresh(image)
    return image

#Parte para la tabla de variantes del producto

# Añadir variante a producto
def add_product_variant(db: Session, product_id: str, variant_data: dict) -> ProductVariant:
    variant = ProductVariant(**variant_data, product_id=product_id)
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant

# Actualizar stock de variante
def update_variant_stock(db: Session, variant_id: str, stock: int) -> ProductVariant:
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if variant:
        variant.stock = stock
        db.commit()
        db.refresh(variant)
    return variant

# Eliminar variante
def delete_product_variant(db: Session, variant_id: str) -> None:
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if variant:
        db.delete(variant)
        db.commit()