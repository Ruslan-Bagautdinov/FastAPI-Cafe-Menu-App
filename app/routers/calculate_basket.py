from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
import json

from app.database.postgre_db import get_session
from app.database.models import Basket
from app.database.schemas import OrderRequest
from app.database.crud import (get_dishes_by_restaurant_and_category_and_id,
                               get_dish_detailed_info)

router = APIRouter()


@router.post("/")
async def calculate_cost(order_request: OrderRequest, session: AsyncSession = Depends(get_session)):
    """
    Calculate the total cost of orders based on the provided order request and save the details into the 'baskets' table.

    Args:
        order_request (OrderRequest): The request containing the restaurant ID, table ID, order datetime,
        and list of orders.
        session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

    Returns:
        dict: A dictionary containing the restaurant ID, table ID, order datetime, list of orders
        and the total cost of the orders.

    Raises:
        HTTPException: 404 error if no dishes are found for the given restaurant and dish IDs.

    This endpoint performs the following steps:
    1. Iterates through each order item in the order request.
    2. Retrieves detailed information about each dish using the `get_dish_detailed_info` function.
    3. If a dish is not found, raises a 404 HTTPException.
    4. Calculates the total cost of the dishes, including any extras.
    5. Creates a new `Basket` instance with the calculated total cost and other order details.
    6. Adds the `Basket` instance to the database session and commits it.
    7. Returns a dictionary with the restaurant ID, table ID, order datetime, and total cost.
    """
    total_cost = Decimal('0.0')

    for order in order_request.order_items:
        dish = await get_dish_detailed_info(session, dish_id=order.dish_id)
        if not dish:
            raise HTTPException(status_code=404,
                                detail=f"Dish with ID {order.dish_id} not found for restaurant {order_request.restaurant_id}")

        dish_cost = Decimal(str(dish["price"]))
        for extra, (_, extra_cost) in order.extras.items():
            dish_cost += Decimal(str(extra_cost))
        total_cost += dish_cost

    order_items_jsonable = jsonable_encoder(order_request.order_items)
    order_items = order_items_jsonable

    # order_items = json.dumps(order_items_jsonable)

    basket = Basket(
        restaurant_id=order_request.restaurant_id,
        table_id=order_request.table_id,
        order_datetime=order_request.order_datetime,
        order_items=order_items,
        total_cost=total_cost,
        status="None",
        waiter=None
    )
    session.add(basket)
    await session.commit()

    return {
        "restaurant_id": order_request.restaurant_id,
        "table_id": order_request.table_id,
        "order_datetime": order_request.order_datetime,
        "order_items": order_items,
        "total_cost": total_cost
    }
