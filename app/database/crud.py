from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, Optional, List

# own imports
from app.database.models import Restaurant, Dish, Category


async def get_restaurant_id_name_pairs(session: AsyncSession) -> dict:
    """
    Retrieve a dictionary with all pairs of restaurant_id and restaurant_name.

    :param session: The asynchronous database session.
    :return: A dictionary with restaurant_id as keys and restaurant_name as values.
    """
    result = await session.execute(select(Restaurant.id, Restaurant.name))
    pairs = result.fetchall()
    return {restaurant_id: restaurant_name for restaurant_id, restaurant_name in pairs}


async def get_category_id_name_pairs(session: AsyncSession) -> dict:
    """
    Retrieve a dictionary with all pairs of category_id and category_name.

    :param session: The asynchronous database session.
    :return: A dictionary with category_id as keys and category_name as values.
    """
    result = await session.execute(select(Category.id, Category.name))
    pairs = result.fetchall()
    return {category_id: category_name for category_id, category_name in pairs}


async def get_restaurant_by_id(session: AsyncSession, restaurant_id: int) -> Restaurant:
    result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    return result.scalars().first()


async def get_dishes_by_restaurant_and_category(session: AsyncSession, restaurant_id: int,
                                                category_id: Optional[int] = None) -> List[Dish] | None:
    query = select(Dish)

    query = query.where(Dish.restaurant_id == restaurant_id)

    if category_id:
        query = query.where(Dish.category_id == category_id)

    result = await session.execute(query)
    return list(result.scalars().all())
