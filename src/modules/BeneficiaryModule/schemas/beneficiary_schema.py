from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BeneficiaryBase(BaseModel):
    person_type: Optional[str]
    document_type: Optional[str]
    document_number: Optional[str]
    company_name: Optional[str]
    cellphone: Optional[str]
    email: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    status: Optional[str]
    active: Optional[int] = 1
    departament: Optional[int]
    municipality: Optional[int]
    vereda: Optional[str]
    ubication: Optional[str]
    consecutive_number_home: Optional[str]
    process: Optional[str]
    dateOfNotification: Optional[str]
    valorSubsidio: Optional[str]

class BeneficiaryCreate(BeneficiaryBase):
    pass

class BeneficiaryUpdate(BeneficiaryBase):
    pass

class BeneficiaryResponse(BeneficiaryBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
