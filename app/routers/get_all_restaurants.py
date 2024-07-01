from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# own import
from app.database.postgre_db import get_session
from app.database.crud import get_restaurant_id_name_pairs

router = APIRouter()


@router.get("/", description="Retrieves a dictionary mapping restaurant IDs to their names.")
async def get_id_name_pairs(session: AsyncSession = Depends(get_session)):
    """
    Retrieves a dictionary mapping restaurant IDs to their names.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

    Returns:
        dict: A dictionary where keys are restaurant IDs and values are restaurant names.
    """
    pairs = await get_restaurant_id_name_pairs(session)
    return pairs
