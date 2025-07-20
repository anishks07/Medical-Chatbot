# Use official lightweight Python base image
FROM python:3.10-slim

# Environment variables for consistent behavior
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Copy project files
COPY . .

# Install Python dependencies using uv (from pyproject.toml)
RUN uv pip install --system .

# Expose appropriate port (update if your app uses a different one)
EXPOSE 8080

# Start your app via uv (adjust CMD if your app doesn't need "bot")
CMD ["uv", "run", "python", "app/application.py"]
