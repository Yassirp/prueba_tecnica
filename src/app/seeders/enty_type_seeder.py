from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.entity_types_module.models.entity_types import EntityType
from src.app.shared.constants.enty_type_enum import (
    EntityTypeds,
    EntityTypeName
)
from src.app.shared.constants.project_enum import Projectds

class EntityTypeSeeder:
    async def run(self):
        session = SessionLocalSeed()

        try:
            # Crear un proyecto
            entity_types = [
                EntityType(name=EntityTypeName.SPORTSWOMAN.value, project_id=Projectds.COMITE.value ,state=1),
                EntityType(name=EntityTypeName.SUPPORT_STAFF.value, project_id=Projectds.COMITE.value, state=1),
            ]
            session.add_all(entity_types)
            await session.commit()  # await aquí

            print("✅ Seeder EntityTypeSeeder ejecutado con éxito.")
        except Exception as e:
            await session.rollback()  # await también en rollback
            print(f"❌ Error en EntityTypeSeeder: {e}")
        finally:
            await session.close()  # await aquí también

