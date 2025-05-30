from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.attributes_module.models.attributes import Attribute
from src.app.modules.parameters_module.models.parameters import Parameter
from src.app.shared.constants.attribute_and_parameter_enum import (ParameterIds, AttributeIds,AttributeName)

class ParameterAttributeSeeder:
    async def run(self):
        session = SessionLocalSeed()

        try:
            # Crear un parámetro
            parameter = [
                Parameter(id = ParameterIds.STAGES.value, name="Tipos de etapas.", description="Etapas", state=1),
                Parameter(id = ParameterIds.DOCUMENT_STATUS.value, name="Tipos de estados de documentos.", description="Estados",state=1),
                Parameter(id = ParameterIds.TYPE_DOCUMENT.value, name="Tipos de documentos.", description="Estados",state=1),
            ]
            session.add_all(parameter)
            await session.commit()  # await aquí

            # Crear atributos asociados
            attributes = [
                # SEEDER DE ETAPAS
                Attribute(id=AttributeIds.DEPARTMENTAL.value, name=AttributeName.DEPARTMENTAL.value, description=" ", parameter_id=ParameterIds.STAGES.value),
                Attribute(id=AttributeIds.REGIONAL.value,name=AttributeName.DEPARTMENTAL.value, description=" ", parameter_id=ParameterIds.STAGES.value),
                Attribute(id=AttributeIds.NATIONAL.value,name=AttributeName.NATIONAL.value, description=" ", parameter_id=ParameterIds.STAGES.value),

                # SEEDER DE ESTADOS DE DODUMENTO
                Attribute(id=AttributeIds.PENDING_APPROVAL.value,name=AttributeName.PENDING_APPROVAL.value, description=" ", parameter_id=ParameterIds.DOCUMENT_STATUS.value),
                Attribute(id=AttributeIds.APPROVED.value,name=AttributeName.APPROVED.value, description=" ", parameter_id=ParameterIds.DOCUMENT_STATUS.value),
                Attribute(id=AttributeIds.REJECTED.value,name=AttributeName.REJECTED.value, description=" ", parameter_id=ParameterIds.DOCUMENT_STATUS.value),

                # SEDDER DE TIPOS DE DOCUMENTOS 
                Attribute(id=AttributeIds.DOCUMENT_TYPE_PHOTO.value,name=AttributeName.DOCUMENT_TYPE_PHOTO.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.IDENTITY_DOCUMENT.value,name=AttributeName.IDENTITY_DOCUMENT.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.INFORMED_CONSENT.value,name=AttributeName.INFORMED_CONSENT.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.CERTIFICATION_EDUCATIONAL_INSTITUTION.value,name=AttributeName.CERTIFICATION_EDUCATIONAL_INSTITUTION.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.CERTIFICATION_EPS_OR_SISBEN.value,name=AttributeName.CERTIFICATION_EPS_OR_SISBEN.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.CERTIFICATE_LABOR.value,name=AttributeName.CERTIFICATE_LABOR.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.CERTIFICATE_EPS.value,name=AttributeName.CERTIFICATE_EPS.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.CERTIFICATE_ARL.value,name=AttributeName.CERTIFICATE_ARL.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.CERTIFICATE_MEDIAL.value,name=AttributeName.CERTIFICATE_MEDIAL.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.CONSENT_INFORMED.value,name=AttributeName.CONSENT_INFORMED.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.CERTIFICATE_CRIMES.value,name=AttributeName.CERTIFICATE_CRIMES.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(id=AttributeIds.OTHERS.value,name=AttributeName.OTHERS.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
            ]

            session.add_all(attributes)
            await session.commit()  # await aquí también

            print("✅ Seeder ParameterAttributeSeeder ejecutado con éxito.")

        except Exception as e:
            await session.rollback()  # await también en rollback
            print(f"❌ Error en ParameterAttributeSeeder: {e}")
        finally:
            await session.close()  # await aquí también

