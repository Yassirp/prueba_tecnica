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
                Parameter(name="Tipos de etapas.", description="Etapas", state=1),
                Parameter(name="Tipos de estados de documentos.", description="Estados",state=1),
                Parameter(name="Tipos de documentos.", description="Estados",state=1),
                Parameter(name="Tipos de Notificaciones.", description="Notificaciones",state=1),
            ]
            session.add_all(parameter)
            await session.commit()  # await aquí

            # Crear atributos asociados
            attributes = [
                # SEEDER DE ETAPAS
                Attribute(name=AttributeName.DEPARTMENTAL.value, description=" ", parameter_id=ParameterIds.STAGES.value),
                Attribute(name=AttributeName.DEPARTMENTAL.value, description=" ", parameter_id=ParameterIds.STAGES.value),
                Attribute(name=AttributeName.NATIONAL.value, description=" ", parameter_id=ParameterIds.STAGES.value),

                # SEEDER DE ESTADOS DE DODUMENTO
                Attribute(name=AttributeName.PENDING_APPROVAL.value, description=" ", parameter_id=ParameterIds.DOCUMENT_STATUS.value),
                Attribute(name=AttributeName.APPROVED.value, description=" ", parameter_id=ParameterIds.DOCUMENT_STATUS.value),
                Attribute(name=AttributeName.REJECTED.value, description=" ", parameter_id=ParameterIds.DOCUMENT_STATUS.value),

                # SEDDER DE TIPOS DE DOCUMENTOS 
                Attribute(name=AttributeName.DOCUMENT_TYPE_PHOTO.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.IDENTITY_DOCUMENT.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.INFORMED_CONSENT.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.CERTIFICATION_EDUCATIONAL_INSTITUTION.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.CERTIFICATION_EPS_OR_SISBEN.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.CERTIFICATE_LABOR.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.CERTIFICATE_EPS.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.CERTIFICATE_ARL.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.CERTIFICATE_MEDIAL.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.CONSENT_INFORMED.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.CERTIFICATE_CRIMES.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                Attribute(name=AttributeName.OTHERS.value, description=" ", parameter_id=ParameterIds.TYPE_DOCUMENT.value),
                
                # SEEDER DE ESTADOS DE DODUMENTO
                Attribute(name=AttributeName.CANCEL.value, description=" ", parameter_id=ParameterIds.DOCUMENT_STATUS.value),

                # SEEDER DE NOTIFICACIONES
                Attribute(name=AttributeName.MESSAGE_NOTIFICATION.value, description=" ", parameter_id=ParameterIds.NOTIFICATION_TYPE.value),
                Attribute(name=AttributeName.CREATED_NOTIFICATION.value, description=" ", parameter_id=ParameterIds.NOTIFICATION_TYPE.value),
                Attribute(name=AttributeName.UPDATED_NOTIFICATION.value, description=" ", parameter_id=ParameterIds.NOTIFICATION_TYPE.value),
                
            ]

            session.add_all(attributes)
            await session.commit()  # await aquí también

            print("✅ Seeder ParameterAttributeSeeder ejecutado con éxito.")

        except Exception as e:
            await session.rollback()  # await también en rollback
            print(f"❌ Error en ParameterAttributeSeeder: {e}")
        finally:
            await session.close()  # await aquí también

