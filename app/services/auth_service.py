from sqlalchemy.orm import Session
from app.models.users import User, PasswordReset
from app.schemas.user_schema import UserCreate, UserLogin
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class AuthService:

    def register_user(self, db: Session, user: UserCreate):
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            return None

        hashed_pw = hash_password(user.password)
        new_user = User(email=user.email, password_hash=hashed_pw)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def login(self, db: Session, user: UserLogin):
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user or not verify_password(user.password, db_user.password_hash):
            return None

        token = jwt.encode({"sub": db_user.email}, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def request_password_reset(self, db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None

        token = PasswordReset.generate_token()
        reset_entry = PasswordReset(
            user_id=user.id,
            token=token,
            expires_at=PasswordReset.expiration_time()
        )

        db.add(reset_entry)
        db.commit()
        return token

    def reset_password(self, db: Session, token: str, new_password: str):
        reset_entry = db.query(PasswordReset).filter(PasswordReset.token == token).first()

        if not reset_entry or reset_entry.expires_at < datetime.utcnow():
            return False

        user = db.query(User).filter(User.id == reset_entry.user_id).first()
        user.password_hash = hash_password(new_password)

        db.delete(reset_entry)
        db.commit()
        return True
