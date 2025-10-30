from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.user_schema import UserCreate, UserLogin
from passlib.context import CryptContext
from jose import jwt
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"

class AuthService:
    def register_user(self, db: Session, user: UserCreate):
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            return None

        hashed_pw = pwd_context.hash(user.password)
        new_user = User(email=user.email, password_hash=hashed_pw)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def login(self, db: Session, user: UserLogin):
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
            return None

        token = jwt.encode({"sub": db_user.email}, SECRET_KEY, algorithm=ALGORITHM)
        return token
