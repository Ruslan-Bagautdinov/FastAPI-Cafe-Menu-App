from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

# Own imports
from app.database.postgre_db import init_db
from app.routers import (
    get_all_restaurants,
    get_all_categories,
    get_restaurant_by_id,
    get_dishes,
    get_dish_details,
    calculate_basket,
    call_waiter,
    add_mock_dishes,
    get_image
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the FastAPI application lifespan.
    Initializes the database connection on startup.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    await init_db()
    yield

# Application description
app_description = """
FastAPI Cafe Menu App is a backend service for a React app, providing an interactive menu for cafes and restaurants.
Visitors can scan a QR code on their table to access the menu, make orders, and call for a waiter.

## Features

- **Restaurant Menu**: Retrieve restaurant details, categories, dishes, and dish details.
- **Order Calculation**: Calculate the total price of the basket.
- **Waiter Call**: Call a waiter to clean the table or give a check.
- **Image Retrieval**: Retrieve images of dishes and restaurants.
- **Mock Data**: Add mock dishes for testing purposes.
"""

app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Cafe Menu App",
    description=app_description,
    version="1.0.0",
    contact={
        "name": "Developer Name",
        "url": "https://github.com/yourusername/fastapi-cafe-menu-app",
        "email": "developer@example.com",
    },
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
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
    """
    Root endpoint that redirects to the API documentation.

    Returns:
        RedirectResponse: Redirects to the '/docs' endpoint.
    """
    return RedirectResponse(url='/docs')