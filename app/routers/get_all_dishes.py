from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

# own imports

from app.database.postgre_db import get_session
from app.database.crud import get_dishes_by_restaurant_and_category
from app.database.models import Dish

router = APIRouter()


@router.get("/")
async def get_dishes(restaurant_id: int,
                     category_id: Optional[int] = None,
                     session: AsyncSession = Depends(get_session)
                     ):
    dishes = await get_dishes_by_restaurant_and_category(session, restaurant_id, category_id)
    if not dishes:
        raise HTTPException(status_code=404, detail="No dishes found for the given restaurant and category")
    return dishes
