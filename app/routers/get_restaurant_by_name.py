from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

# own imports
from app.database.postgre_db import get_session
from app.database.crud import get_restaurant_by_name
from app.database.models import Restaurant

router = APIRouter()


@router.get("/")
async def read_restaurant(restaurant_name: str = Query(..., description="The name of the restaurant"), session: AsyncSession = Depends(get_session)):
    restaurant = await get_restaurant_by_name(session, restaurant_name)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
