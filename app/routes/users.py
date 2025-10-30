from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = auth_service.register_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Usuário já existe.")
    return new_user

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    token = auth_service.login(db, user)
    if not token:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    return {"access_token": token, "token_type": "bearer"}

