from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from shared.constants.settings import Settings
from middleware.api_key import APIKeyMiddleware
import os

app = FastAPI(
    title=Settings.APP_NAME,
    description=Settings.APP_DESCRIPTION,
    version=Settings.APP_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add API Key middleware
app.add_middleware(APIKeyMiddleware)

@app.get("/")
async def root():
    image_path = os.path.join("src", "app", "static", "status.svg")
    return FileResponse(image_path, media_type="image/svg+xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=Settings.HOST,
        port=Settings.PORT,
        reload=bool(Settings.DEBUG)
    )