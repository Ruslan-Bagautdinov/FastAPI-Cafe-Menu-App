from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import WaiterCall
from app.database.schemas import WaiterCallCreateRequest, WaiterCallResponse
from app.database.postgre_db import get_session

router = APIRouter()


@router.post("/", response_model=WaiterCallResponse)
async def create_or_update_waiter_call(
    waiter_call_request: WaiterCallCreateRequest,
    session: AsyncSession = Depends(get_session)
):
    """
        Creates a new waiter call or updates the status of an existing waiter call for a specific table in a restaurant.

        Args:
            waiter_call_request (WaiterCallCreateRequest): The request body containing the details of the waiter call.
            {
                "restaurant_id": 7,
                "table_id": 15,
                "status": "call" or "clean" or "check"
                "call_datetime": "2021-08-02T00:00:00Z",
            }
            session (AsyncSession): The SQLAlchemy asynchronous session.

        Returns:
            WaiterCallResponse: A response model containing the details of the created or updated waiter call.
        """

    query = select(WaiterCall).where(
        WaiterCall.restaurant_id == waiter_call_request.restaurant_id,
        WaiterCall.table_id == waiter_call_request.table_id
    )
    result = await session.execute(query)
    existing_call = result.scalar_one_or_none()

    if existing_call:
        existing_call.call_datetime = waiter_call_request.call_datetime
        existing_call.status = waiter_call_request.status
        await session.commit()
        await session.refresh(existing_call)
        return existing_call
    else:
        new_call = WaiterCall(
            call_datetime = waiter_call_request.call_datetime,
            restaurant_id=waiter_call_request.restaurant_id,
            table_id=waiter_call_request.table_id,
            status=waiter_call_request.status
        )
        session.add(new_call)
        await session.commit()
        await session.refresh(new_call)
        return new_call
