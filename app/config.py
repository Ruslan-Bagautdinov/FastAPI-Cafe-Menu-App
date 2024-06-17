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

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
