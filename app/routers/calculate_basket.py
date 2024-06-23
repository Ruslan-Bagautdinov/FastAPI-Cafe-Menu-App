from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from app.database.postgre_db import get_session
from app.database.models import Basket, Restaurant
from app.database.schemas import OrderRequest
from app.database.crud import get_dish_detailed_info

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
        dict: A dictionary containing the restaurant ID, table ID, order datetime, list of orders,
        the total cost of the orders, currency used in restaurant, and the Basket ID.

    Raises:
        HTTPException: 404 error if no dishes are found for the given restaurant and dish IDs.

    """
    total_cost = Decimal('0.0')
    restaurant_currency = None

    for order in order_request.order_items:
        dish = await get_dish_detailed_info(session, dish_id=order.dish_id)
        if not dish:
            raise HTTPException(status_code=404,
                                detail=f"Dish with ID {order.dish_id} not found for restaurant {order_request.restaurant_id}")

        if not restaurant_currency:
            restaurant = await session.get(Restaurant, order_request.restaurant_id)
            if not restaurant:
                raise HTTPException(status_code=404, detail=f"Restaurant with ID {order_request.restaurant_id} not found")
            restaurant_currency = restaurant.currency

        dish_cost = Decimal(str(dish["price"]))
        for extra, (_, extra_cost) in order.extras.items():
            dish_cost += Decimal(str(extra_cost))
        total_cost += dish_cost

    order_items_jsonable = jsonable_encoder(order_request.order_items)
    order_items = order_items_jsonable

    basket = Basket(
        restaurant_id=order_request.restaurant_id,
        table_id=order_request.table_id,
        order_datetime=order_request.order_datetime,
        order_items=order_items,
        total_cost=total_cost,
        currency=restaurant_currency,
        status="None",
        waiter=None
    )
    session.add(basket)
    await session.flush()
    await session.commit()


    return {
        "basket_id": basket.id,
        "restaurant_id": order_request.restaurant_id,
        "table_id": order_request.table_id,
        "order_datetime": order_request.order_datetime,
        "order_items": order_items,
        "total_cost": total_cost,
        "currency": restaurant_currency
    }
