from datetime import datetime
from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.ubication_module.models.countries import Country


class CountrySeeder:
    async def run(self):
        session = SessionLocalSeed()

        try:
            countries = [
                Country(code="CO", name="Colombia", created_at=datetime.utcnow()),
                Country(code="US", name="United States", created_at=datetime.utcnow()),
            ]

            session.add_all(countries)
            await session.commit()

            print("✅ Seeder CountrySeeder ejecutado con éxito.")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error en CountrySeeder: {e}")
        finally:
            await session.close()
