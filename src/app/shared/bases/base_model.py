from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_mixin
from datetime import datetime

class BaseModel(DeclarativeBase):
    pass



@declarative_mixin
class SoftDeleteMixin:
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    @declared_attr
    def __mapper_args__(cls):
        return {
            "eager_defaults": True
        }