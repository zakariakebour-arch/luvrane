from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from moduls.users.schemas import UserRole,UserCreate
from moduls.users.services import Hola