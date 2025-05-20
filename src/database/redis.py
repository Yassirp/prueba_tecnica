from redis import Redis
from utils.constants import Settings

redis_client = Redis(
    host=Settings.REDIS_HOST,
    port=Settings.REDIS_PORT,
    decode_responses=Settings.REDIS_DECODE_RESPONSES,
    username=Settings.REDIS_USERNAME,
    password=Settings.REDIS_PASSWORD,
)
