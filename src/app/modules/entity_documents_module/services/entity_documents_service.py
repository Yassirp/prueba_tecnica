# Archivo generado automáticamente para entity_documents - services
from datetime import datetime
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any,Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.orm import selectinload
from src.app.modules.attributes_module.services.attributes_service import AttributeService
from src.app.modules.entity_documents_module.models.entity_documents import EntityDocument
from src.app.modules.entity_documents_module.schemas.entity_documents_schemas import EntityDocumentOut
from src.app.modules.entity_types_module.services.entity_type_service import EntityTypeService
from src.app.modules.projects_module.services.projects_service import ProjectService
from src.app.shared.bases.base_service import BaseService
from src.app.modules.entity_types_module.repositories.entity_types_repository import (
    EntityTypeRepository,
)
from src.app.shared.constants.attribute_and_parameter_enum import AttributeIds, ParameterIds
from src.app.shared.utils.utils import upload_base64_to_s3_with_structure

class EntityDocumentService(BaseService[EntityDocument, EntityDocumentOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=EntityDocument,
            repository_cls=EntityTypeRepository,
            db_session=db_session,
            out_schema=EntityDocumentOut,
        )

        self.db_session=db_session
        self.project_service = ProjectService(db_session)
        self.attribute_service = AttributeService(db_session)
        self.entity_type_service = EntityTypeService(db_session)

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        project_id: Optional[int] = None,
        document_status_id: Optional[int] = None,
        entity_type_id: Optional[int] = None,
        stage_id: Optional[int] = None,
        document_type_id: Optional[int] = None,
        id:  Optional[int] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            stmt = select(self.model).options(
                selectinload(self.model.stages),
                selectinload(self.model.project),
                selectinload(self.model.entity_types),
                selectinload(self.model.document_types),
                selectinload(self.model.document_status),
                )
            conditions = []
            
            # Filtramos por el id:
            if id:
                conditions.append(self.model.id == id)

            # Filtramos por el id del proyecto
            if project_id:
                conditions.append(self.model.project_id == project_id)

            # Filtramos por el estado del documento
            if document_status_id:
                conditions.append(self.model.document_status_id == document_status_id)

            # FIiltramos por el tipo de etapa
            if entity_type_id:
                conditions.append(self.model.entity_type_id == entity_type_id)

            # Filtrampos por la etapa
            if stage_id:
                conditions.append(self.model.stage_id == stage_id)

            # Filtrampos por el tipo de documento
            if document_type_id:
                conditions.append(self.model.document_type_id == document_type_id)

            # Aplicar condiciones al query
            if conditions:
                stmt = stmt.where(and_(*conditions))
             
            # Aquí puedes aplicar filtros, orden y paginación si los necesitas.
            if order_by:
                stmt = stmt.order_by(order_by)

            if offset:
                stmt = stmt.offset(offset)
            
            if limit:
                stmt = stmt.limit(limit)

            result = await self.db_session.execute(stmt)
            items = result.scalars().all()

            # Opcional: Si tienes filtros aplicados en SQL puedes contar antes,
            # si no, simplemente haces len().
            total = len(items)
            return items, total
        except Exception as e:
            raise e
        

    async def _validate_data(self, data, is_update=False, entity_document_id=None):
        try:
            project_id = data.get("project_id")
            document_type_id = data.get("document_type_id")
            entity_type_id = data.get("entity_type_id")
            stage_id = data.get("stage_id")
            document_status_id = data.get("document_status_id")

            # Validamos si existe el proyecto
            project = await self.project_service.get_by_id(project_id)
            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el proyecto con el id '{project_id}'.",
            )

            # Validamos el tipo de documento
            data, document_type = await self.attribute_service.get_all(id=document_type_id, parameter_id=ParameterIds.TYPE_DOCUMENT.value)
            if not document_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el tipo de documento con el id '{document_type_id}'.",
            )

            # Validamos el tipo de entidad
            entity_type = await self.entity_type_service.get_by_id(entity_type_id)
            if not entity_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el tipo de entidad con el id '{entity_type_id}'.",
            )

            # Validamos la etapa
            data, stage = await self.attribute_service.get_all(id=stage_id, parameter_id=ParameterIds.STAGES.value)
            if not stage:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró la etapa con el id '{stage_id}'.",
            ) 

            # Validamos el estado del documento
            data, document_status = await self.attribute_service.get_all(id=document_status_id, parameter_id=ParameterIds.DOCUMENT_STATUS.value)
            if not document_status:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el estado del documento con el id '{document_status_id}'.",
            )

            data, entity_document = await self.get_all(project_id=project_id, entity_type_id=entity_type_id, stage_id=stage_id, document_type_id=document_type_id)
            if data:
                for rules in data:
                    if rules.document_status_id == AttributeIds.APPROVED.value:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Ya existe un tipo de documento en estado aprobado para esta entidad.",
                        )
                    else:
                        rules.document_status_id = AttributeIds.CANCEL.value
                        rules.updated_at = datetime.utcnow() 

                        # Guardar (con SQLAlchemy async ORM)
                        self.db_session.add(rules)
                        await self.db_session.commit()
                        await self.db_session.refresh(rules)

            return True
        except Exception as e:
            raise e


    async def _upload_file_to_S3(self, data):
        try:
            file_url = data.get("file_url",None)
            project_id = data.get("project_id",None)
            document_type_id = data.get("document_type_id",None)
            entity_type_id = data.get("entity_type_id",None)
            stage_id = data.get("stage_id",None)
            entity_id = data.get("entity_id")

            # Consultamos los servicios
            project = await self.project_service.get_by_id(project_id)
            entity_type = await self.entity_type_service.get_by_id(entity_type_id)
            stage = await self.attribute_service.get_by_id(stage_id)

            if file_url: 
                s3_file = upload_base64_to_s3_with_structure(
                    base64_data=file_url,  # cadena base64
                    environment="production",
                    project_name=project['name'],
                    entity_type_name=entity_type['name'],
                    stage_name=stage['name'],
                    entity_id=entity_id,
                    document_type_id=document_type_id,
                    document_type_name="contrato"
                )
                print("Ruta s3: ",s3_file)
        except Exception as e:
            raise e
        
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            file_url = data.get("file_url",None)
            await self._validate_data(data)
            if file_url:  
                new_file_url  = await self._upload_file_to_S3(data)
                data["file_url"] = new_file_url # Asingamos la nueva ruta de S3 del el archivo

            item = await self.repo.create(data)
            return self.out_schema.model_validate(item).model_dump()
        except Exception as e:
            raise e
        

    async def update(
        self, entity_document_id: int, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        try:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Metodo no disponible.",
            )
        except Exception as e:
            raise e
        

    async def check_doocument_status(self, entity_document_id: int, 
        data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        try:
            document_status_id = data.get("document_status_id")
            model, entity_document = await self.get_all(id=entity_document_id,limit=1)
            for rules in model:
                data, document_status = await self.attribute_service.get_all(id=document_status_id, parameter_id=ParameterIds.DOCUMENT_STATUS.value, limit=1)
                if not document_status:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No se encontró el estado del documento con el id '{document_status_id}'.",
                )

                if rules.document_status_id == AttributeIds.APPROVED.value:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"El tipo de documento ya fue aprobado.",
                    )
                else:
                    rules.document_status_id = document_status_id
                    rules.updated_at = datetime.utcnow() 

                    # Guardar (con SQLAlchemy async ORM)
                    self.db_session.add(rules)
                    await self.db_session.commit()
                    await self.db_session.refresh(rules)

            return []
        except Exception as e:
            raise e