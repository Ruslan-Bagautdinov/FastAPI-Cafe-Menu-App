from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from typing import Optional, List, Dict

# own imports
from app.database.models import (Restaurant,
                                 Dish,
                                 Category,
                                 Basket
                                 )


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
        # Fetch all dishes for the given restaurant_id
        dish_query = await session.execute(
            select(Dish).where(Dish.restaurant_id == restaurant_id)
        )
        dishes = dish_query.scalars().all()

        # Extract all unique category_id from the dishes
        category_ids = {dish.category_id for dish in dishes}

        # Fetch category names for the extracted category_ids
        category_query = await session.execute(
            select(Category).where(Category.id.in_(category_ids))
        )
    else:
        # Fetch all categories
        category_query = await session.execute(select(Category))

    categories = category_query.scalars().all()

    # Create a dictionary with category_id as keys and category_name as values
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
                                                       dish_id: Optional[int] = None) -> List[Dish] | None:
    """
    Retrieves a list of dishes based on the provided restaurant ID, optionally filtered by category ID and/or dish ID.
    If restaurant_id is not provided, all dishes are returned.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session.
        restaurant_id (Optional[int]): The ID of the restaurant to retrieve dishes from. Defaults to None.
        category_id (Optional[int]): The ID of the category to filter dishes by. Defaults to None.
        dish_id (Optional[int]): The ID of the specific dish to retrieve. Defaults to None.

    Returns:
        List[Dish] | None: A list of Dish objects matching the criteria, or None if no dishes are found.
    """
    query = select(Dish)

    if restaurant_id is not None:
        query = query.where(Dish.restaurant_id == restaurant_id)

    if category_id is not None:
        query = query.where(Dish.category_id == category_id)

    if dish_id is not None:
        query = query.where(Dish.id == dish_id)

    result = await session.execute(query)
    dishes = result.scalars().all()
    return dishes if dishes else None


async def get_dish_detailed_info(session: AsyncSession, dish_id: int):
    """
    Retrieves detailed information about a Dish including related Restaurant and Category details.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session.
        dish_id (int): The ID of the Dish to retrieve.

    Returns:
        dict: A dictionary containing detailed information about the Dish.
    """
    # Construct the query to fetch the Dish with related Restaurant and Category
    query = select(Dish).options(
        selectinload(Dish.restaurant),
        selectinload(Dish.category)
    ).where(Dish.id == dish_id)

    # Execute the query
    result = await session.execute(query)
    dish = result.scalars().first()

    if not dish:
        return None  # or raise an exception if preferred

    # Construct the detailed information dictionary
    dish_details = {
        "id": dish.id,
        "restaurant_name": dish.restaurant.name,
        "category_name": dish.category.name,
        "name": dish.name,
        "photo": dish.photo,
        "description": dish.description,
        "price": dish.price,
        "extra": dish.extra
    }

    return dish_details

