from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import json

# own imports

from app.database.postgre_db import get_session
from app.database.crud import get_restaurant_by_id
from app.database.schemas import RestaurantSchema

router = APIRouter()


@router.get("/", response_model=RestaurantSchema)
async def get_restaurant(restaurant_id: int = Query(...,
                                                    description="The ID of the restaurant"),
                         session: AsyncSession = Depends(get_session)):

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
        "rating": restaurant.rating
    }

    return restaurant_data
