from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey,func
from src.app.shared.bases.base_model import BaseModel
from sqlalchemy.orm import relationship

class ModuleAction(BaseModel):
    __tablename__ = 'c_modules_actions'

    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey('m_modules.id'))
    action_id = Column(Integer, ForeignKey('m_actions.id'))
    created_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False)
