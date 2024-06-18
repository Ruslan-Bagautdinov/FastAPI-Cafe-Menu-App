from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# own import
from app.database.postgre_db import get_session
from app.database.crud import get_category_id_name_pairs

router = APIRouter()


@router.get("/")
async def get_id_category_pairs(session: AsyncSession = Depends(get_session)):
    """
    Retrieves a dictionary mapping category IDs to their names.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.

    Returns:
        dict: A dictionary where keys are category IDs and values are category names.
    """
    pairs = await get_category_id_name_pairs(session)
    return {"restaurants": pairs}
