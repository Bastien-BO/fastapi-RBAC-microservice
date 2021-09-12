from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import backref, relationship

from app.database import Base
from app.models.role_permission import role_permission


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    roles = relationship("Role", secondary=role_permission, backref=backref('permissions', lazy=True), lazy='subquery')
