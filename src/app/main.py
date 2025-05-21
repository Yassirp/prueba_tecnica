from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from src.app.shared.constants.settings import Settings
from src.app.middleware.api_key import APIKeyMiddleware
import os

app = FastAPI(
    title=Settings.APP_NAME,
    description=Settings.APP_DESCRIPTION,
    version=Settings.APP_VERSION
)

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)
#app.add_middleware(APIKeyMiddleware)

@app.get("/")
async def root():
    image_path = os.path.join("src", "app", "static", "status.svg")
    return FileResponse(image_path, media_type="image/svg+xml")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=Settings.HOST,
        port=Settings.PORT,
        reload=Settings.DEBUG
    )
