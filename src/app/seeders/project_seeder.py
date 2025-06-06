from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.projects_module.models.projects import Project
from src.app.shared.constants.project_enum import Projectds
import hashlib


class ProjectSeeder:
    async def run(self):
        session = SessionLocalSeed()

        try:
            raw_key = "Comite123"
            hashed_key = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
            
            # Crear un proyecto
            project = [
                Project(name="Comite", key=hashed_key, state=1),
            ]
            session.add_all(project)
            await session.commit()  # await aquí


            print("✅ Seeder ProjectSeeder ejecutado con éxito.")

        except Exception as e:
            await session.rollback()  # await también en rollback
            print(f"❌ Error en ProjectSeeder: {e}")
        finally:
            await session.close()  # await aquí también

