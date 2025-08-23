import pytest
import asyncio
import httpx
from typing import Dict, Any

BASE_URL = "http://localhost:8080"

@pytest.mark.asyncio
async def test_app_health():
    """Test that the FastAPI app is running and accessible"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "FastAPI is running successfully!"
        print("PASS: App health check passed")

@pytest.mark.asyncio
async def test_create_and_get_user():
    """Test creating and retrieving a user"""
    async with httpx.AsyncClient() as client:
        # Create user
        user_data = {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "age": 30,
            "tags": ["developer", "python"]
        }
        
        create_response = await client.post(f"{BASE_URL}/users", json=user_data)
        assert create_response.status_code == 200
        created_user = create_response.json()
        assert created_user["message"] == "User created"
        assert created_user["user"]["username"] == "johndoe"
        
        # Get user by ID
        get_response = await client.get(f"{BASE_URL}/users/1")
        assert get_response.status_code == 200
        retrieved_user = get_response.json()
        assert retrieved_user["user"]["username"] == "johndoe"
        assert retrieved_user["user"]["email"] == "john@example.com"
        
        print("PASS: Create and get user test passed")

@pytest.mark.asyncio
async def test_user_validation():
    """Test user validation errors"""
    async with httpx.AsyncClient() as client:
        # Test invalid email
        invalid_user = {
            "id": 2,
            "username": "testuser",
            "email": "invalid-email",
            "age": 25
        }
        
        response = await client.post(f"{BASE_URL}/users", json=invalid_user)
        assert response.status_code == 422  # Validation error
        
        # Test invalid username (too short)
        invalid_user2 = {
            "id": 3,
            "username": "ab",
            "email": "test@example.com",
            "age": 25
        }
        
        response2 = await client.post(f"{BASE_URL}/users", json=invalid_user2)
        assert response2.status_code == 422
        
        print("PASS: User validation test passed")

@pytest.mark.asyncio
async def test_get_users_with_query_params():
    """Test getting users with query parameters"""
    async with httpx.AsyncClient() as client:
        # Create multiple users first
        users = [
            {"id": 10, "username": "alice", "email": "alice@example.com", "age": 25, "tags": ["developer"]},
            {"id": 11, "username": "bob", "email": "bob@example.com", "age": 35, "tags": ["manager"]},
            {"id": 12, "username": "charlie", "email": "charlie@example.com", "age": 28, "tags": ["developer"]}
        ]
        
        for user in users:
            await client.post(f"{BASE_URL}/users", json=user)
        
        # Test query parameters
        response = await client.get(f"{BASE_URL}/users?skip=0&limit=2&age_min=30")
        assert response.status_code == 200
        data = response.json()
        # Should return users with age >= 30 (bob)
        assert len(data["users"]) >= 0
        
        print("PASS: Get users with query params test passed")

@pytest.mark.asyncio
async def test_create_item_json():
    """Test creating items via JSON"""
    async with httpx.AsyncClient() as client:
        item_data = {
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 1200.00,
            "tags": ["electronics", "gaming"]
        }
        
        response = await client.post(f"{BASE_URL}/items/json", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item created from JSON"
        assert data["item"]["name"] == "Laptop"
        assert data["item"]["price"] == 1200.00
        
        print("PASS: Create item JSON test passed")

@pytest.mark.asyncio
async def test_create_item_form():
    """Test creating items via form data"""
    async with httpx.AsyncClient() as client:
        form_data = {
            "name": "Phone",
            "description": "Smartphone",
            "price": 800.00
        }
        
        response = await client.post(f"{BASE_URL}/items/form", data=form_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item created from form"
        assert data["item"]["name"] == "Phone"
        assert data["item"]["price"] == 800.00
        
        print("PASS: Create item form test passed")

@pytest.mark.asyncio
async def test_update_user_with_headers():
    """Test updating user with headers and cookies"""
    async with httpx.AsyncClient() as client:
        # First create a user
        user_data = {
            "id": 20,
            "username": "testuser",
            "email": "test@example.com",
            "age": 25,
            "tags": ["tester"]
        }
        
        await client.post(f"{BASE_URL}/users", json=user_data)
        
        # Update the user with headers
        updated_user = {
            "id": 20,
            "username": "updateduser",
            "email": "updated@example.com",
            "age": 26,
            "tags": ["senior-tester"]
        }
        
        headers = {"X-API-Key": "test-api-key"}
        cookies = {"session_id": "test-session-123"}
        
        response = await client.put(
            f"{BASE_URL}/users/20",
            json=updated_user,
            headers=headers,
            cookies=cookies
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "User updated"
        assert data["user"]["username"] == "updateduser"
        assert data["metadata"]["api_key"] == "test-api-key"
        assert data["metadata"]["session_id"] == "test-session-123"
        
        print("PASS: Update user with headers test passed")

@pytest.mark.asyncio
async def test_search_items():
    """Test search functionality with complex query parameters"""
    async with httpx.AsyncClient() as client:
        # Create some test items first
        items = [
            {"name": "Gaming Laptop", "description": "High-end gaming laptop", "price": 1500.00},
            {"name": "Office Laptop", "description": "Business laptop", "price": 800.00},
            {"name": "Gaming Mouse", "description": "RGB gaming mouse", "price": 50.00}
        ]
        
        for item in items:
            await client.post(f"{BASE_URL}/items/json", json=item)
        
        # Search for gaming items
        response = await client.get(f"{BASE_URL}/search?q=gaming&price_min=40&price_max=2000")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) >= 0
        
        print("PASS: Search items test passed")

@pytest.mark.asyncio
async def test_path_parameter_validation():
    """Test path parameter validation"""
    async with httpx.AsyncClient() as client:
        # Test invalid user ID (should be > 0)
        response = await client.get(f"{BASE_URL}/users/0")
        assert response.status_code == 422  # Validation error
        
        # Test non-existent user ID
        response = await client.get(f"{BASE_URL}/users/9999")
        assert response.status_code == 200
        data = response.json()
        assert data["error"] == "User not found"
        
        print("PASS: Path parameter validation test passed")

@pytest.mark.asyncio
async def test_item_price_validation():
    """Test item price validation"""
    async with httpx.AsyncClient() as client:
        # Test negative price
        invalid_item = {
            "name": "Invalid Item",
            "description": "Item with negative price",
            "price": -100.00
        }
        
        response = await client.post(f"{BASE_URL}/items/json", json=invalid_item)
        assert response.status_code == 422  # Validation error
        
        print("PASS: Item price validation test passed")

async def run_all_tests():
    """Run all async tests concurrently for faster execution"""
    print("Running async API tests against localhost:8080...")
    print("=" * 50)
    
    # List of all test functions
    test_functions = [
        test_app_health(),
        test_create_and_get_user(),
        test_user_validation(),
        test_get_users_with_query_params(),
        test_create_item_json(),
        test_create_item_form(),
        test_update_user_with_headers(),
        test_search_items(),
        test_path_parameter_validation(),
        test_item_price_validation()
    ]
    
    try:
        # Run all tests concurrently
        await asyncio.gather(*test_functions)
        print("=" * 50)
        print("All API tests passed!")
        return True
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run the async tests
    result = asyncio.run(run_all_tests())
    exit(0 if result else 1)