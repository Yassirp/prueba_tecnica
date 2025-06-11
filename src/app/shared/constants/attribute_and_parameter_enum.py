from enum import Enum

class ParameterIds(Enum):
    STAGES = 1 # Etapas
    DOCUMENT_STATUS = 2 # Estados de documentos
    TYPE_DOCUMENT = 3 # TIPO DE DOCUMENTO
    NOTIFICATION_TYPE = 4 # TIPO DE NOTIFICACION

class ParameterName(Enum):
    STAGES = "Etapas."
    DOCUMENT_STATUS = "Estados de documentos."
    TYPE_DOCUMENT = "Tipo de documento."
    NOTIFICATION_TYPE = "Tipo de notificación."

class AttributeIds(Enum):
    DEPARTMENTAL = 1
    REGIONAL = 2
    NATIONAL = 3
    PENDING_APPROVAL = 4 
    APPROVED = 5
    REJECTED = 6
    DOCUMENT_TYPE_PHOTO = 7
    IDENTITY_DOCUMENT = 8
    INFORMED_CONSENT = 9
    CERTIFICATION_EDUCATIONAL_INSTITUTION  = 10
    CERTIFICATION_EPS_OR_SISBEN = 11
    CERTIFICATE_LABOR = 12
    CERTIFICATE_EPS = 13
    CERTIFICATE_ARL = 14
    CERTIFICATE_MEDIAL = 15
    CONSENT_INFORMED = 16
    CERTIFICATE_CRIMES = 17
    OTHERS = 18
    CANCEL = 19
    MESSAGE_NOTIFICATION = 20
    CREATED_NOTIFICATION = 21
    UPDATED_NOTIFICATION = 22


class AttributeName(Enum):
    DEPARTMENTAL = "Departamental"
    REGIONAL = "Regional"
    NATIONAL = "Nacional"
    PENDING_APPROVAL = "Por revisar"
    APPROVED = "Aprobado"
    REJECTED = "Rechazado"
    DOCUMENT_TYPE_PHOTO = "Foto tipo documento"
    IDENTITY_DOCUMENT = "Documento de identidad"
    INFORMED_CONSENT = "Consentimiento Informado"
    CERTIFICATION_EDUCATIONAL_INSTITUTION  = "Certificación del establecimiento educativo firmada por el rector"
    CERTIFICATION_EPS_OR_SISBEN = "Certificación de afiliación con estado activo de la EPS o SISBEN"
    CERTIFICATE_LABOR = "Certificación laboral o contractual vigente con la entidad"
    CERTIFICATE_EPS = "Certificación de afiliación a la EPS"
    CERTIFICATE_ARL = "Certificación de afiliación a la ARL"
    CERTIFICATE_MEDIAL = "Certificación de aptitud médica"
    CONSENT_INFORMED = "Consentimiento informado para mayores de edad"
    CERTIFICATE_CRIMES = "Certificación de consulta de inhabilidades (Delitos sexuales cometidos contra menores de 18 años"
    OTHERS = "RETHUS - Solo Aplica para Medicos - Fisioterapeutas"
    CANCEL = "Documentos anulados"
    MESSAGE_NOTIFICATION = "Mensaje de notificación"
    CREATED_NOTIFICATION = "Documento cargado correctamente"
    UPDATED_NOTIFICATION = "Documento actualizado correctamente"








