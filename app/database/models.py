from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, Dict, Tuple
from datetime import datetime


# own import
from app.database.postgre_db import Base


class Restaurant(Base):
    __tablename__ = 'restaurants'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[float] = mapped_column()

    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='restaurant', cascade='all, delete-orphan')


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='category')


class Dish(Base):
    __tablename__ = 'dishes'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id', ondelete='CASCADE'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    extra: Mapped[dict] = mapped_column(JSON)

    restaurant: Mapped['Restaurant'] = relationship('Restaurant', back_populates='dishes')
    category: Mapped['Category'] = relationship('Category', back_populates='dishes')


class User(Base):
    __tablename__ = 'users'

    table_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'), nullable=False)
    time: Mapped[datetime] = mapped_column(default=datetime.now)


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    table_id: Mapped[int] = mapped_column(ForeignKey('users.table_id', ondelete='CASCADE'), nullable=False)
    dish_id: Mapped[int] = mapped_column(ForeignKey('dishes.id'), nullable=False)
    extra: Mapped[dict] = mapped_column(JSON, nullable=True)

    dish: Mapped['Dish'] = relationship('Dish', backref='orders')


class Basket(Base):
    __tablename__ = 'baskets'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    table_id: Mapped[int] = mapped_column(ForeignKey('users.table_id', ondelete='CASCADE'), nullable=False)

    orders: Mapped[List['Order']] = relationship('Order', backref='basket')


class CompletedBasket(Base):
    __tablename__ = 'completed_baskets'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    table_id: Mapped[int] = mapped_column(ForeignKey('users.table_id', ondelete='CASCADE'), nullable=False)
    fetching_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    orders_data: Mapped[List[Tuple[int, dict]]] = mapped_column(JSON, nullable=False)