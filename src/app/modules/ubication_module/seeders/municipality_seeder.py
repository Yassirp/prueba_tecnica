from datetime import datetime
from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.ubication_module.models.municipalities import Municipality


class MunicipalitySeeder:
    async def run(self):
        session = SessionLocalSeed()

        try:
            municipalities = [
  Municipality(
            code="05001",
            name="Medellín",
            country_code="CO",
            department_code="05",
            department_id=1,
            created_at=datetime.utcnow(),
        ),
        Municipality(
            code="11001",
            name="Bogotá",
            country_code="CO",
            department_code="11",
            department_id=2,
            created_at=datetime.utcnow(),
        ),
            ]

            session.add_all(municipalities)
            await session.commit()

            print("✅ Seeder CountrySeeder ejecutado con éxito.")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error en CountrySeeder: {e}")
        finally:
            await session.close()
