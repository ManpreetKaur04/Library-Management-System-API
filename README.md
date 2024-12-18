# Library Management System API

## Project Overview
A Django REST Framework-based Library Management System with:
- JWT Authentication
- Celery Background Tasks
- Swagger API Documentation
- Book and Author Management

## System Architecture
- **Backend**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Background Tasks**: Celery with Redis
- **Documentation**: Swagger/OpenAPI

## Prerequisites
- Python 3.9+
- Django 4.2+
- Redis
- pip

## Setup and Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd library_management_system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 6. Running the Application

#### Start Redis (Required for Celery)
```bash
# macOS
brew services start redis



#### Start Celery Worker
```bash
celery -A library_project worker --loglevel=info
```

#### Run Django Development Server
```bash
python manage.py runserver
```

## Authentication Workflow

### 1. Obtain JWT Token
```bash
# POST request to obtain tokens
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

### 2. Use Token in Requests
Include the access token in the Authorization header:
```bash
curl -X GET http://localhost:8000/api/books/ \
     -H "Authorization: Bearer <your_access_token>"
```

### 3. Refresh Token
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "<your_refresh_token>"}'
```

## API Documentation
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Running Tests
```bash
python manage.py test
```

## Deployment Considerations
- Use PostgreSQL in production
- Set `DEBUG=False`
- Configure proper secret management
- Use gunicorn/uwsgi for production WSGI
```

