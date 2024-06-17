from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

# own_import
from app.database.postgre_db import init_db

from app.routers import (get_restaurant_by_id,
                         get_restaurant_by_name,
                         get_all_dishes,
                         get_dishes_by_category,
                         get_image
                         )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(get_restaurant_by_id.router, prefix="/restaurants/id", tags=["restaurants-by-id"])
app.include_router(get_restaurant_by_name.router, prefix="/restaurants/name", tags=["restaurants-by-name"])
app.include_router(get_all_dishes.router, prefix="/dishes", tags=["dishes"])
app.include_router(get_dishes_by_category.router, prefix="/dishes", tags=["dishes"])
app.include_router(get_image.router, prefix="/images", tags=["images"])

@app.get("/")
async def root():
    return RedirectResponse(url='/docs')
