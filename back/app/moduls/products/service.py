# Importamos todos los métodos del repositorio
from moduls.products.repository import *

# Método para crear producto
def create_product_service(db, product_data: dict) :

    # Validamos que el precio no sea negativo
    if product_data.price < 0:
        raise ValueError(
            "Le prix du produit ne peut pas être négatif."
        )

    # Validamos precio sospechoso (mínimo 10 DZ)
    if product_data.price < 10:
        raise ValueError(
            "Le prix du produit est trop bas. "
            "Le minimum autorisé est de 10 DZ."
        )

    # Asignamos un límite máximo de precio (500 000 DZ)
    if product_data.price > 500000:
        raise ValueError(
            "Le prix du produit dépasse le plafond autorisé. "
            "Le prix maximum est de 500 000 DZ."
        )

    # Verificamos el valor del stock
    if product_data.stock < 1:
        raise ValueError(
            "La quantité en stock doit être au moins égale à 1."
        )

    # Validamos que tenga al menos una imagen o vídeo
    if product_data.image is None:
        raise ValueError(
            "Au moins une image ou un média visuel est requis "
            "pour créer un produit."
        )

    # Creamos el producto
    return create_product(db, product_data)

#Metodo para crear variantes del producto
def create_product_variants_service(db,product_id: str,product_variant: dict) :
    pass
