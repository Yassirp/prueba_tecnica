from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime

class CountryBase(BaseModel):
    code: str = Field(..., max_length=10, description="Código del país, ej: 'CO'")
    name: str = Field(..., max_length=255, description="Nombre del país")

class CountryCreate(CountryBase):
    pass

class CountryUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=10)
    name: Optional[str] = Field(None, max_length=255)

class CountryOut(CountryBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }
