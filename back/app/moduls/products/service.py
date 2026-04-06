#Importamos todos los metodos en repostorio
from moduls.products.repository import *

#Metodo para crear producto
def create_product_service(db,product_data: dict):
    #Validamos precio sospechoso minimo 10 DZ
    if product_data.price < 10:
        raise ValueError("Le prix est trop bas. Le minimum autorisé est 10 DZ.")
    #Comprobamos que el precio no sea negativo
    elif product_data.price < 0:
        raise ValueError("Le prix ne peut pas être négatif")
    
    