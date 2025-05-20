from utils.constants import Settings

class Connection:
    URL = f'postgresql+psycopg2://{Settings.DB_USERNAME}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/{Settings.DB_NAME}'
    MYSQL_URL = f'mysql+pymysql://{Settings.MYSQL_USER}:{Settings.MYSQL_PASSWORD}@{Settings.MYSQL_HOST}:{Settings.MYSQL_PORT}/{Settings.MYSQL_DB}'

