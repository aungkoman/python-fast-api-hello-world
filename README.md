# FastAPI To-Do List API

This is a comprehensive To-Do List CRUD API built with FastAPI, featuring Pydantic models for data validation, in-memory data storage, pagination, and filtering.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete To-Do items.
- **Pydantic Models**: Robust request and response validation.
- **In-Memory Storage**: Simple in-memory data storage for demonstration purposes.
- **Pagination**: Retrieve To-Do items with pagination.
- **Filtering**: Filter To-Do items by completion status.
- **Environment Configuration**: Support for environment variables using `pydantic-settings`.
- **Automatic API Documentation**: Provided by FastAPI (Swagger UI and ReDoc).

## Setup

1.  **Clone the repository** (if applicable):

    ```bash
    git clone <repository_url>
    cd fastapi-python
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Start the FastAPI application**:

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

    The API will be accessible at `http://localhost:8000`.

2.  **Access API Documentation**:

    - **Swagger UI**: `http://localhost:8000/docs`
    - **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

All API endpoints are prefixed with `/api/v1`.

-   **POST /api/v1/todos**: Create a new To-Do item.
-   **GET /api/v1/todos**: Retrieve a list of To-Do items. Supports `skip`, `limit`, and `completed` query parameters.
-   **GET /api/v1/todos/{todo_id}**: Retrieve a single To-Do item by ID.
-   **PUT /api/v1/todos/{todo_id}**: Update an existing To-Do item by ID.
-   **DELETE /api/v1/todos/{todo_id}**: Delete a To-Do item by ID.

## Environment Variables

You can configure the application using a `.env` file. Create a file named `.env` in the project root with the following content (example):

```
APP_NAME="My Awesome Todo API"
ADMIN_EMAIL="your.email@example.com"
ITEMS_PER_PAGE=20
```