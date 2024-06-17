from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Restaurant, Dish, Category


async def get_restaurant_by_name(session: AsyncSession, restaurant_name: str) -> Restaurant:
    result = await session.execute(select(Restaurant).where(Restaurant.name == restaurant_name))
    return result.scalars().first()


async def get_restaurant_by_id(session: AsyncSession, restaurant_id: int) -> Restaurant:
    result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    return result.scalars().first()


async def get_all_dishes_of_restaurant(session: AsyncSession, restaurant_name: str) -> list[Dish]:
    restaurant = await get_restaurant_by_name(session, restaurant_name)
    if restaurant:
        return restaurant.dishes
    return []


async def get_dishes_by_restaurant_and_category(session: AsyncSession, restaurant_name: str, category_name: str) -> list[Dish]:
    restaurant = await get_restaurant_by_name(session, restaurant_name)
    if restaurant:
        result = await session.execute(select(Category).where(Category.name == category_name))
        category = result.scalars().first()
        if category:
            return [dish for dish in restaurant.dishes if dish.category_id == category.id]
    return []
