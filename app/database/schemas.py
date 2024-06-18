from pydantic import BaseModel
from typing import Optional, List, Dict
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


class UserSchema(BaseModel):
    table_id: int
    restaurant_id: int
    time: datetime

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    table_id: int
    dish_id: int
    extra: Optional[Dict] = None


class OrderSchema(BaseModel):
    id: int
    table_id: int
    dish_id: int
    extra: Optional[Dict] = None

    class Config:
        from_attributes = True


class BasketView(BaseModel):
    id: int
    table_id: int
    orders: List[OrderSchema]

    class Config:
        from_attributes = True
