from sqlalchemy import Table, Column, Integer, ForeignKey, PrimaryKeyConstraint

from app.database import Base
from app.models.role import Role

user_role = Table('user_role', Base.metadata,
                  Column('user_id', Integer, ForeignKey('user.id')),
                  Column('role_id', Integer, ForeignKey(Role.id)),
                  PrimaryKeyConstraint('user_id', 'role_id')
                  )
