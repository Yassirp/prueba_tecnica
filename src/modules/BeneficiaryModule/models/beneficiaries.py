from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from database.base import Base
from sqlalchemy.orm import relationship

class Beneficiary(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_type = Column(String(255), nullable=True)
    document_type = Column(String(255), nullable=True)
    document_number = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    cellphone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    active = Column(Integer, nullable=False, default=1)
    departament = Column(Integer, nullable=True)
    municipality = Column(Integer, nullable=True)
    vereda = Column(String(255), nullable=True)
    ubication = Column(String(255), nullable=True)
    valorSubsidio = Column(String(255), nullable=True)
    consecutive_number_home = Column(String(255), nullable=True)
    process = Column(String(255), nullable=True)
    dateOfNotification = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)



    # diagnostic = relationship("BeneficiaryIntegralDiagnostic", backref="beneficiary", lazy='select')

    # contratos_assignment = relationship(
    #     "ContratoAssignment",
    #     primaryjoin=and_(
    #         foreign(ContratoAssignment.associate_id) == cast(id, String),
    #         ContratoAssignment.associate_to == literal('Beneficiario').collate('utf8mb4_unicode_ci')
    #     ),
    #     viewonly=True
    # )