from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

# own imports

from app.database.postgre_db import get_session
from app.database.crud import get_dishes_by_restaurant_and_category_and_id
from app.database.models import Dish
from app.database.schemas import DishSchema

router = APIRouter()


@router.get("/", response_model=List[DishSchema])
async def get_dishes(
        restaurant_id: int = Query(..., description="The ID of the restaurant"),
        category_id: Optional[int] = Query(None, description="The ID of the category (optional)"),
        dish_id: Optional[int] = Query(None, description="The ID of the dish (optional)"),
        session: AsyncSession = Depends(get_session)
):
    dishes = await get_dishes_by_restaurant_and_category_and_id(session, restaurant_id, category_id, dish_id)
    if not dishes:
        raise HTTPException(status_code=404, detail="No dishes found for the given restaurant and category")
    return dishes
