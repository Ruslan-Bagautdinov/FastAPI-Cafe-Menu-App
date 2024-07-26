# FastAPI Cafe Menu App

This FastAPI application serves as the backend for a React app, providing an interactive menu for cafes and restaurants. Visitors can scan a QR code on their table to access the menu, make orders, and call for a waiter.

## Features

- **Restaurant Menu**: Retrieve restaurant details, categories, dishes, and dish details.
- **Order Calculation**: Calculate the total price of the basket.
- **Waiter Call**: Call a waiter to clean the table or give a check.
- **Image Retrieval**: Retrieve images of dishes and restaurants.
- **Mock Data**: Add mock dishes for testing purposes.

## Setup

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/fastapi-cafe-menu-app.git
   cd fastapi-cafe-menu-app
   ```

2. Create a virtual environment and activate it:

   ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```sh
    pip install -r requirements.txt
   ```

4. Set up your environment variables by creating a .env file in the root directory with the following content:

   ```dotenv
    WORK_DATABASE_URL=your_work_database_url
    LOCAL_DATABASE_URL=your_local_database_url
    TEST_DB_URL=your_test_database_url
    HOME_DB=False
   ```

5. Run the application:

   ```sh
    uvicorn main:app --reload
   ```

## API Endpoints

### Restaurants

- GET /all_restaurants: Retrieves a dictionary mapping restaurant IDs to their names.

- GET /restaurant: Retrieves a restaurant by its ID.


### Categories
- GET /all_categories: Retrieves all categories.

### Dishes
- GET /dishes: Retrieves dishes.

- GET /dish_details: Retrieves dish details.

### Basket
- GET /calculate_basket: Calculates the total price of the basket.

### Waiter
- GET /call_waiter: Calls a waiter.

### Images
- GET /images: Retrieves an image.

### Mock Data
- GET /add_mock_dishes: Adds mock dishes.

Contributing
Contributions are welcome! Please open an issue or submit a pull request.

License:
This project is not licensed.