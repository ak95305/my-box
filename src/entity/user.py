from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src import Base
from src.models.user_token import UserToken

class UserEntity(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        user_token = UserToken.getRowUserId(self.id)
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name" : self.last_name,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "token": user_token.to_dict() if user_token else None,
        }