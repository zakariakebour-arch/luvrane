#Importamos repositorio de producto
from moduls.products.repositories.product_repository import get_product_by_id,get_products,get_product_by_name,create_product,update_product,delete_product,get_product_by_name_and_store
#Importamos el metodo de selccion de la tienda
from moduls.stores.repositories import select_store_by_id
#Importamos excepciones
from core.exceptions import ConflictException,NotFoundException,ForbiddenException,ValidationException

#Metodo para crear producto
def create_product_service(db,product_data: dict,current_user_id: str):
    #Comprobamos si la tienda exsiste
    store = select_store_by_id(db,product_data.store_id)

    #Si no exsiste
    if not store:
        raise NotFoundException("Boutique introuvable")

    #Comrobamos si la tienda esta activa
    if not store.is_active:
        raise ForbiddenException("Boutique désactivée")

    #Comprobamos si el usuario es el dueño de la tienda
    if store.owner_id != current_user_id:
        raise ForbiddenException("Accés interdit")
    
    #Comprobamos si en la tienda exsiste un producto con el mismo nombre
    if get_product_by_name_and_store(db, product_data.name, product_data.store_id):
        raise ConflictException("Un produit avec ce nom existe déjà dans cette boutique")

    #Convertimos el producto a diccionario
    product_dict = product_data.model_dump()

    #Creamos el producto
    return create_product(db,product_dict)

#Metodo para obtener producto por identificador
def get_product_by_id_service(db,product_id: str):
    #Comprobamos si el producto exsiste
    product = get_product_by_id(db,product_id)

    #Si el producto no esta disponible
    if not product:
        raise NotFoundException("Le produit est pas disponible")
    
    #Devolvemos el producto
    return product

