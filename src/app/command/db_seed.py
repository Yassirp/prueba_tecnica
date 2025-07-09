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
from src.app.modules.parameters_module.seeders.parameter_values_seeder import parameters as parameter_values_parameters
from src.app.modules.parameters_module.seeders.parameters_2025_07_09 import parameters as parameters_2025_07_09
from src.app.modules.flow_module.seeders.state_user_relationship_seed import StateUserRelationshipSeeder

class Command(BaseCommandAsync):
    help = "Corre los seeders necesarios para el funcionamiento de la aplicación"

    """
        Comando para correr seeder 
            -- python3 src/app/command/db_seed.py --class=AttributeSeeder
    """
    def add_arguments(self, parser):
        parser.add_argument('--class', type=str, help='Nombre del seeder específico a ejecutar')

    async def handle(self, **options):
        try:
            class_seeder = options.get('class', None)

            seeders = {
                "CountrySeeder": CountrySeeder(),
                "DepartmentSeeder": DepartmentSeeder(),
                "AttributeSeeder": AttributeSeeder(parameter_values_parameters),
                "MunicipalitySeeder": MunicipalitySeeder(),
                "SecuritySeeder": SecuritySeeder(),
                "StateUserRelationshipSeeder": StateUserRelationshipSeeder(),
                "UserSeeder": UserSeeder(),
                "ParameterValuesSeeder": AttributeSeeder(parameters_2025_07_09),
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
