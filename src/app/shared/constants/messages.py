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
