import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession
                                    )
from sqlalchemy import text
from app.database.models import Base, Restaurant, Dish, Category
from app.database.crud import (
    get_restaurant_id_name_pairs,
    get_category_id_name_pairs,
    get_restaurant_by_id,
    get_dishes_by_restaurant_and_category_and_id,
    get_dish_detailed_info,
    get_dish_basket_info
)

from app.config import TEST_DB_URL

DATABASE_URL = TEST_DB_URL

@pytest_asyncio.fixture(scope="module")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="module")
async def async_session():
    engine = create_async_engine(TEST_DB_URL, future=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    await engine.dispose()

@ pytest_asyncio.fixture
async def setup_data(async_session):
    # Clean up and initialize database
    await async_session.execute(text("TRUNCATE TABLE restaurants, categories, dishes RESTART IDENTITY"))
    await async_session.commit()

    # Add initial data here
    restaurant = Restaurant(id=1, name="Test Restaurant", rating=4.5, currency="USD", tables_amount=10)
    category = Category(id=1, name="Test Category")
    dish = Dish(restaurant_id=1, category_id=1, name="Test Dish", price=10.0, description="A test dish")

    async_session.add(restaurant)
    await async_session.commit()
    async_session.add(category)
    await async_session.commit()
    async_session.add(dish)
    await async_session.commit()

@pytest.mark.asyncio
async def test_get_restaurant_id_name_pairs(async_session, setup_data):
    result = await get_restaurant_id_name_pairs(async_session)
    assert result == {1: "Test Restaurant"}

@pytest.mark.asyncio
async def test_get_category_id_name_pairs(async_session, setup_data):
    result = await get_category_id_name_pairs(async_session, restaurant_id=1)
    assert result == {1: "Test Category"}

@pytest.mark.asyncio
async def test_get_restaurant_by_id(async_session, setup_data):
    result = await get_restaurant_by_id(async_session, restaurant_id=1)
    assert result.name == "Test Restaurant"

@pytest.mark.asyncio
async def test_get_dishes_by_restaurant_and_category_and_id(async_session, setup_data):
    result = await get_dishes_by_restaurant_and_category_and_id(async_session, restaurant_id=1, category_id=1, dish_id=1)
    assert result[0]["name"] == "Test Dish"

@pytest.mark.asyncio
async def test_get_dish_detailed_info(async_session, setup_data):
    result = await get_dish_detailed_info(async_session, dish_id=1)
    assert result["name"] == "Test Dish"

@pytest.mark.asyncio
async def test_get_dish_basket_info(async_session, setup_data):
    result = await get_dish_basket_info(async_session, dish_id=1)
    assert result["name"] == "Test Dish"
