from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from src.app.shared.bases.base_model import BaseModel

class Department(BaseModel):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country_code = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
