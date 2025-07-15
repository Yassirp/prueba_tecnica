from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.user_module.services.report_service import ReportService
from src.app.middleware.api_auth import require_auth, User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/users")
async def download_users_report(
    format: str = Query("excel", description="Formato del reporte: excel o pdf"),
    role_id: int = Query(None, description="Filtrar por ID de rol"),
    department_id: int = Query(None, description="Filtrar por ID de departamento"),
    municipality_id: int = Query(None, description="Filtrar por ID de municipio"),
    country_id: int = Query(None, description="Filtrar por ID de país"),
    is_active: bool = Query(None, description="Filtrar por estado activo/inactivo"),
    state: int = Query(None, description="Filtrar por estado de aprobación"),
    created_at_from: str = Query(None, description="Fecha de creación desde (YYYY-MM-DD)"),
    created_at_to: str = Query(None, description="Fecha de creación hasta (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    """
    Descarga un reporte completo de usuarios en formato Excel o PDF
    Incluye: usuarios, relaciones, estadísticas y resúmenes
    Permite filtrar por rol, departamento, municipio, país, estado, fechas, etc.
    """
    service = ReportService(db)
    filtros = {
        "role_id": role_id,
        "department_id": department_id,
        "municipality_id": municipality_id,
        "country_id": country_id,
        "is_active": is_active,
        "state": state,
        "created_at_from": created_at_from,
        "created_at_to": created_at_to
    }
    return await service.generate_users_report(format=format, filters=filtros)


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