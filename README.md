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


'''Let me summatize the key features and Approach Explanation:
1. Models:
Created Author, Book, and BorrowRecord models as specified
Implemented relationships and constraints
Added methods for string representation
2. API Endpoints:
•Full CRUD operations for Authors and Books
Custom endpoints for borrowing and returning books
Celery-powered report generation
3. Background Tasks:
Implemented Celery task for report generation
Saves reports as JSON files in reports/directory
Generates timestamp-based filenames
Retrieves latest report via GET endpoint
4. Error Handling:
Added comprehensive error responses
• Handled edge cases like book availability, existing records
5. Authentication
Implemented JWT authentication using diangorestframework-simpleiwt
Created token obtain and refresh endpoints
Added authentication to ViewSets to secure endpoints
Provides stateless, token-based authentication
6. API Documentation
Used dif yasg to generate Swagger documentation
Provides interactive API documentation
Allows testing endpoints directly from Swagger Ul
Includes detailed endpoint descriptions
7. Background Tasks
Celery integrated with Redis as message broker
Periodic report generation task
Flexible task scheduling and execution
8. Architectural Considerations
Separation of concerns
Modular design
Easily extensible
Follows Django and DRF best practices
Deployment Considerations:
Use Redis as the message broker for Celery
SQLite for development, recommend PostgreSQL for production
Implement environment-based settings
Add proper logging and monitoring'''