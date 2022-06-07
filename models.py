"""Database models"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    password_hash = Column(String(128))
    last_login = Column(DateTime)

    sessions = relationship("Sessions", back_populates="user", cascade=False)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, last_login={self.last_login!r}"


class Sessions(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(64), nullable=False)
    expires = Column(DateTime)

    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"Session(id={self.id!r}, expires={self.expires!r}"
