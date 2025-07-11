from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.user_module.services.report_service import ReportService
from src.app.middleware.api_auth import require_auth, User
from typing import Optional

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/users/excel")
async def download_users_excel_report(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    """
    Descarga un reporte completo de usuarios en formato Excel
    Incluye: usuarios, relaciones, estadísticas y resúmenes
    """
    service = ReportService(db)
    return await service.generate_users_excel_report()


@router.get("/relationships/excel")
async def download_relationships_excel_report(
    user_id: Optional[int] = Query(None, description="ID del usuario para filtrar relaciones"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    """
    Descarga un reporte de relaciones de usuarios en formato Excel
    Si se proporciona user_id, filtra las relaciones de ese usuario específico
    """
    service = ReportService(db)
    return await service.generate_user_relationships_report(user_id) 