from datetime import datetime
from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.permission_module.models.role import Role
from src.app.modules.permission_module.models.actions import Action
from src.app.modules.permission_module.models.module import Module
from src.app.modules.permission_module.models.module_actions import ModuleAction
from src.app.modules.permission_module.models.permissions import Permission


class SecuritySeeder:
    async def run(self):
        session = SessionLocalSeed()
        try:
            # 1️⃣ Crear roles
            roles = [
                Role(code="admin", name="Administrador", active=True, created_at=datetime.utcnow()),
                Role(code="user", name="Usuario", active=True, created_at=datetime.utcnow()),
                Role(code="builder", name="Builder", active=True, created_at=datetime.utcnow()),
                Role(code="leader", name="Líder", active=True, created_at=datetime.utcnow()),
            ]
            session.add_all(roles)
            await session.flush()  # Para obtener los IDs

            # 2️⃣ Crear acciones
            actions = [
                Action(code="VIEW", name="Ver", active=True, created_at=datetime.utcnow()),
                Action(code="EDIT", name="Editar", active=True, created_at=datetime.utcnow()),
                Action(code="DELETE", name="Eliminar", active=True, created_at=datetime.utcnow()),
            ]
            session.add_all(actions)
            await session.flush()

            # 3️⃣ Crear módulos
            modules = [
                Module(
                    level=1,
                    name="Dashboard",
                    path="/dashboard",
                    parent_id=None,
                    active=True,
                    position=1,
                    icon="dashboard",
                    created_at=datetime.utcnow()
                ),
                Module(
                    level=1,
                    name="Usuarios",
                    path="/users",
                    parent_id=None,
                    active=True,
                    position=2,
                    icon="users",
                    created_at=datetime.utcnow()
                ),
            ]
            session.add_all(modules)
            await session.flush()

            # 4️⃣ Asociar acciones con módulos (ModuleAction)
            module_actions = []
            for module in modules:
                for action in actions:
                    module_actions.append(
                        ModuleAction(
                            module_id=module.id,
                            action_id=action.id,
                            created_at=datetime.utcnow()
                        )
                    )
            session.add_all(module_actions)
            await session.flush()

            # 5️⃣ Asignar permisos al rol ADMIN
            permissions = [
                Permission(
                    associate_to="role", 
                    associate_id=1,
                    module_action_id=mod_act.id,
                    created_at=datetime.utcnow()
                )
                for mod_act in module_actions
            ]
            session.add_all(permissions)

            # ✅ Confirmar
            await session.commit()
            print("✅ SecuritySeeder ejecutado con éxito.")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error en SecuritySeeder: {e}")
        finally:
            await session.close()