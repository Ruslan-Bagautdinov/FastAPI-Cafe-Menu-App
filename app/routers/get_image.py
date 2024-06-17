from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import os
import io

from app.tools.functions import read_photo

router = APIRouter()

STATIC_PHOTO_FOLDER = "static/photo"
default_avatar_path = os.path.join(STATIC_PHOTO_FOLDER, 'default_4.jpeg')


@router.get("/")
async def get_image(path: str):
    full_path = os.path.join(STATIC_PHOTO_FOLDER, path)

    if os.path.exists(full_path):
        photo_bytes = await read_photo(full_path)
        if photo_bytes is None:
            photo_bytes = await read_photo(default_avatar_path)
    else:
        photo_bytes = await read_photo(default_avatar_path)

    if photo_bytes is None:
        raise HTTPException(status_code=404, detail="Default image not found")

    return StreamingResponse(io.BytesIO(photo_bytes), media_type="image/jpeg")
