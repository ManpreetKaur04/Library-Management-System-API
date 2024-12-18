# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose ports for Django and Redis
EXPOSE 8000 6379

# Create reports directory
RUN mkdir -p /app/reports

# Start Redis and Celery worker and Django server
CMD bash -c "redis-server --daemonize yes && \
             celery -A library_project worker --loglevel=info & \
             python manage.py migrate && \
             python manage.py runserver 0.0.0.0:8000"