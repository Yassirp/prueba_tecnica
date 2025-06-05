from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

@router.get("/preview-email", response_class=HTMLResponse)
async def preview_email(request: Request):
    """
    Endpoint para previsualizar el email con datos de ejemplo
    """
    # Datos de ejemplo para la previsualización
    preview_data = {
        "name": "Usuario Ejemplo",
        "document_type": "Documento de Identidad",
        "message": "Este es un mensaje de ejemplo para mostrar cómo se verá el correo electrónico cuando se envíe."
    }
    
    return templates.TemplateResponse(
        "email_notification.html",
        {"request": request, **preview_data}
    ) 