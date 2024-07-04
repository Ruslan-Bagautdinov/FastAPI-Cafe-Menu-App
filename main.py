from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware


# own_import
from app.database.postgre_db import init_db

# routers
from app.routers import (get_all_restaurants,
                         get_all_categories,
                         get_restaurant_by_id,
                         get_dishes,
                         get_dish_details,
                         calculate_basket,
                         call_waiter,
                         add_mock_dishes,
                         get_image)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(get_all_restaurants.router, prefix="/all_restaurants", tags=["all_restaurants"])
app.include_router(get_all_categories.router, prefix="/all_categories", tags=["all_categories"])
app.include_router(get_restaurant_by_id.router, prefix="/restaurant", tags=["restaurant"])
app.include_router(get_dishes.router, prefix="/dishes", tags=["dishes"])
app.include_router(get_dish_details.router, prefix="/dish_details", tags=["dish_details"])
app.include_router(calculate_basket.router, prefix="/calculate_basket", tags=["calculate_basket"])
app.include_router(call_waiter.router, prefix="/call_waiter", tags=["call_waiter"])


app.include_router(get_image.router, prefix="/images", tags=["images"])

app.include_router(add_mock_dishes.router, prefix="/add_mock_dishes", tags=["add_mock_dishes"])


@app.get("/")
async def root():
    return RedirectResponse(url='/docs')
