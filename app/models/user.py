from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy.orm import relationship, backref

from app.database import Base

user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
    PrimaryKeyConstraint('user_id', 'role_id')
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    is_active = Column(Boolean, default=True)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    hashed_password = Column(String)

    roles = relationship("Role", secondary=user_role, backref=backref('users'))
