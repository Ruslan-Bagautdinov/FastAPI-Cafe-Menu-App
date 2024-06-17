from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.postgre_db import get_session
from app.database.crud import get_restaurant_id_name_pairs

router = APIRouter()


@router.get("/restaurants/id-name-pairs")
async def get_id_name_pairs(session: AsyncSession = Depends(get_session)):
    pairs = await get_restaurant_id_name_pairs(session)
    return pairs
