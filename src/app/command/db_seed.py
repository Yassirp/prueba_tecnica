import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from src.app.command.config.base import BaseCommandAsync
from src.app.seeders.paramert_attribute_seeder import ParameterAttributeSeeder
from src.app.seeders.enty_type_seeder import EntityTypeSeeder
from src.app.seeders.project_seeder import ProjectSeeder

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
                "ParameterAttributeSeeder": ParameterAttributeSeeder(),
                "ProjectSeeder": ProjectSeeder(),
                "EntityTypeSeeder": EntityTypeSeeder(),
                # añade otros seeders aquí...
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
