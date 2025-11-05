from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user_schema import (
    UserCreate, UserLogin, UserResponse,
    ForgetPasswordRequest, ResetPasswordRequest
)
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

@router.post("/forgot-password")
def forgot_password(request: ForgetPasswordRequest, db: Session = Depends(get_db)):
    token = auth_service.request_password_reset(db, request.email)
    if not token:
        raise HTTPException(status_code=404, detail="Email não encontrado.")
    return {"message": "Token para redefinição gerado", "token": token}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    success = auth_service.reset_password(db, request.token, request.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado.")
    return {"message": "Senha redefinida com sucesso!"}

