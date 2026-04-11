#Importamos libreria que se encarga de cargar las variables 
from dotenv import load_dotenv
import os

#Cargamos el archivo .env
load_dotenv()

#Variables de configuracion
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
DATABASE_URL = os.getenv("DATABASE_URL")