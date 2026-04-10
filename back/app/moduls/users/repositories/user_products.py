#Importamos sesion
from sqlalchemy.orm import Session
#Importamos la clase de la tabla de products deseables
from moduls.users.modules import ProductLike

#Metodo para crear una lista de productos guardados por like
def like_products(db: Session,product_id: str) -> ProductLike:
    #Pasamos el identificador del producto
    list_products = ProductLike(
        product_id
    )
    db.add(list_products)
    db.commit()
    db.refresh(list_products)
    return list_products

#Metodo para eliminar producto favorito
def delete_product(db: Session,product_id: str) -> ProductLike:
    #Eliminamos el producto de la lista segun el identificador(lo seleccionado)
    product = db.query(ProductLike).filter(ProductLike.id == product_id).first()

    db.delete(product)
    db.commit()
    return product