from app.shared.constants.settings import Settings

class Connection:
    URL = f'postgresql+asyncpg://{Settings.DB_USERNAME}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/{Settings.DB_NAME}'