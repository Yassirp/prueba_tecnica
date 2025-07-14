from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.user_module.services.report_service import ReportService
from src.app.middleware.api_auth import require_auth, User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/users")
async def download_users_report(
    format: str = Query("excel", description="Formato del reporte: excel o pdf"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    """
    Descarga un reporte completo de usuarios en formato Excel o PDF
    Incluye: usuarios, relaciones, estadísticas y resúmenes
    """
    service = ReportService(db)
    return await service.generate_users_report(format=format)


@router.get("/user/{user_id}")
async def download_relationships_excel_report(
    user_id: int,
    format: str = Query("excel", description="Formato del reporte: excel o pdf"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    """
    Descarga un reporte de relaciones de usuarios en formato Excel
    Si se proporciona user_id, filtra las relaciones de ese usuario específico
    """
    service = ReportService(db)
    return await service.generate_user_relationships_report(user_id,format=format) 