# Archivo generado automáticamente para document_rules - services
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any,Tuple
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, select, func, case, literal_column, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import aliased
from src.app.modules.attributes_module.models.attributes import Attribute
from src.app.modules.attributes_module.services.attributes_service import AttributeService
from src.app.modules.document_rules_module.models.document_rules import DocumentRule
from src.app.modules.document_rules_module.repositories.document_rules_repository import DocumentRuleRepository
from src.app.modules.document_rules_module.schemas.document_rules_schemas import DocumentRuleOut
from src.app.modules.entity_documents_module.models.entity_documents import EntityDocument
from src.app.modules.entity_documents_module.services.entity_documents_service import EntityDocumentService
from src.app.modules.entity_types_module.models.entity_types import EntityType
from src.app.modules.entity_types_module.services.entity_type_service import EntityTypeService
from src.app.modules.projects_module.services.projects_service import ProjectService
from src.app.shared.constants.attribute_and_parameter_enum import AttributeIds, ParameterIds
from src.app.shared.bases.base_service import BaseService
from src.app.shared.constants.project_enum import EntityTypeIds, Setting

class DocumentRuleService(BaseService[DocumentRule, DocumentRuleOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=DocumentRule,
            repository_cls=DocumentRuleRepository,
            db_session=db_session,
            out_schema=DocumentRuleOut,
        )
        self.db_session=db_session
        self.project_service = ProjectService(db_session)
        self.entity_type_service = EntityTypeService(db_session)
        self.attribute_service = AttributeService(db_session)  
        self.entity_service = EntityDocumentService(db_session)  
    
    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        entity_type_id: Optional[int] = None,
        document_type_id: Optional[int] = None,
        stage_id: Optional[int] = None,
        project_id: Optional[int] = None,
        id: Optional[int] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            stmt = select(self.model).options(
                selectinload(self.model.project),
                selectinload(self.model.document_types),
                selectinload(self.model.stages),
                selectinload(self.model.entity_types),
                )
            conditions = []
            
            # filtramos por el id
            if id:
                conditions.append(self.model.id == id)
        
            # Filtramos por el tipo de entidad
            if entity_type_id:
                conditions.append(self.model.entity_type_id == entity_type_id)
            
            # Filtramos por tipo de documento
            if document_type_id:
                conditions.append(self.model.document_type_id == document_type_id)
            
            # Filtramos por etapa
            if stage_id: 
                conditions.append(self.model.stage_id == stage_id)

            # Filtramos por proyecto
            if project_id:
                conditions.append(self.model.project_id == project_id)

            # Filtramos por el tipo de documentop¡
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
        

    async def _validate_data(self, data, is_update=False, document_rule_id=None):
        try:
            project_id = data.get("project_id")
            entity_type_id = data.get("entity_type_id")
            document_type_id = data.get("document_type_id")
            stage_id = data.get("stage_id")
            
            # Validamos si existe el proyecto
            project = await self.project_service.get_by_id(project_id)
            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el proyecto con el id '{project_id}'.",
            )
            
            # Validamos el tipo de entidad
            entity_type = await self.entity_type_service.get_by_id(entity_type_id)
            if not entity_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el tipo de entidad con el id '{entity_type_id}'.",
            )

            # Validamos el tipo de documento
            data, document_type = await self.attribute_service.get_all(id=document_type_id, parameter_id=ParameterIds.TYPE_DOCUMENT.value)
            if not document_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el tipo de documento con el id '{document_type_id}'.",
            )
            
            # Validamos la etapa
            data, stage = await self.attribute_service.get_all(id=stage_id, parameter_id=ParameterIds.STAGES.value)
            if not stage:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró la etapa con el id '{stage_id}'.",
            )  

            # Validamos si la regla ya existe con estos parametros
            data, validate_rules = await self.get_all(stage_id=stage_id, project_id=project_id, entity_type_id=entity_type_id, document_type_id=document_type_id, limit=1)
            if is_update and document_rule_id:
                for rule in data:
                    if rule.id != document_rule_id:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Ya existe una regla con estos parametros.",
                    )
            else:
                if validate_rules:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Ya existe una regla con estos parametros.",
                ) 

            return True
        except Exception as e:
            raise e
        

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            await self._validate_data(data)
            item = await self.repo.create(data)
            return self.out_schema.model_validate(item).model_dump()
        except Exception as e:
            raise e
        
    
    async def update(
        self, document_rule_id: int, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        try:
            await self._validate_data(data, True, document_rule_id)

            item = await self.repo.update(document_rule_id, data)
            if not item: return None
            return self.out_schema.model_validate(item).model_dump()
        except Exception as e:
            raise e
        

    async def validate_user(self, user_id):
        try:
            print("validate_user: ",user_id)
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El id del estudiante es requerido.",
                )
            
            model, count = await self.entity_service.get_all(entity_id=user_id)
            if not count:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró el usuario con id '{user_id}'.",
            )
            return True
        except Exception as e:
            raise e

    async def get_document_students(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        key: Optional[str] = None,
        user_id: Optional[int] = None,
        entity_type_id: Optional[int] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            med = aliased(EntityDocument)
            med_base = aliased(EntityDocument)
            mdr = aliased(DocumentRule)
            met = aliased(EntityType)
            ma = aliased(Attribute)
            mat = aliased(Attribute)  # Estado del documento (si lo necesitas)
            

            await self.validate_user(user_id=user_id)

            stmt = (
                select(
                mdr.project_id,
                mdr.document_type_id,
                mdr.entity_type_id,
                mdr.stage_id,
                ma.name,
                func.max(func.coalesce(med.updated_at, med.created_at)).label("last_updated"),
                case(
                    (func.count(med.id) > 0, literal_column("'SÍ'")),
                    else_=literal_column("'NO'")
                ).label("exists"),
                case(
                    (mat.name == None, literal_column("'Por cargar'")),
                    else_=mat.name
                ).label("document_status_name")
            )
            .select_from(mdr)
            # INNER JOIN por tuplas exactas
            .join(
                med_base,
                and_(
                    mdr.project_id == med_base.project_id,
                    mdr.document_type_id == med_base.document_type_id,
                    mdr.entity_type_id == med_base.entity_type_id,
                    mdr.stage_id == med_base.stage_id
                )
            )
            # LEFT JOIN con filtros adicionales
            .outerjoin(
                med,
                and_(
                    med.id == med_base.id,
                    (med.state == Setting.STATUS.value) | (med.state == None),
                    med.document_status_id != AttributeIds.CANCEL.value,
                    med.entity_id == user_id
                )
            )
            .join(met, met.id == mdr.entity_type_id)
            .join(ma, ma.id == mdr.document_type_id)
            .outerjoin(mat, mat.id == med.document_status_id)
            .where(mdr.entity_type_id == EntityTypeIds.SPORTSMAN.value)
                .group_by(
                    mdr.project_id,
                    mdr.document_type_id,
                    mdr.entity_type_id,
                    mdr.stage_id,
                    ma.name,
                    met.name,
                    mat.name
                )
            )

            if offset:
                stmt = stmt.offset(offset)

            if limit:
                stmt = stmt.limit(limit)

            if order_by:
                stmt = stmt.order_by(order_by)

            result = await self.db_session.execute(stmt)
            rows = result.mappings().all()  # Para obtener dicts por columna

            total = len(rows)
            return rows, total
        except Exception as e:
            raise e
