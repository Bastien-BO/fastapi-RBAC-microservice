from sqlalchemy import Table, ForeignKey, Column

from app.database import Base

role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True),
)
