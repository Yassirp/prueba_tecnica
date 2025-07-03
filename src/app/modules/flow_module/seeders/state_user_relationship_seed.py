from datetime import datetime
from src.app.config.database.session_seed import SessionLocalSeed
from src.app.modules.flow_module.models.object_states import ObjectState
from src.app.modules.flow_module.models.flows import Flow
from src.app.modules.flow_module.models.flow_object_states import FlowObjectState


class StateUserRelationshipSeeder:
    async def run(self):
        session = SessionLocalSeed()
        try:
            # Crear flujo
            flow = Flow(reference="user_relationship", flow_name="Flujo de relación de usuario", active=True, created_at=datetime.utcnow())
            session.add(flow)
            await session.flush()

            # Crear estados específicos para este flujo
            state_data = [
                ("pending", "Pendiente"),
                ("accepted", "Aceptado"),
                ("accepted_by_user", "Aceptado por user_id"),
                ("accepted_by_user_relationship", "Aceptado por user_relationship_id"),
                ("rejected_by_user", "Rechazado por user_id"),
                ("rejected_by_user_relationship", "Rechazado por user_relationship_id"),
            ]

            states = []
            for reference, name in state_data:
                state = ObjectState(
                    reference=reference,
                    name=name,
                    active=True,
                    created_at=datetime.utcnow()
                )
                states.append(state)
                session.add(state)

            await session.flush()

            # Asociar estados con el flujo
            flow_object_states = [
                FlowObjectState(
                    flow_id=flow.id,
                    object_state_id=state.id,
                    created_at=datetime.utcnow()
                ) for state in states
            ]
            session.add_all(flow_object_states)

            # Commit
            await session.commit()
            print("✅ StateUserRelationshipSeeder ejecutado con éxito.")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error en StateUserRelationshipSeeder: {e}")
        finally:
            await session.close()
