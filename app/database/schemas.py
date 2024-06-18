from pydantic import BaseModel, Field, RootModel
from typing import Optional, List, Dict


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

