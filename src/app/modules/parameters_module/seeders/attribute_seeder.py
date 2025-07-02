from src.app.modules.parameters_module.models.parameters import Parameter
from src.app.modules.parameters_module.models.parameters_values import ParameterValue
from sqlalchemy import insert
import json

from src.app.config.database.session_seed import SessionLocalSeed

class AttributeSeeder:
    def __init__(self, parameters: dict):
        self.parameters = parameters
        self.session = SessionLocalSeed()

    async def run(self):
        for parameter_ref, parameter_data in self.parameters.items():
            name = parameter_data.get("name")
            values = parameter_data.get("values", [])

            # Crear parámetro
            result = await self.session.execute(
                insert(Parameter).values(key=parameter_ref, name=name).returning(Parameter.id)
            )
            parameter_id = result.scalar_one()

            # Crear valores del parámetro
            if values:
                await self._save_parameter_values(parameter_id, values, session=self.session)

        await self.session.commit()

    async def _save_parameter_values(self, parameter_id: int, values: list, parent_id: int | None = None, session = None):
        for value_data in values:
            reference = value_data.get("reference")
            value = value_data.get("value")

            # Insertar el valor
            result = await session.execute(
                insert(ParameterValue).values(
                    parameter_id=parameter_id,
                    reference=reference,
                    value=value,
                    parent_id=parent_id
                ).returning(ParameterValue.id)
            )
            pv_id = result.scalar_one()

            # Si hay valores hijos, insertarlos recursivamente
            if "values" in value_data:
                await self._save_parameter_values(parameter_id, value_data["values"], pv_id, session)

    def _get_data(self, data) -> str | None:
        if data is None or isinstance(data, dict):
            return json.dumps(data) if data else None
        return str(data)
