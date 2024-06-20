from sqlalchemy import (Column,
                        Integer,
                        ForeignKey,
                        DateTime,
                        JSON,
                        String,
                        Numeric,
                        Enum)

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid


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


class Basket(Base):
    __tablename__ = 'baskets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(Integer, nullable=False)
    table_id = Column(Integer, nullable=False)
    order_datetime = Column(DateTime, nullable=False)
    order_items = Column(JSONB, nullable=True)
    total_cost = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum("None", "in work", "complete", name="status_enum"), default="None")
    waiter = Column(String, nullable=True)
