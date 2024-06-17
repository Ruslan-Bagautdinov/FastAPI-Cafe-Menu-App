from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database.postgre_db import Base


class Restaurant(Base):
    __tablename__ = 'restaurants'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column()
    rating: Mapped[float] = mapped_column()

    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='restaurant', cascade='all, delete-orphan')


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='category')


class Dish(Base):
    __tablename__ = 'dishes'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id', ondelete='CASCADE'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column(nullable=False)
    extra: Mapped[dict] = mapped_column(JSON)

    restaurant: Mapped['Restaurant'] = relationship('Restaurant', back_populates='dishes')
    category: Mapped['Category'] = relationship('Category', back_populates='dishes')
