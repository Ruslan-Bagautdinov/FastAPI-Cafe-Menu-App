from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal, ROUND_HALF_UP

from app.database.postgre_db import get_session
from app.database.models import Basket, Restaurant
from app.database.schemas import (OrderRequest,
                                  OrderItemResponse,
                                  CalculateCostResponse)
from app.database.crud import get_dish_detailed_info

router = APIRouter()


@router.post("/", response_model=CalculateCostResponse, description="Calculates the total cost of an order and returns detailed order information.")
async def calculate_cost(order_request: OrderRequest, session: AsyncSession = Depends(get_session)):
    """
    Calculates the total cost of an order and returns detailed order information.

    Args:
        order_request (OrderRequestSave): The request body containing order details.
        session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

    Returns:
        CalculateCostResponse: A response object containing the basket ID, restaurant ID, table ID, order datetime,
        detailed order items with dish prices, total cost, and currency.
    """
    total_cost = Decimal('0.0')
    restaurant_currency = None
    order_items_response = []

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
            dish_cost += Decimal(extra_cost)
        total_cost += dish_cost

        # Include dish price in the response
        order_items_response.append(OrderItemResponse(
            dish_id=order.dish_id,
            dish_price=f"{Decimal(str(dish['price'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}",
            extras=order.extras
        ))

    basket = Basket(
        restaurant_id=order_request.restaurant_id,
        table_id=order_request.table_id,
        order_datetime=order_request.order_datetime,
        order_items=jsonable_encoder(order_items_response),
        total_cost=total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        currency=restaurant_currency,
        status="None",
        waiter=None
    )
    session.add(basket)
    await session.flush()
    await session.commit()

    print(order_items_response)

    return CalculateCostResponse(
        basket_id=basket.id,
        restaurant_id=order_request.restaurant_id,
        table_id=order_request.table_id,
        order_datetime=order_request.order_datetime,
        order_items=order_items_response,
        total_cost=f"{total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}",
        currency=restaurant_currency
    )
