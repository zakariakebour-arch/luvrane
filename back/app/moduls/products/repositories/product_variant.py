#Importamos tabla de producto variante
from moduls.products.modules import ProductVariant
#Importamos sesion
from sqlalchemy.orm import Session

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

#Metodo para seleccionar producto por identificador
def get_product_variant_by_id(db: Session,variant_id: str) -> ProductVariant:
    #Devolvemos la consulta
    return db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()

