from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Tuple
from datetime import datetime
from decimal import Decimal
import uuid


class DishSchema(BaseModel):
    id: int
    restaurant_id: int
    category_id: Optional[int] = None
    name: str
    photo: Optional[str] = None
    description: Optional[str] = None
    price: Decimal = Field(..., description="Price in decimal with 2 digits precision")
    currency: Optional[str] = None
    extra: Optional[Dict] = None

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: f"{v:.2f}"  # Ensure Decimal values are formatted to 2 decimal places
        }


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RestaurantSchema(BaseModel):
    id: int
    name: str
    photo: Optional[str]
    rating: Optional[Decimal]
    tables_amount: Optional[int]

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, value):
        if value is not None:
            return round(value, 1)
        return value

    class Config:
        from_attributes = True


class OrderItem(BaseModel):
    dish_id: int
    extras: Dict[str, Tuple[str, float]]


class OrderRequest(BaseModel):
    restaurant_id: int
    table_id: int
    order_datetime: datetime
    order_items: List[OrderItem]


class WaiterCallCreateRequest(BaseModel):
    restaurant_id: int = Field(..., description="ID of the restaurant")
    table_id: int = Field(..., description="ID of the table")
    status: str = Field(..., description="Status of the waiter call")

    @field_validator('status')
    def check_status(cls, v):
        allowed_statuses = {"call", "clean", "check"}
        if v not in allowed_statuses:
            raise ValueError(f"Invalid status: {v}. Allowed statuses are: {', '.join(allowed_statuses)}")
        return v


class WaiterCallResponse(BaseModel):
    id: uuid.UUID = Field(..., description="Unique identifier of the waiter call")
    restaurant_id: int = Field(..., description="ID of the restaurant")
    table_id: int = Field(..., description="ID of the table")
    status: str = Field(..., description="Status of the waiter call")
#
# class UserBasketResponse(BaseModel):
#     user_id: int
#     restaurant_id: int
#     table_id: int
#     basket_id: int
#
#
# class OrderCreate(BaseModel):
#     user_id: int
#     dish_id: int
#     extra: Optional[Dict] = None
#
#
# class OrderSchema(BaseModel):
#     user_id: int
#     table_id: int
#     dish_id: int
#     extra: Optional[Dict] = None
#
#     class Config:
#         from_attributes = True
#
#
# class BasketView(BaseModel):
#     id: int
#     user_id: int
#     orders: List[OrderSchema]
#
#     class Config:
#         from_attributes = True

