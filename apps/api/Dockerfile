# Multi-stage Dockerfile for Django API
# Optimized for development and production builds

# Base stage - shared dependencies
FROM python:3.12-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
# Open for collaboration: Add any additional system packages needed
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir \
    ipdb \
    django-debug-toolbar \
    pytest \
    pytest-django \
    black \
    ruff

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p staticfiles media

# Expose port
EXPOSE 8000

# Development command (can be overridden in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base as production

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user for security
RUN useradd -m -u 1000 django && chown -R django:django /app
USER django

# Expose port
EXPOSE 8000

# Production command with Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
