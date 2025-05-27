from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.attributes_module.models.attributes import Attribute
from src.app.modules.parameters_module.models.parameters import Parameter

class ParameterAttributeSeeder:
    async def run(self):
        session = SessionLocalSeed()

        try:
            # Crear un parámetro
            parameter = Parameter(name="Tipo de documento", description="Define los tipos de documentos")
            session.add(parameter)
            await session.commit()  # await aquí

            # Crear atributos asociados
            attributes = [
                Attribute(name="Cédula de Ciudadanía", description="CC", parameter_id=parameter.id),
                Attribute(name="Tarjeta de Identidad", description="TI", parameter_id=parameter.id),
                Attribute(name="Pasaporte", description="PA", parameter_id=parameter.id),
            ]

            session.add_all(attributes)
            await session.commit()  # await aquí también

            print("✅ Seeder ParameterAttributeSeeder ejecutado con éxito.")

        except Exception as e:
            await session.rollback()  # await también en rollback
            print(f"❌ Error en ParameterAttributeSeeder: {e}")
        finally:
            await session.close()  # await aquí también

