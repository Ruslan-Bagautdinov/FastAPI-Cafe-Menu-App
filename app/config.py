import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

WORK_DATABASE_URL = os.getenv('WORK_DATABASE_URL')
LOCAL_DATABASE_URL = os.getenv('LOCAL_DATABASE_URL')

HOME_DB = os.getenv('HOME_DB', False)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PHOTO_FOLDER = os.path.join(BASE_DIR, 'img')


MIME_TYPES = {
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "tiff": "image/tiff",
    "webp": "image/webp",
}
