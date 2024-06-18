from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.postgre_db import get_session
from app.database.crud import create_order
from app.database.models import Order
from app.database.schemas import OrderCreate, OrderSchema

router = APIRouter()


@router.post("/", response_model=OrderSchema)
async def create_new_order(order: OrderCreate, session: AsyncSession = Depends(get_session)):
    """
    Creates a new order and adds it to the user's basket.

    Args:
        order (OrderCreate): The order data including table_id, dish_id, and extra information.
        session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

    Returns:
        OrderSchema: The created Order object.
    """
    try:
        created_order = await create_order(session, order.table_id, order.dish_id, order.extra)
        return created_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
