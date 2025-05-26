# SQLAlchemy ORM models

from sqlalchemy import Column, Integer, String, Date, UUID
from BackendService.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)