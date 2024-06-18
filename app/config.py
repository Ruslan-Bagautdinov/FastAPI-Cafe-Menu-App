from os import getenv, path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

POSTGRES_HOST = getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = getenv('POSTGRES_PORT', '5432')
POSTGRES_USER = getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_DB = getenv('POSTGRES_DB', 'database')

DATABASE_URL = (f"postgresql+asyncpg"
                f"://{POSTGRES_USER}"
                f":{POSTGRES_PASSWORD}"
                f"@{POSTGRES_HOST}"
                f"/{POSTGRES_DB}")

TEST_DATABASE_URL = "postgresql+asyncpg://food_app:GoKY53b4EQ1Jy5@94.124.78.52:5432/food_app"

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
