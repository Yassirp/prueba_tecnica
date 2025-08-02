from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass


class SoftDeleteMixin:
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    @declared_attr.directive
    def __mapper_args__(cls):
        return {
            "confirm_deleted_rows": False
        }

class BaseModel(Base, SoftDeleteMixin):
    __abstract__ = True
