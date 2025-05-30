from enum import Enum

class ParameterIds(Enum):
    STAGES = 1 # Etapas
    DOCUMENT_STATUS = 2 # Estados de documentos


class ParameterName(Enum):
    STAGES = "Etapas."
    DOCUMENT_STATUS = "Estados de documentos."


class AttributeIds(Enum):
    DEPARTMENTAL = 1
    REGIONAL = 2
    NATIONAL = 3
    PENDING_APPROVAL = 4 
    APPROVED = 5
    REJECTED = 6


class AttributeIName(Enum):
    DEPARTMENTAL = "Departamental"
    REGIONAL = "Regional"
    NATIONAL = "Nacional"
    PENDING_APPROVAL = "Pndiente de aprobación"
    APPROVED = "Aprobado"
    REJECTED = "Rechazado"
