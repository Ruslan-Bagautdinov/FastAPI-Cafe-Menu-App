from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

# own import
from app.database.postgre_db import get_session
from app.database.crud import get_category_id_name_pairs

router = APIRouter()


@router.get("/", description="Retrieve a dictionary mapping category IDs to their names for a given restaurant.")
async def get_id_category_pairs(
    restaurant_id: int = Query(..., description="The ID of the restaurant for which to retrieve categories."),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieves a dictionary mapping category IDs to their names for a specified restaurant.

    Args:
        restaurant_id (int): The ID of the restaurant.
        session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

    Returns:
        dict: A dictionary where keys are category IDs and values are category names.
    """
    pairs = await get_category_id_name_pairs(restaurant_id, session)
    return pairs
