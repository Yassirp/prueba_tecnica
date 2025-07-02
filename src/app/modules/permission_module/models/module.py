from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,func
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy.orm import relationship
from src.app.modules.permission_module.models.module_actions import ModuleAction

class Module(BaseModel):
    __tablename__ = 'm_modules'

    id = Column(Integer, primary_key=True)
    level = Column(Integer)
    name = Column(String)
    path = Column(String)
    parent_id = Column(Integer)
    active = Column(Boolean)
    position = Column(Integer)
    icon = Column(String)
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)

    module_actions = relationship("ModuleAction", back_populates="module")