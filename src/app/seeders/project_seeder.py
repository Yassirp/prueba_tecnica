from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.projects_module.models.projects import Project
from src.app.shared.constants.project_enum import Projectds


class ProjectSeeder:
    async def run(self):
        session = SessionLocalSeed()

        try:
            # Crear un proyecto
            project = [
                Project(name="Comite",  state=1),
            ]
            session.add_all(project)
            await session.commit()  # await aquí


            print("✅ Seeder ProjectSeeder ejecutado con éxito.")

        except Exception as e:
            await session.rollback()  # await también en rollback
            print(f"❌ Error en ProjectSeeder: {e}")
        finally:
            await session.close()  # await aquí también

