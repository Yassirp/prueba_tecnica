# Archivo generado automáticamente para entity_documents - services
import json
from datetime import datetime
from collections import defaultdict
from fastapi import HTTPException, status, Request
from typing import List, Optional, Dict, Any,Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import selectinload, joinedload, aliased
from sqlalchemy.orm import selectinload
from src.app.modules.attributes_module.models.attributes import Attribute
from src.app.modules.attributes_module.services.attributes_service import AttributeService
from src.app.modules.entity_documents_module.models.entity_documents import EntityDocument
from src.app.modules.entity_documents_module.schemas.entity_documents_schemas import EntityDocumentOut
from src.app.modules.entity_types_module.services.entity_type_service import EntityTypeService
from src.app.modules.projects_module.models.projects import Project
from src.app.modules.projects_module.services.projects_service import ProjectService
from src.app.shared.bases.base_service import BaseService
from src.app.modules.entity_types_module.repositories.entity_types_repository import (
    EntityTypeRepository,
)
from src.app.shared.constants.attribute_and_parameter_enum import AttributeIds, ParameterIds, AttributeName
from src.app.shared.constants.project_enum import Setting
from src.app.shared.utils.utils import upload_base64_to_s3_with_structure
from src.app.modules.entity_document_logs_module.services.entity_document_logs_service import EntityDocumentLogsService
from src.app.modules.notifications_module.services.notifications_service import NotificationsService
from src.app.modules.entity_documents_module.schemas.entity_documents_schemas import EntityDocumentBase


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
        self.notification_service = NotificationsService(db_session)
        self.entity_document_log_service = EntityDocumentLogsService(db_session)


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
        search: Optional[str] = None,
        request: Optional[Request] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            document_status = aliased(Attribute)
            document_types = aliased(Attribute)
            project = aliased(Project)

            is_project = None
            is_department = None
            is_municipality = None
            is_region = None

            if request and hasattr(request.state, "query_params"):
                query_params = request.state.query_params
                if isinstance(query_params, dict):  # por si usas dict directamente
                    is_project = query_params.get("project_id")
                    is_department = query_params.get("department_id")
                    is_municipality = query_params.get("municipality_id")
                    is_region = query_params.get("region_id")


            stmt = select(self.model).join(
                document_status, self.model.document_status_id == document_status.id
            ).join(
                document_types, self.model.document_type_id == document_types.id
            ).join(
                project, self.model.project_id == project.id
            ).options(
                selectinload(self.model.stages),
                selectinload(self.model.project),
                selectinload(self.model.entity_types),
                selectinload(self.model.document_types),
                selectinload(self.model.document_status),

            ).where(self.model.state == Setting.STATUS.value)
            
            conditions = []

            # ----------------------------------------------------------
            # Seccion de filtros para projectos
            if is_project:
                stmt = stmt.where(self.model.project_id == int(is_project))          

            if is_department:
                stmt = stmt.where(self.model.properties["department_id"].as_integer() == int(is_department))            

            if is_municipality:
                stmt = stmt.where(self.model.properties["municipality_id"].as_integer() == int(is_municipality))            

            if is_region:
                stmt = stmt.where(self.model.properties["region_id"].as_integer() == int(is_region))

            # ----------------------------------------------------------

            # Filtramos por el id:
            if id:
                conditions.append(self.model.id == id)

            # Filtramos por el id del proyecto
            if project_id:
                conditions.append(self.model.project_id == project_id)

            # Filtramos por el estado del documento
            if document_status_id:
                conditions.append(self.model.document_status_id == document_status_id)

            # FIiltramos por el tipo de entidad
            if entity_type_id:
                conditions.append(self.model.entity_type_id == entity_type_id)

            # Filtrampos por la etapa
            if stage_id:
                conditions.append(self.model.stage_id == stage_id)

            # Filtrampos por el tipo de documento
            if document_type_id:
                conditions.append(self.model.document_type_id == document_type_id)


            # Filtro LIKE con búsqueda en document_status.name y document_types.name
            if search:
                search_pattern = f"%{search}%"
                conditions.append(
                    or_(
                        document_status.name.ilike(search_pattern),
                        document_types.name.ilike(search_pattern),
                        project.name.ilike(search_pattern),
                    )
                )
                
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
            if entity_document:
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
            document_type = await self.attribute_service.get_by_id(document_type_id)
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
                    document_type_name=document_type['name']
                )
                return s3_file
        except Exception as e:
            raise e
        
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            file_url = data.get("file_url",None)
            await self._validate_data(data)
            if file_url:  
                new_file_url  = await self._upload_file_to_S3(data)
                data["file_url"] = new_file_url # Asingamos la nueva ruta de S3 del el archivo
            
            # Convertimos el diccionario a un modelo Pydantic
            entity_document = EntityDocumentBase(**data)
            # Usamos dict_for_db para obtener solo los campos que van a la base de datos
            item = await self.repo.create(entity_document.dict_for_db())
            #Creamos el log del la entidad
            data_log = {
                "entity_document_id": item.id,
                "action": "create",
                "before": json.dumps(data, ensure_ascii=False),  # Serializar `data` como JSON
                "observations": "Documento creado",
                "created_by": data.get("created_by"),
            }
            await self.entity_document_log_service.create(data_log)
            #Enviamos el correo de notificación
            await self.notification_service.create_notification_send_email(item.id, data)
            
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

        
    async def check_doocument_status(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            async with self.db_session.begin():
                documents = data.get("documents", None)
                document_status_id = data.get("document_status_id", None)
    
                for id in documents:
                    entity_document = await self.get_by_id(id)
                    if not entity_document:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No se encontró el documento con el id '{id}'.",
                        )
                    if entity_document["document_status_id"] == AttributeIds.APPROVED.value:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"El tipo de documento ya fue aprobado.",
                        )
    
                    # Obtener y modificar la entidad
                    entity_document = await self.db_session.get(EntityDocument, id)
                    entity_document.document_status_id = document_status_id
                    entity_document.updated_at = datetime.utcnow()
    
                    self.db_session.add(entity_document)
                    await self.db_session.flush()  
                    await self.db_session.refresh(entity_document)
    
                    # Actualizar logs
                    model_log, entity_document_log = await self.entity_document_log_service.get_all(
                        entity_document_id=id
                    )
                    if not entity_document_log:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No se encontró el log para el documento con el id '{id}'.",
                        )
    
                    for log in model_log:
                        log.after = json.dumps(data, ensure_ascii=False)
                        self.db_session.add(log)
    
                # Validar el estado
                model_document, document_status = await self.attribute_service.get_all(
                    id=document_status_id,
                    parameter_id=ParameterIds.DOCUMENT_STATUS.value,
                    limit=1
                )
                if not document_status:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No se encontró el estado del documento con el id '{document_status_id}'.",
                    )
                return []
        except Exception as e:
            raise e

        
  
    async def get_group_by_document_status(        
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        document_status_id: Optional[int] = None,
        search: Optional[str] = None,
        request: Optional[Request] = None,
        )-> Tuple[List[Dict[str, Any]], int]:
        try:
            # Alias de cada los modelos
            document_status = aliased(Attribute)
            document_types = aliased(Attribute)

            is_project = None
            is_department = None
            is_municipality = None
            is_region = None

            if request and hasattr(request.state, "query_params"):
                query_params = request.state.query_params
                if isinstance(query_params, dict):  # por si usas dict directamente
                    is_project = query_params.get("project_id")
                    is_department = query_params.get("department_id")
                    is_municipality = query_params.get("municipality_id")
                    is_region = query_params.get("region_id")
                    
            stmt = select(self.model).join(
                document_status, self.model.document_status_id == document_status.id
            ).join(
                document_types, self.model.document_type_id == document_types.id
            ).options(
                selectinload(self.model.document_status),
                selectinload(self.model.document_types),

            ).where(self.model.state == Setting.STATUS.value)

            conditions = []

            # ----------------------------------------------------------
            # Seccion de filtros para projectos
            if is_project:
                stmt = stmt.where(self.model.project_id == int(is_project))          

            if is_department:
                stmt = stmt.where(self.model.properties["department_id"].as_integer() == int(is_department))            

            if is_municipality:
                stmt = stmt.where(self.model.properties["municipality_id"].as_integer() == int(is_municipality))            

            if is_region:
                stmt = stmt.where(self.model.properties["region_id"].as_integer() == int(is_region))

            # ----------------------------------------------------------

            # Filtrampos por el tipo de estado del documento
            if document_status_id:
                conditions.append(self.model.document_status_id == document_status_id)
            
            # Realizamos el like 
            if search:
                conditions.append(or_(
                    document_status.name.ilike(f"%{search}%"),
                    document_types.name.ilike(f"%{search}%")
                ))

            if conditions:
                stmt = stmt.where(and_(*conditions))

            if order_by:
                stmt = stmt.order_by(order_by)

            if offset:
                stmt = stmt.offset(offset)

            if limit:
                stmt = stmt.limit(limit)

            result = await self.db_session.execute(stmt)
            items = result.scalars().all()
            total = len(items)

            # Agrupar por document_status_id
            grouped = defaultdict(lambda: {
                "document_status_id": None,
                "document_status_name": None,
                "documents": []
            })

            for doc in items:
                document = doc.document_status
                grouped[document.id]["document_status_id"] = document.id
                grouped[document.id]["document_status_name"] = document.name
                grouped[document.id]["documents"].append(doc)

            return list(grouped.values()) ,total
        except Exception as e:
            raise e
        

    async def get_count_document_status(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        request: Optional[Request] = None,
        )-> Tuple[List[Dict[str, Any]], int]:
        try:
            # Alias para evitar colisiones
            document_status = aliased(Attribute)
            document_types = aliased(Attribute)

            is_project = None
            is_department = None
            is_municipality = None
            is_region = None

            if request and hasattr(request.state, "query_params"):
                query_params = request.state.query_params
                if isinstance(query_params, dict):  # por si usas dict directamente
                    is_project = query_params.get("project_id")
                    is_department = query_params.get("department_id")
                    is_municipality = query_params.get("municipality_id")
                    is_region = query_params.get("region_id")

            # SELECT document_status_id, COUNT(*) ...
            stmt = select(
                self.model.document_status_id,
                document_status.name.label("document_status_name"),
                func.count(self.model.id).label("count_document")
            ).join(
                document_status, self.model.document_status_id == document_status.id
            ).join(
                document_types, self.model.document_type_id == document_types.id
            ).where(
                self.model.state == Setting.STATUS.value
            ).group_by(
                self.model.document_status_id,
                document_status.name
            )

            # ----------------------------------------------------------
            # Seccion de filtros para projectos
            if is_project:
                stmt = stmt.where(self.model.project_id == int(is_project))          

            if is_department:
                stmt = stmt.where(self.model.properties["department_id"].as_integer() == int(is_department))            

            if is_municipality:
                stmt = stmt.where(self.model.properties["municipality_id"].as_integer() == int(is_municipality))            

            if is_region:
                stmt = stmt.where(self.model.properties["region_id"].as_integer() == int(is_region))

            # ----------------------------------------------------------
            if order_by:
                stmt = stmt.order_by(order_by)

            if offset:
                stmt = stmt.offset(offset)

            if limit:
                stmt = stmt.limit(limit)

            result = await self.db_session.execute(stmt)
            items = result.all()
            total = len(items)

            # Convertir a lista de diccionarios
            response = [
                {
                    "document_status_id": row.document_status_id,
                    "document_status_name": row.document_status_name,
                    "count_document": row.count_document
                }
                for row in items
            ]

            return response, total

        except Exception as e:
            raise e
