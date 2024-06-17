from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
import os
import io

from app.tools.functions import read_photo
from app.config import MIME_TYPES

router = APIRouter()

STATIC_PHOTO_FOLDER = "static/photo"
default_avatar_path = os.path.join(STATIC_PHOTO_FOLDER, 'default_4.jpeg')


@router.get("/")
async def get_image(path: str = Query(None, description="The image filename")):
    full_path = os.path.join(STATIC_PHOTO_FOLDER, path)

    if os.path.exists(full_path):
        photo_bytes = await read_photo(full_path)
        if photo_bytes is None:
            photo_bytes = await read_photo(default_avatar_path)
    else:
        photo_bytes = await read_photo(default_avatar_path)

    if photo_bytes is None:
        raise HTTPException(status_code=404, detail="Default image not found")

    # Determine the media type based on the file extension
    file_extension = path.split('.')[-1].lower()
    media_type = MIME_TYPES.get(file_extension, "application/octet-stream")

    return StreamingResponse(io.BytesIO(photo_bytes), media_type=media_type)
