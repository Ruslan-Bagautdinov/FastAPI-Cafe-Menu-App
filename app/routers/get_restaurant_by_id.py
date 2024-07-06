from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# own imports
from app.database.postgre_db import get_session
from app.database.crud import get_restaurant_by_id
from app.database.schemas import RestaurantSchema

router = APIRouter()


@router.get("/", response_model=RestaurantSchema)
async def get_restaurant(restaurant_id: int = Query(..., description="The ID of the restaurant"),
                         session: AsyncSession = Depends(get_session)):
    """
    Retrieves a restaurant by its ID.

    Args:
        restaurant_id (int): The ID of the restaurant to retrieve.
        session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

    Returns:
        RestaurantSchema: The restaurant data.

    Raises:
        HTTPException: 400 error if restaurant_id is not provided.
        HTTPException: 404 error if the restaurant is not found.
    """
    if restaurant_id is not None:
        restaurant = await get_restaurant_by_id(session, restaurant_id)
    else:
        raise HTTPException(status_code=400, detail="Restaurant_id must be provided")

    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    restaurant_data = {
        "id": restaurant.id,
        "name": restaurant.name,
        "photo": restaurant.photo,
        "rating": '%.1f' % restaurant.rating,
        "tables_amount": restaurant.tables_amount,
        "restaurant_currency": restaurant.currency  # Include the currency in the response
    }

    return restaurant_data
