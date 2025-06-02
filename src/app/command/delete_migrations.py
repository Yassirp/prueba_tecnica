import os
from pathlib import Path

def delete_alembic_migrations():
    """
    By Naoweee Dev: python src/app/command/delete_migrations.py
    """
    versions_path = Path(__file__).resolve().parent.parent.parent / "migrations" / "versions"

    if not versions_path.exists():
        print(f"❌ No existe la carpeta: {versions_path}")
        return

    deleted = 0
    for file in versions_path.iterdir():
        if file.is_file():
            file.unlink()
            print(f"🗑️ Borrado: {file.name}")
            deleted += 1

    print(f"\n✅ Migraciones eliminadas: {deleted}")
    if deleted == 0:
        print("ℹ️ No había archivos para eliminar.")

if __name__ == "__main__":
    delete_alembic_migrations()