#
# async def create_user(session: AsyncSession, restaurant_id: int, table_id: int):
#     """
#     Creates a new User and an associated Basket in the database.
#
#     Args:
#         session (AsyncSession): The SQLAlchemy asynchronous session.
#         table_id (int): The table ID where the user is seated.
#         restaurant_id (int): The ID of the restaurant the user is associated with.
#
#     Returns:
#         Tuple[User, Basket]: A tuple containing the created User and Basket objects.
#     """
#     # Create a new User
#     user = User(restaurant_id=restaurant_id, table_id=table_id)
#     session.add(user)
#     await session.flush()  # Ensure the user gets an ID
#
#     # Create a new Basket associated with the new User
#     basket = Basket(user_id=user.id)
#     session.add(basket)
#     await session.commit()
#
#     return user, basket
#
#
# async def create_order(session: AsyncSession, user_id: int, dish_id: int, extra: Optional[dict] = None):
#     """
#     Creates a new order and adds it to the user's basket.
#
#     Args:
#         session (AsyncSession): The SQLAlchemy asynchronous session.
#         user_id (int): The ID of the user.
#         dish_id (int): The ID of the dish being ordered.
#         extra (Optional[dict]): Additional information about the order.
#
#     Returns:
#         Order: The created Order object.
#     """
#     # Create the new order
#     order = Order(user_id=user_id, dish_id=dish_id, extra=extra)
#     session.add(order)
#     await session.flush()  # To get the order's primary key
#
#     # Find the basket for the user and add the order to it
#     basket_query = await session.execute(
#         select(Basket).where(Basket.user_id == user_id)
#     )
#     basket = basket_query.scalars().first()
#     if not basket:
#         # Create a new Basket if it doesn't exist
#         basket = Basket(user_id=user_id)
#         session.add(basket)
#         await session.flush()  # To get the basket's primary key
#
#     basket.orders.append(order)
#     await session.commit()
#     return order
#
#
# async def get_basket_orders(session: AsyncSession, user_id: int):
#     """
#     Retrieves all orders in a user's basket.
#
#     Args:
#         session (AsyncSession): The SQLAlchemy asynchronous session.
#         user_id (int): The ID of the user.
#
#     Returns:
#         List[Order]: A list of Order objects in the user's basket.
#     """
#
#     # Find the user for the given user_id
#     user_query = await session.execute(
#         select(User).where(User.id == user_id)
#     )
#     user = user_query.scalars().first()
#     if not user:
#         return []
#
#     # Find the basket for the user
#     basket_query = await session.execute(
#         select(Basket).options(selectinload(Basket.orders)).where(Basket.user_id == user_id)
#     )
#     basket = basket_query.scalars().first()
#     if basket:
#         return basket.orders
#     return []
#
#
# async def create_completed_basket(session: AsyncSession, user_id: int):
#     """
#     Creates a new CompletedBasket record for the given user_id.
#
#     Args:
#         session (AsyncSession): The SQLAlchemy asynchronous session.
#         user_id (int): The user ID for which to create the CompletedBasket.
#
#     Returns:
#         CompletedBasket: The created CompletedBasket object.
#     """
#     # Fetch the User record to get the fetching_time and table_id
#     user_query = await session.execute(
#         select(User).where(User.id == user_id)
#     )
#     user = user_query.scalars().first()
#     if not user:
#         raise ValueError(f"No user found for user_id: {user_id}")
#
#     # Fetch the Restaurant record to get the restaurant_name
#     restaurant_query = await session.execute(
#         select(Restaurant).where(Restaurant.id == user.restaurant_id)
#     )
#     restaurant = restaurant_query.scalars().first()
#     if not restaurant:
#         raise ValueError(f"No restaurant found for restaurant_id: {user.restaurant_id}")
#
#     # Fetch the Basket record to get the list of orders
#     basket_query = await session.execute(
#         select(Basket).options(selectinload(Basket.orders)).where(Basket.user_id == user_id)
#     )
#     basket = basket_query.scalars().first()
#     if not basket:
#         raise ValueError(f"No basket found for user_id: {user_id}")
#
#     # Extract dish_id and extras from each order
#     orders_data = [(order.dish_id, order.extra) for order in basket.orders]
#
#     # Create a new CompletedBasket record
#     completed_basket = CompletedBasket(
#         restaurant_name=restaurant.name,
#         table_id=user.table_id,
#         orders_time=user.time,
#         orders_data=orders_data
#     )
#     session.add(completed_basket)
#     await session.commit()
#     await session.refresh(completed_basket)
#
#     return completed_basket
#
#
# async def delete_user(session: AsyncSession, table_id: int):
#     """
#     Deletes a user from the database.
#
#     Args:
#         session (AsyncSession): The SQLAlchemy asynchronous session.
#         table_id (int): The table ID where the user is seated.
#
#     Returns:
#         bool: True if the user was deleted successfully, False otherwise.
#     """
#     user_query = await session.execute(
#         select(User).where(User.table_id == table_id)
#     )
#     user = user_query.scalars().first()
#     if user:
#         await session.delete(user)
#         await session.commit()
#         return True
#     return False
