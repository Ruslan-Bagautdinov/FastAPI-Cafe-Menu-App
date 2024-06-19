from os import getenv, path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# LOCAL_POSTGRES_HOST = getenv('LOCAL_POSTGRES_HOST', 'localhost')
# LOCAL_POSTGRES_PORT = getenv('LOCAL_POSTGRES_PORT', '5432')
# LOCAL_POSTGRES_USER = getenv('LOCAL_POSTGRES_USER', 'postgres')
# LOCAL_POSTGRES_PASSWORD = getenv('LOCAL_POSTGRES_PASSWORD', 'password')
# LOCAL_POSTGRES_DB = getenv('LOCAL_POSTGRES_DB', 'database')
#
# LOCAL_DATABASE_URL = (f"postgresql+asyncpg"
#                       f"://{LOCAL_POSTGRES_USER}"
#                       f":{LOCAL_POSTGRES_PASSWORD}"
#                       f"@{LOCAL_POSTGRES_HOST}"
#                       f"/{LOCAL_POSTGRES_DB}")
#
# WORK_POSTGRES_HOST = getenv('WORK_POSTGRES_HOST', 'localhost')
# WORK_POSTGRES_PORT = getenv('WORK_POSTGRES_PORT', '5432')
# WORK_POSTGRES_USER = getenv('WORK_POSTGRES_USER', 'postgres')
# WORK_POSTGRES_PASSWORD = getenv('WORK_POSTGRES_PASSWORD', 'password')
# WORK_POSTGRES_DB = getenv('WORK_POSTGRES_DB', 'database')
#
# WORK_DATABASE_URL = (f"postgresql+asyncpg"
#                      f"://{WORK_POSTGRES_USER}"
#                      f":{WORK_POSTGRES_PASSWORD}"
#                      f"@{WORK_POSTGRES_HOST}"
#                      f"/{WORK_POSTGRES_DB}")


WORK_DATABASE_URL = "postgresql+asyncpg://food_app:GoKY53b4EQ1Jy5@94.124.78.52:5432/food_app"

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

MIME_TYPES = {
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "tiff": "image/tiff",
    "webp": "image/webp",
}
