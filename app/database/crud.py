from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, Optional, List

# own imports
from app.database.models import Restaurant, Dish, Category


# async def get_restaurant_by_name(session: AsyncSession, restaurant_name: str) -> Restaurant:
#     result = await session.execute(select(Restaurant).where(Restaurant.name == restaurant_name))
#     return result.scalars().first()


async def get_restaurant_by_id(session: AsyncSession, restaurant_id: int) -> Restaurant:
    result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    return result.scalars().first()


async def get_dishes_by_restaurant_and_category(session: AsyncSession, restaurant_id: int,
                                                category_id: Optional[int] = None) -> List[Dish] | None:
    query = select(Dish)

    # if restaurant_identifier.isdigit():
    #     restaurant_id = int(restaurant_identifier)
    #     query = query.where(Dish.restaurant_id == restaurant_id)
    # else:
    #     query = query.join(Restaurant).where(Restaurant.name == restaurant_identifier)
    #

    try:
        query = query.where(Dish.restaurant_id == restaurant_id)
    except ValueError:
        return None

    if category_id:
        try:
            query = query.where(Dish.category_id == category_id)
        except ValueError:
            return None

        # if category_identifier.isdigit():
        #     category_id = int(category_identifier)
        #     query = query.where(Dish.category_id == category_id)
        # else:
        #     query = query.join(Category).where(Category.name == category_identifier)

    result = await session.execute(query)
    return list(result.scalars().all())
