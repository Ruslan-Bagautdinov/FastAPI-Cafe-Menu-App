from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# own import
from app.database.postgre_db import get_session
from app.database.crud import get_basket_orders
from app.database.models import Basket
from app.database.schemas import BasketView


router = APIRouter()


@router.get("/",
            response_model=BasketView,
            description="Retrieve all orders in a user's basket.")
async def get_basket(user_id: int = Query(..., description="The table ID where the user is seated."),
                     session: AsyncSession = Depends(get_session)):
    """
    Retrieves all orders in a user's basket.

    Args:
        user_id (int): The ID of the user.
        session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

    Returns:
        BasketView: The basket and its orders.
    """
    try:
        orders = await get_basket_orders(session, user_id)
        basket = await session.execute(select(Basket).where(Basket.user_id == user_id))
        basket = basket.scalars().first()
        if not basket:
            raise HTTPException(status_code=404, detail="Basket not found")
        return BasketView(id=basket.id, user_id=basket.user_id, orders=orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
