from os import getenv, path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

WORK_DATABASE_URL = getenv('WORK_DATABASE_URL')
LOCAL_DATABASE_URL = getenv('LOCAL_DATABASE_URL')

HOME = getenv('HOME', False)

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
