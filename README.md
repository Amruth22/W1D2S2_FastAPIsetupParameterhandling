# FastAPI Parameter Handling Demo

This project demonstrates FastAPI setup, parameter handling, and request processing with comprehensive examples.

## Features

1. **FastAPI Setup**
   - Basic FastAPI application initialization
   - Uvicorn server integration
   - API documentation with Swagger UI and ReDoc

2. **Parameter Handling**
   - Path parameters with validation
   - Query parameters with various constraints
   - Request body processing (JSON)
   - Form data handling
   - Header and Cookie parameters

3. **Request Processing**
   - Pydantic models for data validation and serialization
   - Custom field validators
   - Error handling and validation

## Project Structure

```
├── main.py              # Main FastAPI application
├── requirements.txt     # Project dependencies
└── unit_test.py         # Unit tests for all functionality
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The application will start on `http://0.0.0.0:8080`

## API Endpoints

- `GET /` - Root endpoint
- `GET /users/{user_id}` - Get user by ID (path parameter)
- `GET /users` - Get users with filtering (query parameters)
- `POST /users` - Create a new user (JSON body)
- `PUT /users/{user_id}` - Update user (path parameter + JSON body + header/cookie)
- `POST /items/form` - Create item from form data
- `POST /items/json` - Create item from JSON
- `GET /search` - Search items with query parameters

## Testing

The unit tests now use async HTTP calls to test the real API running on localhost:8080.

### Running Tests

1. **Start the API server first:**
```bash
python main.py
```

2. **In a separate terminal, install test dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the async unit tests:**
```bash
python -m pytest unit_test.py -v
```

### Test Features

- **Async HTTP calls**: Tests use `httpx.AsyncClient` for faster concurrent testing
- **Real API validation**: Tests call actual endpoints on localhost:8080
- **Comprehensive coverage**: Tests all endpoints, parameter types, and validation rules
- **Concurrent execution**: Tests run concurrently using `asyncio.gather()` for speed

### Test Cases Included

- App health check and basic connectivity
- User creation and retrieval with validation
- Query parameter filtering and pagination
- Item creation via JSON and form data
- Header and cookie parameter handling
- Search functionality with complex query parameters
- Path parameter validation
- Data validation error handling

## Key Concepts Demonstrated

### Path Parameters
```python
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., gt=0)):
    # user_id must be greater than 0
```

### Query Parameters
```python
@app.get("/users")
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    age_min: Optional[int] = Query(None, ge=13)
):
    # skip >= 0, limit <= 100, age_min >= 13
```

### Request Body
```python
@app.post("/users")
def create_user(user: User):
    # User is a Pydantic model with validation
```

### Form Data
```python
@app.post("/items/form")
def create_item_form(
    name: str = Form(...),
    price: float = Form(..., gt=0)
):
    # Form data with validation
```

### Header and Cookie Parameters
```python
@app.put("/users/{user_id}")
def update_user(
    user_id: int = Path(..., gt=0),
    x_api_key: Optional[str] = Header(None),
    session_id: Optional[str] = Cookie(None)
):
    # Header and cookie parameters
```

### Data Validation with Pydantic
```python
class User(BaseModel):
    id: int = Field(..., gt=0)
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=13, le=120)
```

## Interactive Documentation

Once the server is running, visit:
- http://localhost:8080/docs - Swagger UI documentation
- http://localhost:8080/redoc - ReDoc documentation