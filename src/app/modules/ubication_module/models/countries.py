from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from src.app.shared.bases.base_model import BaseModel

class Country(BaseModel):
    __tablename__ = "countries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(10), unique=True, nullable=False)  # Ej: 'CO', 'US'
    name = Column(String(255), nullable=False)              # Ej: 'Colombia', 'United States'
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
