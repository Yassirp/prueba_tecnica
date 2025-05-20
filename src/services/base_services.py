from typing import Type, TypeVar, List, Optional, Dict, Any
from repositories.base_repository import BaseRepository
from pydantic import ValidationError

Model = TypeVar("Model")
CreateSchema = TypeVar("CreateSchema")
UpdateSchema = TypeVar("UpdateSchema")

class BaseService:
    def __init__(self, model: Type[Model], repository_cls: Type[BaseRepository], create_schema: Type[CreateSchema], update_schema: Type[UpdateSchema]):
        self.model = model
        self.repo: BaseRepository = repository_cls
        self.create_schema = create_schema
        self.update_schema = update_schema

    def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Model]:
        return self.repo.get_all(
            limit=limit,
            offset=offset,
            order_by=order_by,
            filters=filters
        )
        
    def get_all_with_relationships(self, limit: int = 10, offset: int = 0, order_by: str = 'asc', filters: dict = None):
        items = self.repo.get_all_with_relationships(limit, offset, order_by, filters)
        return items

    def get_by_id(self, entity_id: int) -> Optional[Model]:
        return self.repo.get_by_id(entity_id)

    def create(self, data: dict) -> Model:
        try:
            # Validamos los datos usando el esquema de creación
            validated_data = self.create_schema.model_validate(data, context={'db': self.repo.db})
        except ValidationError as ve:
            # Extraemos el primer mensaje de error
            error_messages = [err['msg'] for err in ve.errors()]
            # Enviar el mensaje fuera del campo 'error'
            raise Exception({
                "error": str(ve),  # Mantener la traza técnica del error
                "message": error_messages[0]  # Primer mensaje amigable (puedes personalizar para varios mensajes)
            })

        # Si los datos son válidos, realizamos la creación en el repositorio
        return self.repo.create(validated_data.model_dump())

    def update(self, entity_id: int, data: dict) -> Model:
        try:
            # Validamos los datos usando el esquema de actualización
            validated_data = self.update_schema.model_validate(data, context={'db':  self.repo.db, 'id': entity_id})
        except ValidationError as ve:
            # Extraemos el primer mensaje de error
            error_messages = [err['msg'] for err in ve.errors()]
            # Enviar el mensaje fuera del campo 'error'
            raise Exception({
                "error": str(ve),  # Mantener la traza técnica del error
                "message": error_messages[0]  # Primer mensaje amigable
            })

        # Si los datos son válidos, realizamos la actualización en el repositorio
        return self.repo.update(entity_id, validated_data.model_dump(exclude_unset=True))

    def delete(self, entity_id: int) -> bool:
        entity = self.repo.get_by_id(entity_id)
        if not entity:
            return False
        self.repo.delete(entity.id)
        return True
