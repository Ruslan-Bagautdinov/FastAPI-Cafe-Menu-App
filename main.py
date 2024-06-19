from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

# own_import
from app.database.postgre_db import init_db

from app.routers import (get_all_restaurants,
                         get_all_categories,
                         get_restaurant_by_id,
                         get_dishes,
                         get_dish_details,
                         get_image,
                         create_new_user,
                         get_basket,
                         create_new_order
                         )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(get_all_restaurants.router, prefix="/all_restaurants", tags=["all_restaurants"])
app.include_router(get_all_categories.router, prefix="/all_categories", tags=["all_categories"])
app.include_router(get_restaurant_by_id.router, prefix="/restaurant", tags=["restaurant"])
app.include_router(get_dishes.router, prefix="/dishes", tags=["dishes"])
app.include_router(get_dish_details.router, prefix="/dish_details", tags=["dish_details"])
app.include_router(get_image.router, prefix="/images", tags=["images"])
# app.include_router(create_new_user.router, prefix="/users", tags=["users"])
# app.include_router(get_basket.router, prefix="/baskets", tags=["baskets"])
# app.include_router(create_new_order.router, prefix="/orders", tags=["orders"])



@app.get("/")
async def root():
    return RedirectResponse(url='/docs')
