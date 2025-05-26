import os
import sys

TEMPLATE_FILES = {
    "models": "{}.py",
    "repositories": "{}_repository.py",
    "routes": "{}_routes.py",
    "schemas": "{}_schemas.py",
    "services": "{}_service.py",
}

BASE_DIR = os.path.join("src", "app", "modules")

def create_module_structure(module_name):
    module_path = os.path.join(BASE_DIR, f"{module_name}_module")
    
    if os.path.exists(module_path):
        print(f"❌ El módulo '{module_name}' ya existe.")
        return

    os.makedirs(module_path)
    print(f"📁 Creando módulo: {module_path}")

    for folder, file_template in TEMPLATE_FILES.items():
        folder_path = os.path.join(module_path, folder)
        os.makedirs(folder_path)
        file_name = file_template.format(module_name)
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "w") as f:
            f.write(f"# Archivo generado automáticamente para {module_name} - {folder}\n")
        
        print(f"✅ Archivo creado: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python generate_module.py <module_name>")
        sys.exit(1)
    
    module_name = sys.argv[1]
    create_module_structure(module_name)
