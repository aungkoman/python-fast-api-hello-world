# FastAPI To-Do List API

This is a comprehensive To-Do List CRUD API built with FastAPI, featuring Pydantic models for data validation, in-memory data storage, pagination, and filtering.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete To-Do items and general items.
- **Pydantic Models**: Robust request and response validation.
- **In-Memory Storage**: Simple in-memory data storage for demonstration purposes.
- **Pagination**: Retrieve To-Do items with pagination.
- **Filtering**: Filter To-Do items by completion status.
- **Environment Configuration**: Support for environment variables using `pydantic-settings`.
- **Automatic API Documentation**: Provided by FastAPI (Swagger UI and ReDoc).

## Setup

1.  **Clone the repository** (if applicable):

    ```bash
    git clone https://github.com/aungkoman/python-fast-api-hello-world
    cd python-fast-api-hello-world
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

### To-Do Items

-   **POST /api/v1/todos**: Create a new To-Do item.
-   **GET /api/v1/todos**: Retrieve a list of To-Do items. Supports `skip`, `limit`, and `completed` query parameters.
-   **GET /api/v1/todos/{todo_id}**: Retrieve a single To-Do item by ID.
-   **PUT /api/v1/todos/{todo_id}**: Update an existing To-Do item by ID.
-   **DELETE /api/v1/todos/{todo_id}**: Delete a To-Do item by ID.

### General Items

-   **POST /api/v1/items**: Create a new item.
-   **GET /api/v1/items**: Retrieve a list of items. Supports `skip`, `limit`, and `name` query parameters.
-   **GET /api/v1/items/{item_id}**: Retrieve a single item by ID.
-   **PUT /api/v1/items/{item_id}**: Update an existing item by ID.
-   **DELETE /api/v1/items/{item_id}**: Delete an item by ID.

## Environment Variables

You can configure the application using a `.env` file. Copy `.env.example` to `.env` and update the values as needed:

## Deployment Guide (Ubuntu with Apache and mod_wsgi)

This guide outlines the steps to deploy your FastAPI application on an Ubuntu server using Apache as a reverse proxy and `mod_wsgi`.

### Prerequisites

-   An Ubuntu server.
-   Apache web server installed.
-   Python 3.x and `pip` installed.
-   MySQL server installed and configured.

### 1. Server Setup

1.  **Update and Upgrade System Packages**:

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2.  **Install Apache and mod_wsgi**:

    ```bash
    sudo apt install apache2 libapache2-mod-wsgi-py3 -y
    ```

### 2. Project Setup on Server

1.  **Clone your repository** to a suitable location, e.g., `/var/www/fastapi-python`:

    ```bash
    sudo git clone <your_repository_url> /var/www/fastapi-python
    cd /var/www/fastapi-python
    ```

2.  **Create and Activate a Virtual Environment**:

    ```bash
    sudo apt install python3-venv -y
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:

    Create a `.env` file in the project root (`/var/www/fastapi-python/.env`) with your production settings, especially for the database connection.

    ```env
    APP_NAME="Production Todo API"
    ADMIN_EMAIL="production@example.com"
    ITEMS_PER_PAGE=20
    MYSQL_USER=your_mysql_user
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_DB=fast_api_python
    ```

5.  **Create Database Tables**:

    Ensure your MySQL database (`fast_api_python`) exists and then run the table creation script:

    ```bash
    python create_db_tables.py
    ```

### 3. WSGI Entry Point

Create a `wsgi.py` file in your project root (`/var/www/fastapi-python/wsgi.py`) with the following content:

```python
import sys
import os

# Add your project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main import app

# This is the WSGI application entry point
application = app
```

### 4. Apache Virtual Host Configuration

1.  **Create a new Apache virtual host file** for your application, e.g., `/etc/apache2/sites-available/fastapi-todo.conf`:

    ```bash
    sudo nano /etc/apache2/sites-available/fastapi-todo.conf
    ```

2.  **Add the following configuration** to the file, replacing `your_domain.com` with your actual domain or server IP:

    ```apache
    <VirtualHost *:80>
        ServerAdmin webmaster@localhost
        ServerName your_domain.com
        # ServerAlias www.your_domain.com

        DocumentRoot /var/www/fastapi-python

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        WSGIDaemonProcess fastapi-todo python-home=/var/www/fastapi-python/venv python-path=/var/www/fastapi-python
        WSGIProcessGroup fastapi-todo
        WSGIScriptAlias / /var/www/fastapi-python/wsgi.py

        <Directory /var/www/fastapi-python>
            Require all granted
        </Directory>

        # Optional: Proxy for static files if you have any
        # Alias /static /var/www/fastapi-python/static
        # <Directory /var/www/fastapi-python/static>
        #     Require all granted
        # </Directory>
    </VirtualHost>
    ```

3.  **Enable the virtual host and restart Apache**:

    ```bash
    sudo a2ensite fastapi-todo.conf
    sudo a2dissite 000-default.conf # Disable default Apache page
    sudo systemctl restart apache2
    ```

### 5. Access Your Application

Your FastAPI application should now be accessible via your configured `ServerName` (e.g., `http://your_domain.com`). The API documentation will be available at `http://your_domain.com/docs`.