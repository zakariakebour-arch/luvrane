import boto3
import urllib.parse
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#Importamos variables desde config
from core.config import (
    DSQL_ENDPOINT,
    DSQL_PORT,
    DSQL_USER,
    DSQL_DATABASE,
    AWS_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY
)

#En local usamos credenciales del .env
#En App Runner boto3 usa el rol IAM automaticamente
if os.getenv("ENV") == "local":
    boto3.setup_default_session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

#Metodo para generar token IAM temporal para Aurora DSQL
def generate_dsql_token() -> str:
    client = boto3.client("dsql", region_name=AWS_REGION)
    token = client.generate_db_connect_admin_auth_token(
        Hostname=DSQL_ENDPOINT,
        Region=AWS_REGION,
        ExpiresIn=3600
    )
    return token

#Metodo para crear engine con token fresco
def get_engine():
    token = generate_dsql_token()
    encoded_token = urllib.parse.quote_plus(token)

    database_url = (
        f"postgresql+psycopg2://{DSQL_USER}:{encoded_token}"
        f"@{DSQL_ENDPOINT}:{DSQL_PORT}/{DSQL_DATABASE}"
        f"?sslmode=require"
    )

    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=10,
        max_overflow=20
    )

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()