# Módulos sin relaciones circulares
from src.app.modules.parameters_module.models.parameters import Parameter 
from src.app.modules.parameters_module.models.parameters_values import ParameterValue 

# Permisos y acciones — usa strings en los modelos
from src.app.modules.permission_module.models.actions import Action 
from src.app.modules.permission_module.models.module import Module
from src.app.modules.permission_module.models.module_actions import ModuleAction
from src.app.modules.permission_module.models.role import Role
from src.app.modules.permission_module.models.permissions import Permission

# Ubicación
from src.app.modules.ubication_module.models.countries import Country
from src.app.modules.ubication_module.models.departments import Department
from src.app.modules.ubication_module.models.municipalities import Municipality

# Documentos
from src.app.modules.document_module.models.documents import Document

# Flujos
from src.app.modules.flow_module.models.flows import Flow
from src.app.modules.flow_module.models.object_states import ObjectState
from src.app.modules.flow_module.models.flow_object_states import FlowObjectState


# Finalmente: User (que depende de todo lo anterior)
from src.app.modules.user_module.models.users import User
from src.app.modules.user_module.models.user_relationship import UserRelationship

# Sedes
from src.app.modules.sedes_module.models.sedes import Sede

# Eventos
from src.app.modules.living_group_module.models.living_group import LivingGroup
from src.app.modules.living_group_module.models.living_group_users import LivingGroupUser

# Pagos
from src.app.modules.payment_module.models.payment import Payment


from src.app.shared.bases.base_model import BaseModel
