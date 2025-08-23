# FastAPI Setup, Parameter Handling, and Request Processing - Project Question

## Problem Statement

Develop a comprehensive FastAPI application that demonstrates the core concepts of FastAPI framework including application setup, parameter handling, request processing, data validation, and response serialization. The application should showcase various parameter types available in FastAPI and implement proper validation mechanisms.

## Project Requirements

Create a FastAPI application that implements the following features:

### 1. FastAPI Application Setup
- Initialize a FastAPI application with proper configuration
- Set up Uvicorn as the ASGI server
- Configure application metadata (title, description, version)

### 2. Parameter Handling
Implement endpoints that demonstrate all major parameter types in FastAPI:

#### a) Path Parameters
- Create endpoints that accept path parameters
- Implement validation for path parameters (e.g., numeric constraints)

#### b) Query Parameters
- Create endpoints that accept query parameters
- Implement various validation constraints (min, max, length, etc.)
- Handle optional query parameters
- Handle list-type query parameters

#### c) Request Body Parameters
- Process JSON request bodies
- Process form data
- Implement validation for both JSON and form data

#### d) Header and Cookie Parameters
- Extract and process header parameters
- Extract and process cookie parameters

### 3. Request Processing
- Implement proper request validation using Pydantic models
- Handle data serialization for responses
- Implement error handling for validation failures

### 4. Data Validation and Serialization
- Use Pydantic models for data validation
- Implement field-level validations using Field()
- Create custom validators using validator decorators
- Ensure proper data serialization in responses

## Technical Requirements

### Pydantic Models to Implement
1. **User Model** with the following fields:
   - id (integer, > 0)
   - username (string, 3-50 characters, alphanumeric)
   - email (string, valid email format)
   - age (integer, 13-120)
   - tags (list of strings)
   - Custom validator for username to ensure alphanumeric characters

2. **Item Model** with the following fields:
   - name (string, required)
   - description (string, optional)
   - price (float, > 0)
   - tags (list of strings)

### Endpoints to Implement

#### 1. Basic Endpoint
- `GET /` - Root endpoint returning a simple message

#### 2. Path Parameter Endpoint
- `GET /users/{user_id}` - Retrieve user by ID with path parameter validation

#### 3. Query Parameter Endpoint
- `GET /users` - Retrieve users with filtering and pagination:
  - skip (integer, >= 0, default: 0)
  - limit (integer, <= 100, default: 10)
  - age_min (optional integer, >= 13)
  - tags (optional list of strings)

#### 4. Request Body Endpoints
- `POST /users` - Create user with JSON body validation
- `POST /items/json` - Create item with JSON body validation
- `POST /items/form` - Create item with form data validation

#### 5. Multiple Parameter Types Endpoint
- `PUT /users/{user_id}` - Update user with:
  - Path parameter: user_id
  - Request body: user data
  - Header parameter: X-API-Key (optional)
  - Cookie parameter: session_id (optional)

#### 6. Complex Query Parameters Endpoint
- `GET /search` - Search items with:
  - q (optional string, max 50 characters)
  - price_min (optional float, >= 0)
  - price_max (optional float, > 0)

## Validation Requirements

### User Model Validation Rules:
- id: Must be greater than 0
- username: 3-50 characters, must be alphanumeric
- email: Must match standard email format
- age: Must be between 13 and 120 (inclusive)
- tags: List of strings

### Item Model Validation Rules:
- name: Required string
- description: Optional string
- price: Must be greater than 0
- tags: List of strings

### Parameter Validation Rules:
- Path parameters: Numeric constraints as specified
- Query parameters: Various constraints as described above
- Form parameters: Validation for required and constrained fields
- Header/Cookie parameters: Optional string handling

## Implementation Guidelines

1. Use proper type hints for all function parameters
2. Implement comprehensive error handling
3. Use appropriate HTTP status codes
4. Return properly structured JSON responses
5. Follow FastAPI best practices for parameter definitions
6. Implement clean, readable code with proper documentation

## Testing Requirements

Create unit tests that verify:
1. All endpoints function correctly with valid data
2. Validation works properly for invalid data
3. All parameter types are handled correctly
4. Error responses are appropriate for invalid inputs
5. Pydantic models validate data as expected

## Deliverables

1. `main.py` - Complete FastAPI application implementation
2. `requirements.txt` - Dependencies needed to run the application
3. Unit tests to verify all functionality
4. Documentation explaining the implementation

## Evaluation Criteria

The implementation will be evaluated on:
1. Correctness of FastAPI setup and configuration
2. Proper implementation of all parameter types
3. Comprehensive data validation
4. Code quality and readability
5. Proper error handling
6. Test coverage and quality
7. Adherence to FastAPI best practices