from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.database.postgre_db import get_session
from app.database.schemas import OrderRequest
from app.database.crud import get_dishes_by_restaurant_and_category_and_id

router = APIRouter()

@router.post("/calculate-cost/")
async def calculate_cost(order_request: OrderRequest,
                         session: AsyncSession = Depends(get_session)):
    total_cost = 0.0

    for order in order_request.orders:

        dish = await get_dishes_by_restaurant_and_category_and_id(session, order.dish_id)

        dish_cost = 0.0  # Assume this is fetched or known based on dish_id

        for extra, (_, extra_cost) in order.extras.items():
            dish_cost += extra_cost
        total_cost += dish_cost

    return {"restaurant_id": order_request.restaurant_id,
            "table_id": order_request.table_id,
            "total_cost": total_cost}