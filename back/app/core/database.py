from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexion a aurora DSQL
DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/marketplace"

#Conexion base
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

#Cada peticion usa una conexion y autocommit desactivado
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#Base para modelos ORM
Base = declarative_base()


#Dependencia para FastAPI para usar en los enpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()