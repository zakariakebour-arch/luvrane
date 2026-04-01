from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db

from moduls.users.schemas import UserCreate, UserLogin, UserResponse
from moduls.users.services import register_user_service, login_user_service

router = APIRouter(tags=["Users"])


# REGISTER
@router.post("/users", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user_service(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# LOGIN
@router.post("/auth/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        user = login_user_service(db, data.email, data.password)

        # ⚠️ por ahora devolvemos usuario (luego JWT)
        return {
            "message": "Connexion réussie",
            "user_id": user.id
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))