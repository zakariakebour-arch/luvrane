#Importamos todos los metodos de repositories de sotore
from moduls.stores.repositories import (create_store,select_store_by_id,select_stores)

#Metodo para crear tienda 
def create_store_service(db,store_data):
    #Validamos que cumpla el nombre de la tienda la longitud correcta
    if len(store_data.name < 2):
        raise ValueError("Lu nom du magasin est trop court")
    
    #Comprobamos que el nombre de la tienda no sea exsistente en el sistema, para ello usamos el metodo que selecciona todas las tiendas y comparamos
    exsisting_store_name = select_stores()

   