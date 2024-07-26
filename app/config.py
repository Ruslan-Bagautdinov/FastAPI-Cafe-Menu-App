import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Database URLs
WORK_DATABASE_URL = os.getenv('WORK_DATABASE_URL')
LOCAL_DATABASE_URL = os.getenv('LOCAL_DATABASE_URL')
TEST_DB_URL = os.getenv('TEST_DB_URL')

# Environment flag
HOME_DB = os.getenv('HOME_DB', False)

# Base directory and main photo folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PHOTO_FOLDER = os.path.join(BASE_DIR, 'img')

# MIME types for image files
MIME_TYPES = {
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "tiff": "image/tiff",
    "webp": "image/webp",
}