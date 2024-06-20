from pydantic import BaseModel
from typing import Optional, List, Dict, Tuple
from datetime import datetime


class DishSchema(BaseModel):
    id: int
    restaurant_id: int
    category_id: Optional[int]
    name: str
    photo: Optional[str]
    description: Optional[str]
    price: float
    extra: Optional[Dict]

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RestaurantSchema(BaseModel):
    id: int
    name: str
    photo: Optional[str]
    rating: Optional[float]

    class Config:
        from_attributes = True


class OrderItem(BaseModel):
    dish_id: int
    extras: Dict[str, Tuple[str, float]]


class OrderRequest(BaseModel):
    restaurant_id: int
    table_id: int
    order_datetime: datetime
    orders: List[OrderItem]

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
