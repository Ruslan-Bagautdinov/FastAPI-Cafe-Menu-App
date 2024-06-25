from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from decimal import Decimal

# own imports
from app.database.postgre_db import get_session
from app.database.crud import get_dishes_by_restaurant_and_category_and_id
from app.database.models import Dish
from app.database.schemas import DishSchema

router = APIRouter()


@router.get("/", response_model=List[DishSchema])
async def get_dishes(
        restaurant_id: Optional[int] = Query(None, description="The ID of the restaurant (optional)"),
        category_id: Optional[int] = Query(None, description="The ID of the category (optional)"),
        dish_id: Optional[int] = Query(None, description="The ID of the specific dish to retrieve (optional)"),
        session: AsyncSession = Depends(get_session)
):
    """
    Retrieves a list of dishes based on the provided restaurant ID, optionally filtered by category ID and/or dish ID.
    If restaurant_id is not provided, all dishes are returned.

    Args:
        restaurant_id (Optional[int]): The ID of the restaurant to retrieve dishes from. Defaults to None.
        category_id (Optional[int]): The ID of the category to filter dishes by. Defaults to None.
        dish_id (Optional[int]): The ID of the specific dish to retrieve. Defaults to None.
        session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

    Returns:
        List[DishSchema]: A list of DishSchema objects matching the criteria.

    Raises:
        HTTPException: 404 error if no dishes are found for the given criteria.
    """
    dishes = await get_dishes_by_restaurant_and_category_and_id(session, restaurant_id, category_id, dish_id)
    if not dishes:
        raise HTTPException(status_code=404, detail="No dishes found for the given criteria")

    # Convert price to Decimal with 2 decimal places
    for dish in dishes:
        dish.price = Decimal(str(dish.price)).quantize(Decimal('0.01'))

    return dishes
