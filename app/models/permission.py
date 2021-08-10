from sqlalchemy import Column, Integer, String, Table, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import backref, relationship

from app.database import Base

role_permission = Table(
    'role_permission',
    Base.metadata,
    Column('permission_id', Integer, ForeignKey('permissions.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
    PrimaryKeyConstraint('permission_id', 'role_id')
)


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    roles = relationship("Role", secondary=role_permission, backref=backref('permissions'))
