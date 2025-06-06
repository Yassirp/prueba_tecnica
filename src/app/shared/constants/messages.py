class GlobalMessages:
    ERROR_VALIDATION = "Error de validación"
    ERROR_CREATED = "Error al crear el registro"
    ERROR_UPDATED = "Error al actualizar el registro"
    ERROR_DELETED = "Error al eliminar el registro"
    ERROR_GET = "Error al obtener el registro"
    ERROR_GET_ALL = "Error al obtener los registros"
    ERROR_INTERNAL = "Error interno del servidor"
    ERROR_UNAUTHORIZED = "No autorizado"
    ERROR_FORBIDDEN = "Prohibido"
    ERROR_NOT_FOUND = "No encontrado"
    ERROR_METHOD_NOT_ALLOWED = "Método no permitido"
    ERROR_CONFLICT = "Conflicto"
    ERROR_TOO_MANY_REQUESTS = "Demasiadas solicitudes"
    ERROR_UNPROCESSABLE_ENTITY_VALIDATION = (
        "Error de validación en los datos de entrada"
    )


class ProjectsMessages(GlobalMessages):
    OK_GET_ALL = "Proyectos obtenidos correctamente"
    OK_GET = "Proyecto obtenido correctamente"
    OK_CREATED = "Proyecto creado correctamente"
    OK_UPDATED = "Proyecto actualizado correctamente"
    OK_DELETED = "Proyecto eliminado correctamente"
    ERROR_NOT_FOUND = "Proyecto no encontrado"


class EntityTypesMessages(GlobalMessages):
    OK_GET_ALL = "Tipos de entidad obtenidos correctamente"
    OK_GET = "Tipo de entidad obtenido correctamente"
    OK_CREATED = "Tipo de entidad creado correctamente"
    OK_UPDATED = "Tipo de entidad actualizado correctamente"
    OK_DELETED = "Tipo de entidad eliminado correctamente"
    ERROR_NOT_FOUND = "Tipo de entidad no encontrado"


# Parametros 
class ParameterMessages(GlobalMessages):
    OK_GET_ALL = "Parametros obtenidos correctamente"
    OK_GET     = "Parametros obtenidos correctamente"
    OK_CREATED = "Parametro creada correctamente"
    OK_UPDATED = "Parametro actualizado correctamente"
    OK_DELETED = "Parametro eliminado correctamente"


# Atributo
class AttributeMessages(GlobalMessages):
    OK_GET_ALL = "Atributos obtenidos correctamente"
    OK_GET     = "Atributos obtenidos correctamente"
    OK_CREATED = "Atributo creada correctamente"
    OK_UPDATED = "Atributo actualizado correctamente"
    OK_DELETED = "Atributo eliminado correctamente"


# Reglas de documentos 
class DocumentRuleMessages(GlobalMessages):
    OK_GET_ALL = "Reglas de documentos obtenidos correctamente"
    OK_GET     = "Reglas de documentos obtenidos correctamente"
    OK_CREATED = "Reglas de documento creada correctamente"
    OK_UPDATED = "Reglas de documento actualizada correctamente"
    OK_DELETED = "Reglas de documento eliminada correctamente"

# Documentos de entidades
class EntityDocumentMessages(GlobalMessages):
    OK_GET_ALL = "Documentos de entidades obtenidos correctamente"
    OK_GET = "Documentos de entidad obtenido correctamente"
    OK_CREATED = "Documentos de entidad creado correctamente"
    OK_UPDATED = "Documentos de entidad actualizado correctamente"
    OK_DELETED = "Documentos de entidad eliminado correctamente"
    ERROR_NOT_FOUND = "Documentos de entidad no encontrado"

# Logs de documentos
class EntityDocumentLogMessages(GlobalMessages):
    OK_GET_ALL = "Logs de documentos obtenidos correctamente"
    OK_GET     = "Log de documento obtenido correctamente"
    OK_CREATED = "Log de documento creado correctamente"
    OK_UPDATED = "Log de documento actualizado correctamente"
    OK_DELETED = "Log de documento eliminado correctamente"
    ERROR_NOT_FOUND = "Log de documento no encontrado"
    

# Notificaciones
class NotificationMessages(GlobalMessages):
    OK_GET_ALL = "Notificaciones obtenidas correctamente"
    OK_GET     = "Notificación obtenida correctamente"
    OK_CREATED = "Notificación creada correctamente"
    OK_UPDATED = "Notificación actualizada correctamente"
    OK_DELETED = "Notificación eliminada correctamente"
    ERROR_NOT_FOUND = "Notificación no encontrada"


# Login
class LoginMessages(GlobalMessages):
    SUCCESS = "Inicio de session correctamente"
    ERROR = "Inicio de session fallido"


# Logout 

class LogoutMessages(GlobalMessages):
    SUCCESS = "Cerrar session realizado correctamente"
    ERROR = "Cerrar session fallido"