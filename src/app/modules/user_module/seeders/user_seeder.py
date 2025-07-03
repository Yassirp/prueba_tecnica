from datetime import datetime
import pytz
from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.user_module.models.users import User  # Ajusta el import según tu estructura

class UserSeeder:
    async def run(self):
        session = SessionLocalSeed()
        try:
            now = datetime.now(pytz.timezone('America/Bogota'))

            users = [
                User(
                    name="Admin",
                    last_name="Principal",
                    email="adminlvr@naoweesuite.com",
                    password="$2a$10$U8e6SNzUfltfo2qeIrc4VePyVASevTuVvRKfTN4rtk18ftoy0O96e",  # ⚠️ Usa hashing real en prod
                    phone="3001234567",
                    department_id=1,
                    municipality_id=1,
                    country_id=1,
                    address="Cra 1 # 2-34",
                    document_type=1,
                    document_number="1234567890",
                    zip_code="110111",
                    role_id=1,  # Asegúrate que el rol con ID=1 sea Admin
                    state=1,
                    created_at=now,
                ),
                User(
                    name="Juan",
                    last_name="Pérez",
                    email="juanlvr@naoweesuite.com",
                    password="$2a$10$U8e6SNzUfltfo2qeIrc4VePyVASevTuVvRKfTN4rtk18ftoy0O96e",  # ⚠️ Hasheado
                    phone="3109876543",
                    address="Calle 45 # 10-20",
                    department_id=1,
                    municipality_id=1,
                    country_id=1,
                    document_type=1,
                    document_number="1234567890",
                    zip_code="110112",
                    role_id=2,
                    state=1,
                    created_at=now,
                ),
            ]

            session.add_all(users)
            await session.commit()

            print("✅ UserSeeder ejecutado con éxito.")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error en UserSeeder: {e}")
        finally:
            await session.close()
