# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
#
# # own imports
# from app.database.postgre_db import get_session
# from app.database.crud import create_user
# from app.database.schemas import UserSchema
#
# router = APIRouter()
#
#
# @router.post("/", response_model=UserSchema)
# async def create_new_user(restaurant_id: int, table_id: int, session: AsyncSession = Depends(get_session)):
#     """
#     Creates a new user and an associated basket in the database.
#
#     Args:
#         restaurant_id (int): The ID of the restaurant the user is associated with.
#         table_id (int): The table ID where the user is seated.
#         session (AsyncSession): The SQLAlchemy asynchronous session, obtained from the dependency.
#
#     Returns:
#         UserSchema: The created User object.
#     """
#     try:
#         user = await create_user(session, restaurant_id, table_id)
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
