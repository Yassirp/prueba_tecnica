from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.app.modules.parameters_module.models.parameters_values import ParameterValue
from src.app.modules.parameters_module.models.parameters import Parameter
from src.app.shared.bases.base_repository import BaseRepository


class ParameterValueRepository(BaseRepository[ParameterValue]):
    def __init__(self, model: type[ParameterValue], db_session: AsyncSession):
        super().__init__(model, db_session)

    async def get_by_parameter_name(self, name: str):
        stmt = (
            select(self.model)
            .join(self.model.getParameter)
            .filter(Parameter.name.ilike(f"%{name}%"))
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_parameter_references(self, references: list[str]):
        stmt = (
            select(self.model)
            .join(self.model.getParameter)
            .filter(Parameter.key.in_(references))
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_parent_id(self, parent_id: int):
        stmt = select(self.model).filter(self.model.parent_id == parent_id)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_parent_ids(self, parent_ids: list[int]):
        stmt = select(self.model).filter(self.model.parent_id.in_(parent_ids))
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_parameter_reference(self, reference: str):
        stmt = (
            select(self.model)
            .join(self.model.getParameter)
            .filter(Parameter.key == reference)
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_value_id(self, value_id: int):
        stmt = select(self.model).filter(self.model.id == value_id)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_value_reference(self, reference: str):
        stmt = select(self.model).filter(self.model.reference == reference)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_name(self, name: str | list[str]):
        name_list = [name] if isinstance(name, str) else name
        stmt = select(self.model).filter(self.model.value.in_(name_list))
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_parent_name(self, parent_name: str):
        stmt = (
            select(self.model)
            .join(self.model.getParent)
            .filter(Parameter.name.ilike(f"%{parent_name}%"))
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
