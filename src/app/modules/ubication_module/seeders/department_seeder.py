from datetime import datetime
from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.ubication_module.models.departments import Department


class DepartmentSeeder:
    async def run(self):
        session = SessionLocalSeed()

        try:
            departments = [
        Department(code="05", name="Antioquia", country_code="CO", created_at=datetime.utcnow()),
        Department(code="11", name="Bogotá D.C.", country_code="CO", created_at=datetime.utcnow()),
            ]

            session.add_all(departments)
            await session.commit()

            print("✅ Seeder CountrySeeder ejecutado con éxito.")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error en CountrySeeder: {e}")
        finally:
            await session.close()
