from fastapi import FastAPI, Path, Query, Body, Form, Header, Cookie
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import uvicorn

# Pydantic models for request validation and data serialization
class User(BaseModel):
    id: int = Field(..., gt=0)
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=13, le=120)
    tags: List[str] = []
    
    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'Username must be alphanumeric'
        return v

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    tags: List[str] = []

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Demo",
    description="Demonstrating FastAPI setup, parameter handling, and request processing",
    version="1.0.0"
)

# In-memory storage
users_db = {}
items_db = {}

# 1. FastAPI Setup - Basic endpoint
@app.get("/")
def root():
    return {"message": "FastAPI is running successfully!"}

# 2. Parameter Handling Examples

# Path Parameters
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., gt=0)):
    """Path parameter example"""
    if user_id in users_db:
        return {"user": users_db[user_id]}
    return {"error": "User not found"}

# Query Parameters
@app.get("/users")
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    age_min: Optional[int] = Query(None, ge=13),
    tags: Optional[List[str]] = Query(None)
):
    """Query parameter examples"""
    filtered_users = list(users_db.values())
    
    if age_min:
        filtered_users = [u for u in filtered_users if u["age"] >= age_min]
    
    if tags:
        filtered_users = [u for u in filtered_users if any(tag in u["tags"] for tag in tags)]
    
    return {"users": filtered_users[skip:skip+limit]}

# Request Body (JSON)
@app.post("/users")
def create_user(user: User):
    """Request body processing with validation"""
    users_db[user.id] = user.dict()
    return {"message": "User created", "user": user}

# Form Data
@app.post("/items/form")
def create_item_form(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(..., gt=0)
):
    """Form data processing"""
    item_id = len(items_db) + 1
    item = {"id": item_id, "name": name, "description": description, "price": price}
    items_db[item_id] = item
    return {"message": "Item created from form", "item": item}

# JSON Body
@app.post("/items/json")
def create_item_json(item: Item):
    """JSON body processing with validation"""
    item_id = len(items_db) + 1
    item_dict = item.dict()
    item_dict["id"] = item_id
    items_db[item_id] = item_dict
    return {"message": "Item created from JSON", "item": item_dict}

# Multiple Parameter Types
@app.put("/users/{user_id}")
def update_user(
    user_id: int = Path(..., gt=0),
    user: User = Body(...),
    x_api_key: Optional[str] = Header(None),
    session_id: Optional[str] = Cookie(None)
):
    """Multiple parameter types: path, body, header, cookie"""
    if user_id not in users_db:
        return {"error": "User not found"}
    
    users_db[user_id] = user.dict()
    
    # Return info about all parameters received
    return {
        "message": "User updated",
        "user": user,
        "metadata": {
            "api_key": x_api_key,
            "session_id": session_id
        }
    }

# Complex Query Parameters
@app.get("/search")
def search_items(
    q: Optional[str] = Query(None, max_length=50),
    price_min: Optional[float] = Query(None, ge=0),
    price_max: Optional[float] = Query(None, gt=0)
):
    """Complex query parameters"""
    results = list(items_db.values())
    
    if q:
        results = [item for item in results if q.lower() in item["name"].lower()]
    
    if price_min:
        results = [item for item in results if item["price"] >= price_min]
    
    if price_max:
        results = [item for item in results if item["price"] <= price_max]
    
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)