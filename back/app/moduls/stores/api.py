#Importamos ApiRouter y dependencias y excepcion http de fastapi
from fastapi import APIRouter,Depends,HTTPException
#Importamos sesion de la base de datos
from sqlalchemy.orm import Session
#Importamos validadores de datos y la clase de respuesta en los endpoints
from moduls.stores.schemas import CreateStore,StoreResponse,StoresPageResponse,UpdateStore
#Importamos los servicios para ejecutar en los enpoints
from moduls.stores.services import (create_store_service,get_store_by_id_service,get_store_by_name_service,get_stores_service,update_store_service,delete_store_service)
#Importamos la funcion para la conexion correcta a la base de datos
from core.database import get_db


#Router de stores, tambien el tag para ordenar y separar en el swagger
router = APIRouter(tags=["Stores"])

#Enpoint para creacion de tienda 
@router.post("/create",response_model=StoreResponse,status_code=201)
def create_store(store: CreateStore,db: Session = Depends(get_db)):
    #Try para ejecutar el metodo service para crear la tienda
    try:
        #Retornamos el metodo y le pasamos el parametro que contiene la conexion a la base de datos y los datos recibidos de la tienda
        return create_store_service(db,store)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    
#Enpoint que muestra todas las tiendas disponibles
@router.get("/",response_model=StoresPageResponse)
def get_stores(skip: int= 0,limit: int= 20,db: Session = Depends(get_db)):
    #Ejectuamos el servicio que nos retorna todas las tiendas
    try:
        return get_stores_service(db,skip=skip,limit=limit)
    except ValueError as e:
        #Mostramos el error
        raise HTTPException(status_code=400,detail=str(e))

#Enpoint para recibir datos de la tienda segun el identificador
@router.get("/{store_id}",response_model=StoreResponse)
def get_store_by_id(store_id: str, db: Session = Depends(get_db)):
    #Ejecutamos el metodo
    try:
        return get_store_by_id_service(db,store_id)
    except ValueError as e:
        #Mensaje con detalle del error, tienda no encontrada
        raise HTTPException(status_code=404,detail=str(e))
    
#Enpoint para buscar tienda segun nombre de la tienda
@router.get("/search",response_model=StoreResponse)
def get_store_by_name(name: str,db: Session = Depends(get_db)):
    #Try para ejecutar el servicio
    try:
        return get_store_by_name_service(db,name)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))
    
#Endpoint para eliminar/desactivar tienda
@router.delete("/{store_id}",response_model=StoreResponse,status_code=200)
def delete_store(store_id: str ,db: Session= Depends(get_db)):
    #Ejecutamos el metodo para desactivar/eliminar tienda 
    try:
        return delete_store_service(db,store_id)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    
#Enpoint para actualizar tienda
@router.put("/{store_id}",response_model=StoreResponse)
def update_store(store_id: str,store_data: UpdateStore, db: Session = Depends(get_db)):
    #Ejecutamos el metodo service para actualizar datos de tienda
    try:
        return update_store_service(db,store_id,store_data)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))