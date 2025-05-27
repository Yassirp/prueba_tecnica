from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Type, TypeVar, List, Optional, Dict, Any, Generic, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.modules.parameters_module.models.parameters import Attribute, Parameter
from src.app.modules.parameters_module.repositories.attribute_repository import AttributeRepository
from src.app.modules.parameters_module.repositories.parameters_repository import ParameterRepository
from src.app.modules.parameters_module.schemas.parameters_schemas import AttributeOut, ParameterOut
from src.app.shared.bases.base_service import BaseService

class ParameterService(BaseService[Parameter, ParameterOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Parameter,
            repository_cls=ParameterRepository,
            db_session=db_session,
            out_schema=ParameterOut,
        )