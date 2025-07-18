# Archivo generado automáticamente para sedes - services
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.sedes_module.models.sedes import Sede
from src.app.modules.sedes_module.repositories.sedes_repository import SedeRepository
from src.app.modules.sedes_module.schemas.sedes_schemas import SedeOut, SedeCreate, SedeUpdate
from src.app.modules.parameters_module.repositories.parameter_values_repository import ParameterValueRepository
from src.app.modules.ubication_module.repositories.deparment_repository import DepartmentRepository
from src.app.modules.ubication_module.repositories.municipality_repository import MunicipalityRepository
from src.app.modules.ubication_module.repositories.country_repository import CountryRepository
from fastapi import HTTPException, status

class SedeService(BaseService[Sede, SedeOut]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        super().__init__(
            model=Sede,
            repository_cls=SedeRepository,
            db_session=db_session,
            out_schema=SedeOut,
        )

    async def _validate_foreign_keys(self, data: SedeCreate | SedeUpdate):
        if data.type_id:
            parameter_value_repository = ParameterValueRepository(db_session=self.db_session)
            parameter_value = await parameter_value_repository.get_by_id(data.type_id)
            if not parameter_value:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo inválido.")

        if data.department_id:
            repo = DepartmentRepository(db_session=self.db_session)
            department = await repo.get_by_id(data.department_id)
            if not department:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Departamento inválido.")

        if data.municipality_id:
            repo = MunicipalityRepository(db_session=self.db_session)
            municipality = await repo.get_by_id(data.municipality_id)
            if not municipality:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Municipio inválido.")

        if data.country_id:
            repo = CountryRepository(db_session=self.db_session)
            country = await repo.get_by_id(data.country_id)
            if not country:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="País inválido.")

    async def create(self, data: SedeCreate):
        await self._validate_foreign_keys(data)
        return await super().create(data.model_dump())

    async def update(self, id: int, data: SedeUpdate):
        await self._validate_foreign_keys(data)
        return await super().update(id, data.model_dump(exclude_unset=True))