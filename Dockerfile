# Use official lightweight Python base image
FROM python:3.10-slim

# Environment variables for consistent behavior
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install uv package manager
RUN pip install --no-cache-dir uv

# Create necessary directories for application
RUN mkdir -p data logs vector_store/db_faiss

# Copy project files
COPY . .

# Install Python dependencies using uv (from pyproject.toml)
RUN uv pip install --system .

# Expose appropriate port (update if your app uses a different one)
EXPOSE 5000

# Health check to ensure Flask application is running
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Start your app via uv (adjust CMD if your app doesn't need "bot")
CMD ["uv", "run", "python", "app/application.py"]
