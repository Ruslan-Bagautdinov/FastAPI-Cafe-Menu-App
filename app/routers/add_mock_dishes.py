from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
import random

from app.database.postgre_db import get_session
from app.database.models import Dish
from app.database.crud import (get_dishes_by_restaurant_and_category_and_id,
                               get_restaurant_by_id,
                               get_category_id_name_pairs)

router = APIRouter()


@router.get("/")
async def add_mock_dishes(restaurant_id: int, i: int, session: AsyncSession = Depends(get_session)):
    """
        Generate mock dishes for a specified restaurant and save them into the 'dishes' table.

        Args:
            restaurant_id (int): The ID of the restaurant for which mock dishes are to be generated.
            i (int): The number of mock dishes to generate for each category.
            session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

        Returns:
            dict: A dictionary containing the restaurant ID, the number of categories, and the number of dishes added.

        Raises:
            HTTPException: 404 error if the restaurant or categories are not found.
        """

    # Fetch the restaurant name
    restaurant = await get_restaurant_by_id(session, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant_name = restaurant.name

    # Fetch the categories for the restaurant
    category_id_name_pairs = await get_category_id_name_pairs(session=session)
    if not category_id_name_pairs:
        raise HTTPException(status_code=404, detail="No categories found for the restaurant")

    # Fetch the existing dishes for the restaurant
    dishes = await get_dishes_by_restaurant_and_category_and_id(session, restaurant_id=restaurant_id)
    existing_dish_names = {dish.name for dish in dishes} if dishes else set()

    # Define adjectives, main ingredients, cuisine styles, cooking methods, accompaniments, and flavors
    adjectives = ["delicious", "exquisite", "mouth-watering", "succulent", "flavorful"]
    main_ingredients = ["chicken", "beef", "vegetable", "seafood", "pork"]
    cuisine_styles = ["Italian", "Chinese", "French", "Japanese", "Mexican"]
    cooking_methods = ["grilled", "steamed", "fried", "baked", "roasted"]
    accompaniments = ["rice", "noodles", "bread", "salad", "soup"]
    flavors = ["sweet and sour", "spicy", "savory", "tangy", "rich"]

    dish_count = 0
    categories_amount = len(category_id_name_pairs)

    # Generate mock dishes
    for category_id, category_name in category_id_name_pairs.items():
        for j in range(i):  # i records for each category
            dish_name = f"{restaurant_name} {category_name} {j + 1}"
            # Ensure the dish name is unique
            while dish_name in existing_dish_names:
                j += 1
                dish_name = f"{restaurant_name} {category_name} {j + 1}"
            existing_dish_names.add(dish_name)

            description = f"Indulge in our {dish_name}, a {random.choice(adjectives)} {random.choice(main_ingredients)} dish, expertly crafted by our chef. This {random.choice(cuisine_styles)} specialty is {random.choice(cooking_methods)} to perfection, and served with {random.choice(accompaniments)}. A harmonious blend of {random.choice(flavors)}, it’s a true celebration of taste that promises to delight your palate."
            price = Decimal(random.uniform(1, 20)).quantize(Decimal('0.01'))
            extras = {
                "1": [f"{restaurant_name}-1", 0.69],
                "2": [f"{restaurant_name}-2", 0.99],
                "3": [f"{restaurant_name}-3", 1.99],
                "4": [f"{restaurant_name}-4", 2.99],
                "5": [f"{restaurant_name}-5", 3.99],
                "6": [f"{restaurant_name}-6", 4.99],
                "7": [f"{restaurant_name}-7", 5.99],
                "8": [f"{restaurant_name}-8", 6.99],
                "9": [f"{restaurant_name}-9", 7.99]
            }

            new_dish = Dish(
                restaurant_id=restaurant_id,
                category_id=category_id,
                name=dish_name,
                description=description,
                price=float(price),
                extra=extras
            )
            session.add(new_dish)
            dish_count += 1

    await session.commit()

    return {"message": f"Added {dish_count} dishes in {categories_amount} categories in restaurant {restaurant_name}"}
