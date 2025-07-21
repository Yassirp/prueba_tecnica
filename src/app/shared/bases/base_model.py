from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, DateTime
from datetime import datetime

# 1. Base declarativa limpia
class Base(DeclarativeBase):
    pass

# 2. Mixin para SoftDelete
class SoftDeleteMixin:
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    @declared_attr.directive
    def __mapper_args__(cls):
        return {
            "confirm_deleted_rows": False
        }

# 3. Modelo base que usarás para tus entidades
class BaseModel(Base, SoftDeleteMixin):
    __abstract__ = True
