from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
import os
import io

from app.tools.functions import read_photo
from app.config import MIME_TYPES

router = APIRouter()

from app.config import MAIN_PHOTO_FOLDER
default_avatar_path = os.path.join(MAIN_PHOTO_FOLDER, 'default_cafe_04.jpeg')


@router.get("/")
async def get_image(
    restaurant_id: int = Query(None, description="The ID of the restaurant"),
    photo: str = Query(None, description="The filename of the photo")
):
    """
    Retrieves a photo from the static photo folder or returns a default photo if the specified photo is not found.

    Args:
        restaurant_id (int): The ID of the restaurant.
        photo (str): The filename of the photo to retrieve. If not provided, the default photo will be returned.

    Returns:
        StreamingResponse: A streaming response containing the photo bytes.

    Raises:
        HTTPException: 404 error if the default photo is not found.
    """
    if restaurant_id and photo:
        restaurant_id = str(restaurant_id)
        full_path = os.path.join(MAIN_PHOTO_FOLDER, restaurant_id, photo)
    else:
        full_path = default_avatar_path

    if os.path.exists(full_path):
        photo_bytes = await read_photo(full_path)
        if photo_bytes is None:
            photo_bytes = await read_photo(default_avatar_path)
    else:
        photo_bytes = await read_photo(default_avatar_path)

    if photo_bytes is None:
        raise HTTPException(status_code=404, detail="Default photo not found")

    # Determine the media type based on the file extension
    file_extension = photo.split('.')[-1].lower() if photo else 'jpeg'
    media_type = MIME_TYPES.get(file_extension, "application/octet-stream")

    return StreamingResponse(io.BytesIO(photo_bytes), media_type=media_type)
