from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

# own import
from app.database.crud import (format_extra_prices,
                               get_dish_detailed_info)
from app.database.postgre_db import get_session


router = APIRouter()


@router.get("/details", response_model=Dict, description="Retrieve detailed information about a Dish including related Restaurant and Category details.")
async def get_dish_details(dish_id: int = Query(..., description="The ID of the Dish to retrieve."),
                           session: AsyncSession = Depends(get_session)):
    """
    Retrieves detailed information about a Dish including related Restaurant and Category details.

    Args:
        dish_id (int): The ID of the Dish to retrieve.
        session (AsyncSession): The SQLAlchemy asynchronous session.

    Returns:
        dict: A dictionary containing detailed information about the Dish.
    """
    dish_details = await get_dish_detailed_info(session, dish_id)

    if not dish_details:
        raise HTTPException(status_code=404, detail="Dish not found")

    return dish_details
