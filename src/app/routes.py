from fastapi import APIRouter
from .modules.stages_module.routes.stages_routes import router as stages_route
from .modules.parameters_module.routes.parameters_routes import router as parameters_routes
from .modules.attributes_module.routes.attributes_routes import router as attributes_routes
from .modules.projects_module.routes.projects_routes import router as projects_router
from .modules.entity_types_module.routes.entity_type_routes import (
    router as entity_types_router,
)

router = APIRouter()

router.include_router(projects_router)
router.include_router(entity_types_router)
router.include_router(stages_route)
router.include_router(parameters_routes)
router.include_router(attributes_routes)
