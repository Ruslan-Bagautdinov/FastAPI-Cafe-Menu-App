from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# own imports

from app.database.postgre_db import get_session
from app.database.crud import get_dishes_by_restaurant_and_category
from app.database.models import Dish

router = APIRouter()


@router.get("/{restaurant_name}/category/{category_name}/dishes")
async def read_dishes_by_category(restaurant_name: str, category_name: str, session: AsyncSession = Depends(get_session)):
    dishes = await get_dishes_by_restaurant_and_category(session, restaurant_name, category_name)
    if not dishes:
        raise HTTPException(status_code=404, detail="No dishes found for this restaurant and category")
    return dishes
