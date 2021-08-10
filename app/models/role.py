from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship, backref

from app.database import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
