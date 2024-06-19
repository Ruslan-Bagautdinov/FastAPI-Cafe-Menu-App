from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
import os
import io

from app.tools.functions import read_photo
from app.config import MIME_TYPES

router = APIRouter()

STATIC_PHOTO_FOLDER = "static/photo"
default_avatar_path = os.path.join(STATIC_PHOTO_FOLDER, 'default_cafe_04.jpeg')


@router.get("/")
async def get_image(path: str = Query(None, description="The image filename")):
    """
    Retrieves an image from the static photo folder or returns a default image if the specified image is not found.

    Args:
        path (str): The filename of the image to retrieve. If not provided, the default image will be returned.

    Returns:
        StreamingResponse: A streaming response containing the image bytes.

    Raises:
        HTTPException: 404 error if the default image is not found.
    """
    full_path = os.path.join(STATIC_PHOTO_FOLDER, path) if path else default_avatar_path

    if os.path.exists(full_path):
        photo_bytes = await read_photo(full_path)
        if photo_bytes is None:
            photo_bytes = await read_photo(default_avatar_path)
    else:
        photo_bytes = await read_photo(default_avatar_path)

    if photo_bytes is None:
        raise HTTPException(status_code=404, detail="Default image not found")

    # Determine the media type based on the file extension
    file_extension = path.split('.')[-1].lower() if path else 'jpeg'
    media_type = MIME_TYPES.get(file_extension, "application/octet-stream")

    return StreamingResponse(io.BytesIO(photo_bytes), media_type=media_type)
