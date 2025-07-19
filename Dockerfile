## Parent image
FROM python:3.10-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Install uv package manager
RUN pip install uv

## Copy uv configuration files first for better caching
COPY pyproject.toml uv.lock ./

## Install dependencies using uv
RUN uv sync --frozen

## Copy the rest of the application
COPY . .

## Expose only flask port
EXPOSE 5000

## Run the Flask app with uv
CMD ["uv", "run", "python", "app/application.py"]

