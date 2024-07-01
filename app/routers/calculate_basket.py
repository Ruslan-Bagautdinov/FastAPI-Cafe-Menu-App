from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal, ROUND_HALF_UP

from app.database.postgre_db import get_session
from app.database.models import Basket, Restaurant
from app.database.schemas import (OrderRequestSave,
                                  OrderItemSave,
                                  OrderRequestReturn,
                                  OrderItemReturn
                                  )
from app.database.crud import get_dish_detailed_info, format_extra_prices

router = APIRouter()


@router.post("/")
async def calculate_cost(order_request: OrderRequestSave, session: AsyncSession = Depends(get_session)):
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
    order_items = [OrderItemSave(dish_id=item['dish_id'], extras=format_extra_prices(item['extras'])).dict() for item in
                   order_items_jsonable]
    basket = Basket(
        restaurant_id=order_request.restaurant_id,
        table_id=order_request.table_id,
        order_datetime=order_request.order_datetime,
        order_items=order_items,
        total_cost=total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        currency=restaurant_currency,
        status="None",
        waiter=None
    )
    session.add(basket)
    await session.flush()
    await session.commit()

    # Convert order_items to OrderItemReturn for the response
    order_items_return = [OrderItemReturn(dish_id=item['dish_id'], extras={key: (name, str(Decimal(price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))) for key, (name, price) in item['extras'].items()}).dict() for item in order_items_jsonable]
    print(order_items_return)

    return {
        "basket_id": basket.id,
        "restaurant_id": order_request.restaurant_id,
        "table_id": order_request.table_id,
        "order_datetime": order_request.order_datetime,
        "order_items": order_items_return,
        "total_cost": f"{total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}",
        "currency": restaurant_currency
    }

