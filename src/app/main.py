from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from src.app.middleware.api_key import APIKeyMiddleware
from src.app.shared.constants.settings import Settings
from src.app.routes import router as main_router
from src.app.shared.utils.request_utils import http_response, get_errors_validations
from src.app.shared.constants.messages import GlobalMessages
from src.app.utils.email_preview import router as email_preview_router
from fastapi.openapi.utils import get_openapi

# Configuracion para Swagger
app = FastAPI(
    title=Settings.APP_NAME,
    description=Settings.APP_DESCRIPTION,
    version=Settings.APP_VERSION,
    swagger_ui_parameters={"displayRequestDuration": True},
)

# Configuracion para Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=Settings.APP_NAME,
        version=Settings.APP_VERSION,
        description=Settings.APP_DESCRIPTION,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# TEMPLATES
templates = Jinja2Templates(directory="src/app/templates")

# STATIC FILES
app.mount("/static", StaticFiles(directory="src/app/static"), name="static")

# MAIN ROUTERS
app.include_router(main_router)
#app.include_router(email_preview_router, tags=["Email Preview"])


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "version": Settings.APP_VERSION,
            "app_name": Settings.APP_NAME,
            "app_description": Settings.APP_DESCRIPTION,
        },
    )

# MIDDLEWARES
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in Settings.ALLOWED_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(APIKeyMiddleware)

# MANEJO DE ERRORES GLOBALES
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    error_messages = [
        f"'{error['field']}': {error['message']}" for error in get_errors_validations(exc)
    ]
    return http_response(
        message=GlobalMessages.ERROR_UNPROCESSABLE_ENTITY_VALIDATION,
        errors=error_messages,
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return http_response(
        message=GlobalMessages.ERROR_INTERNAL,
        errors=[str(exc)],
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# ARRANQUE DE LA APLICACION
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=Settings.HOST, port=Settings.PORT, reload=Settings.DEBUG)
