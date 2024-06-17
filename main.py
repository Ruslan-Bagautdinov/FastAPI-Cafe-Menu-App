from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

# own_import
from app.database.postgre_db import init_db

from app.routers import (get_restaurant,
                         get_all_dishes,
                         get_image
                         )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(get_restaurant.router, prefix="/restaurants", tags=["restaurants"])
app.include_router(get_all_dishes.router, prefix="/dishes", tags=["dishes"])
app.include_router(get_image.router, prefix="/images", tags=["images"])

@app.get("/")
async def root():
    return RedirectResponse(url='/docs')
