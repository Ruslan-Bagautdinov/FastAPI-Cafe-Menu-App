from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# own imports

from app.database.postgre_db import get_session
from app.database.crud import get_all_dishes_of_restaurant
from app.database.models import Dish

router = APIRouter()


@router.get("/{restaurant_name}/dishes")
async def read_all_dishes(restaurant_name: str, session: AsyncSession = Depends(get_session)):
    dishes = await get_all_dishes_of_restaurant(session, restaurant_name)
    if not dishes:
        raise HTTPException(status_code=404, detail="No dishes found for this restaurant")
    return dishes
