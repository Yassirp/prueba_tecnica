from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.attributes_module.models.attributes import Attribute
from src.app.modules.parameters_module.models.parameters import Parameter
from src.app.shared.constants.attribute_and_parameter import (ParameterIds, AttributeIds)

class ParameterAttributeSeeder:
    async def run(self):
        session = SessionLocalSeed()

        try:
            # Crear un parámetro
            parameter = [
                Parameter(id = ParameterIds.STAGES.value, name="Tipos de etapas.", description="Etapas", state=1),
                Parameter(id = ParameterIds.DOCUMENT_STATUS.value, name="Tipos de estados de documentos.", description="Estados",state=1),
            ]
            session.add_all(parameter)
            await session.commit()  # await aquí

            # Crear atributos asociados
            attributes = [
                # SEEDER DE ETAPAS
                Attribute(id=AttributeIds.DEPARTMENTAL.value, name="Departamental", description="Etapa departamental", parameter_id=ParameterIds.STAGES.value),
                Attribute(id=AttributeIds.REGIONAL.value,name="Regional", description="Etapa regional", parameter_id=ParameterIds.STAGES.value),
                Attribute(id=AttributeIds.NATIONAL.value,name="Nacional", description="Etapa nacional", parameter_id=ParameterIds.STAGES.value),

                # SEEDER DE ESTADOS DE DODUMENTO
                Attribute(id=AttributeIds.PENDING_APPROVAL.value,name="Pendiente de aprobación", description="Estado pendiente", parameter_id=ParameterIds.DOCUMENT_STATUS.value),
                Attribute(id=AttributeIds.APPROVED.value,name="Aprobado", description="Estado aprobado", parameter_id=ParameterIds.DOCUMENT_STATUS.value),
                Attribute(id=AttributeIds.REJECTED.value,name="Rechazado", description="Estado rechazado", parameter_id=ParameterIds.DOCUMENT_STATUS.value),
            ]

            session.add_all(attributes)
            await session.commit()  # await aquí también

            print("✅ Seeder ParameterAttributeSeeder ejecutado con éxito.")

        except Exception as e:
            await session.rollback()  # await también en rollback
            print(f"❌ Error en ParameterAttributeSeeder: {e}")
        finally:
            await session.close()  # await aquí también

