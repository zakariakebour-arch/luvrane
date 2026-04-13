#Importamos repositorio de imagenes de producto
from moduls.products.repositories.product_imgages import add_product_image,delete_product_image,update_image_position
#Importamos metodo de respositorio de tienda
from moduls.stores.repositories import Store

#Metodo para agregar imagenes al producto o video
def add_product_image_service(db,product_id,image_data):
    #Comprobamos si el usuario es el propietario de la tienda
    pass