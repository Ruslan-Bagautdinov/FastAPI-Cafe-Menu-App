import aiofiles


async def read_photo(photo_path):
    """
    Asynchronously reads the contents of a photo file.

    Args:
        photo_path (str): The path to the photo file.

    Returns:
        bytes | None: The binary data of the photo file if found, otherwise None.

    Raises:
        FileNotFoundError: If the file at `photo_path` does not exist.
        Exception: For any other errors encountered while reading the file.
    """
    try:
        async with aiofiles.open(photo_path, 'rb') as photo_file:
            photo_data = await photo_file.read()
            return photo_data
    except FileNotFoundError:
        print(f"File not found: {photo_path}")
        return None
    except Exception as e:
        print(f"Error reading photo {photo_path}: {e}")
        return None
