from fastapi import APIRouter
from .modules.projects_module.routes import router as projects_router

router = APIRouter()

router.include_router(projects_router)