import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.app.command.config.base import BaseCommandAsync
from src.app.modules.ubication_module.seeders.country_seeder import CountrySeeder
from src.app.modules.ubication_module.seeders.department_seeder import DepartmentSeeder
from src.app.modules.ubication_module.seeders.municipality_seeder import MunicipalitySeeder
from src.app.modules.permission_module.seeders.security_seeder import SecuritySeeder
from src.app.modules.user_module.seeders.user_seeder import UserSeeder
from src.app.modules.parameters_module.seeders.attribute_seeder import AttributeSeeder
from src.app.modules.parameters_module.seeders.documents_media_type_seeder import parameters as document_type_parameters
from src.app.modules.flow_module.seeders.state_user_relationship_seed import StateUserRelationshipSeeder
from src.app.modules.parameters_module.seeders.type_parent_seeder import parameters as type_parent_parameters

class Command(BaseCommandAsync):
    help = "Corre los seeders necesarios para el funcionamiento de la aplicación"

    """
        Comando para correr seeder 
            -- python3 src/app/command/db_seed.py --class=ProjectSeeder
    """
    def add_arguments(self, parser):
        parser.add_argument('--class', type=str, help='Nombre del seeder específico a ejecutar')

    async def handle(self, **options):
        try:
            class_seeder = options.get('class', None)

            seeders = {
                "CountrySeeder": CountrySeeder(),
                "DepartmentSeeder": DepartmentSeeder(),
                "MunicipalitySeeder": MunicipalitySeeder(),
                "SecuritySeeder": SecuritySeeder(),
                "AttributeSeederDocumentType": AttributeSeeder(document_type_parameters),
                "AttributeSeederTypeParent": AttributeSeeder(type_parent_parameters),
                "StateUserRelationshipSeeder": StateUserRelationshipSeeder(),
                "UserSeeder": UserSeeder(),
            }

            if class_seeder:
                seeder = seeders.get(class_seeder)
                if not seeder:
                    print(f"❌ Seeder '{class_seeder}' no encontrado.")
                    return
                print(f"➡️ Ejecutando {class_seeder}...")
                await seeder.run()
                print(f"✅ Seeder '{class_seeder}' ejecutado correctamente.")
            else:
                print("🌱 Ejecutando todos los seeders...\n")
                for name, seeder in seeders.items():
                    print(f"➡️ Ejecutando {name}...")
                    await seeder.run()
                print("\n✅ Todos los seeders fueron ejecutados correctamente.")
        except Exception as e:
            print("❌ Ha ocurrido un error:", str(e))


if __name__ == "__main__":
    Command().run_from_argv()
