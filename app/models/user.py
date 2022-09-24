from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship, backref

from app.database import Base
from app.models.user_role import user_role


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    is_active = Column(Boolean, default=True)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, unique=True, nullable=False)

    roles = relationship(
        "Role",
        secondary=user_role,
        backref=backref("user", lazy=True),
        lazy="subquery",
    )
