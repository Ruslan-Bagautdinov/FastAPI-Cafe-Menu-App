from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from typing import Optional, List, Dict
from decimal import Decimal


# own imports
from app.database.models import (Restaurant,
                                 Dish,
                                 Category
                                 )


def format_extra_prices(extra: Optional[Dict]) -> Optional[Dict]:
    if extra is None:
        return None
    formatted_extra = {}
    for key, value in extra.items():
        description, price = value
        formatted_price = Decimal(str(price)).quantize(Decimal('0.01'))
        formatted_extra[key] = [description, formatted_price]
    return formatted_extra


async def get_restaurant_id_name_pairs(session: AsyncSession) -> dict:
    """
    Retrieves a dictionary mapping restaurant IDs to their names.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session.

    Returns:
        dict: A dictionary where keys are restaurant IDs and values are restaurant names.
    """
    result = await session.execute(select(Restaurant.id, Restaurant.name))
    pairs = result.fetchall()
    return {restaurant_id: restaurant_name for restaurant_id, restaurant_name in pairs}


async def get_category_id_name_pairs(session: AsyncSession, restaurant_id: Optional[int] = None) -> Dict[int, str]:
    """
    Fetches all dishes for a given restaurant_id, extracts their category_id,
    and returns a dictionary with category_id as keys and category_name as values.
    If restaurant_id is None, fetches all categories.

    Args:
        restaurant_id (Optional[int]): The ID of the restaurant.
        session (AsyncSession): The SQLAlchemy asynchronous session.

    Returns:
        Dict[int, str]: A dictionary with category_id as keys and category_name as values.
    """
    if restaurant_id is not None:

        dish_query = await session.execute(
            select(Dish).where(Dish.restaurant_id == restaurant_id)
        )
        dishes = dish_query.scalars().all()

        category_ids = {dish.category_id for dish in dishes}

        category_query = await session.execute(
            select(Category).where(Category.id.in_(category_ids))
        )
    else:
        category_query = await session.execute(select(Category))

    categories = category_query.scalars().all()

    category_id_name_pairs = {category.id: category.name for category in categories}

    return category_id_name_pairs


async def get_restaurant_by_id(session: AsyncSession, restaurant_id: int) -> Restaurant:
    """
    Retrieves a restaurant by its ID.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session.
        restaurant_id (int): The ID of the restaurant to retrieve.

    Returns:
        Restaurant: The Restaurant object corresponding to the given ID.
    """
    result = await session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    return result.scalars().first()


async def get_dishes_by_restaurant_and_category_and_id(session: AsyncSession,
                                                       restaurant_id: Optional[int] = None,
                                                       category_id: Optional[int] = None,
                                                       dish_id: Optional[int] = None) -> List[dict] | None:
    """
    Retrieves a list of dishes based on the provided restaurant ID, optionally filtered by category ID and/or dish ID.
    If restaurant_id is not provided, all dishes are returned.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session.
        restaurant_id (Optional[int]): The ID of the restaurant to retrieve dishes from. Defaults to None.
        category_id (Optional[int]): The ID of the category to filter dishes by. Defaults to None.
        dish_id (Optional[int]): The ID of the specific dish to retrieve. Defaults to None.

    Returns:
        List[dict] | None: A list of dictionaries containing dish details and restaurant currency,
        or None if no dishes are found.
    """
    query = select(Dish).options(selectinload(Dish.restaurant))

    if restaurant_id is not None:
        query = query.where(Dish.restaurant_id == restaurant_id)

    if category_id is not None:
        query = query.where(Dish.category_id == category_id)

    if dish_id is not None:
        query = query.where(Dish.id == dish_id)

    result = await session.execute(query)
    dishes = result.scalars().all()

    if not dishes:
        return None

    dish_list = []

    for dish in dishes:
        if dish.restaurant is None:
            continue  # Skip dishes without an associated restaurant

        dish.price = Decimal(str(dish.price)).quantize(Decimal('0.01'))
        dish.extra = format_extra_prices(dish.extra)

        dish_info = {
            "id": dish.id,
            "restaurant_id": dish.restaurant_id,
            "category_id": dish.category_id,
            "name": dish.name,
            "photo": dish.photo,
            "description": dish.description,
            "price": dish.price,
            "extra": dish.extra,
            "currency": dish.restaurant.currency
        }
        dish_list.append(dish_info)

    return dish_list


async def get_dish_detailed_info(session: AsyncSession, dish_id: int):
    """
    Retrieves detailed information about a Dish including related Restaurant and Category details.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session.
        dish_id (int): The ID of the Dish to retrieve.

    Returns:
        dict: A dictionary containing detailed information about the Dish.
    """

    query = select(Dish).options(
        selectinload(Dish.restaurant),
        selectinload(Dish.category)
    ).where(Dish.id == dish_id)

    result = await session.execute(query)
    dish = result.scalars().first()

    if not dish:
        return None

    dish.price = Decimal(str(dish.price)).quantize(Decimal('0.01'))
    dish.extra = format_extra_prices(dish.extra)

    dish_details = {
        "id": dish.id,
        "restaurant_name": dish.restaurant.name,
        "category_name": dish.category.name,
        "name": dish.name,
        "photo": dish.photo,
        "description": dish.description,
        "price": dish.price,
        "currency": dish.restaurant.currency,
        "extra": dish.extra
    }

    return dish_details


async def get_dish_basket_info(session: AsyncSession, dish_id: int):
    """
    Retrieves detailed information about a Dish including related Restaurant and Category details.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session.
        dish_id (int): The ID of the Dish to retrieve.

    Returns:
        dict: A dictionary containing detailed information about the Dish.
    """

    query = select(Dish).options(
        selectinload(Dish.restaurant),
        selectinload(Dish.category)
    ).where(Dish.id == dish_id)

    result = await session.execute(query)
    dish = result.scalars().first()

    if not dish:
        return None

    dish.price = Decimal(str(dish.price)).quantize(Decimal('0.01'))
    # dish.extra = format_extra_prices(dish.extra)

    dish_details = {
        "id": dish.id,
        "restaurant_name": dish.restaurant.name,
        "category_name": dish.category.name,
        "name": dish.name,
        "photo": dish.photo,
        "description": dish.description,
        "price": dish.price,
        "currency": dish.restaurant.currency,
        "extra": dish.extra
    }

    return dish_details
