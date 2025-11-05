from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    reset_tokens = relationship("PasswordReset", back_populates="user")


class PasswordReset(Base):
    __tablename__ = "password_reset"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="reset_tokens")

    @staticmethod
    def generate_token():
        return str(uuid.uuid4())

    @staticmethod
    def expiration_time():
        return datetime.utcnow() + timedelta(minutes=30)
