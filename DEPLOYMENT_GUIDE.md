# 🚀 Medical Chatbot Deployment Guide

> Complete guide for deploying the AI Medical Chatbot in various environments from development to production.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Considerations](#production-considerations)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **Python**: Version 3.10 or higher
- **Memory**: Minimum 4GB RAM (8GB+ recommended for production)
- **Storage**: 10GB+ available space for vector database and models
- **Network**: Stable internet connection for API calls

### Required Accounts & API Keys

1. **Groq API Key**
   - Visit [Groq Console](https://console.groq.com/)
   - Create account and generate API key
   - Free tier includes generous usage limits

2. **HuggingFace Token** (Optional)
   - Visit [HuggingFace](https://huggingface.co/settings/tokens)
   - Create read access token for model downloads

## 🏠 Local Development Setup

### Step 1: Environment Preparation

```bash
# Clone repository
git clone https://github.com/anishks07/Medical-Chatbot.git
cd Medical-Chatbot

# Create virtual environment
python3 -m venv medical-chatbot-env
source medical-chatbot-env/bin/activate  # Linux/macOS
# medical-chatbot-env\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Step 3: Environment Configuration

Create `.env` file in project root:

```bash
# Create environment file
touch .env  # Linux/macOS
# echo. > .env  # Windows
```

Add the following content to `.env`:

```env
# Required: Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Optional: HuggingFace Configuration
HF_TOKEN=your_huggingface_token_here

# Application Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000

# Database Configuration
DB_FAISS_PATH=vector_store/db_faiss
DATA_PATH=data/

# Model Configuration
GROQ_MODEL_NAME=llama-3.1-8b-instant
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### Step 4: Initialize Vector Database

```bash
# Ensure medical PDFs are in data/ directory
ls data/  # Should show PDF files

# Create vector database from PDFs
python app/components/data_loader.py
```

Expected output:
```
INFO - Loading PDF files from data/ directory...
INFO - Processing documents into chunks...
INFO - Creating embeddings and vector store...
INFO - Vector store saved successfully at vector_store/db_faiss/
```

### Step 5: Start Development Server

```bash
# Method 1: Direct Flask run
python app/application.py

# Method 2: Using Flask CLI
export FLASK_APP=app.application
flask run --host=0.0.0.0 --port=5000
```

Access the application at: `http://localhost:5000`

## 🐳 Docker Deployment

### Single Container Deployment

```bash
# Build Docker image
docker build -t medical-chatbot:latest .

# Run container with environment variables
docker run -d \
  --name medical-chatbot \
  -p 5000:5000 \
  -e GROQ_API_KEY=your_api_key \
  -v $(pwd)/vector_store:/app/vector_store \
  -v $(pwd)/logs:/app/logs \
  medical-chatbot:latest
```

### Docker Compose Deployment (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  medical-chatbot:
    build: .
    container_name: medical-chatbot
    ports:
      - "5000:5000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - HF_TOKEN=${HF_TOKEN}
      - FLASK_ENV=production
    volumes:
      - ./vector_store:/app/vector_store:ro
      - ./logs:/app/logs
      - ./data:/app/data:ro
    restart: unless-stopped
    networks:
      - medical-network

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: medical-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - medical-chatbot
    networks:
      - medical-network

networks:
  medical-network:
    driver: bridge
```

Deploy with Docker Compose:

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f medical-chatbot

# Stop services
docker-compose down
```

### Docker Production Optimization

Create `Dockerfile.prod`:

```dockerfile
FROM python:3.10-slim

# Production optimizations
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_DEBUG=False

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app.application:app"]
```

## ☁️ Cloud Deployment

### AWS EC2 Deployment

#### 1. Launch EC2 Instance

```bash
# Launch Ubuntu 22.04 LTS instance
# Minimum: t3.medium (2 vCPU, 4GB RAM)
# Recommended: t3.large (2 vCPU, 8GB RAM)

# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip
```

#### 2. Setup Environment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Reboot to apply changes
sudo reboot
```

#### 3. Deploy Application

```bash
# Clone and setup
git clone https://github.com/anishks07/Medical-Chatbot.git
cd Medical-Chatbot

# Configure environment
cp .env.example .env
nano .env  # Add your API keys

# Deploy with Docker Compose
docker-compose up -d
```

#### 4. Setup Nginx and SSL

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Nginx configuration
sudo nano /etc/nginx/sites-available/medical-chatbot
```

Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Google Cloud Platform (GCP)

#### 1. Cloud Run Deployment

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/medical-chatbot

# Deploy to Cloud Run
gcloud run deploy medical-chatbot \
  --image gcr.io/PROJECT_ID/medical-chatbot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=your_key
```

#### 2. Compute Engine Deployment

```bash
# Create VM instance
gcloud compute instances create medical-chatbot-vm \
  --zone=us-central1-a \
  --machine-type=e2-standard-2 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB

# SSH and setup (similar to EC2 steps)
gcloud compute ssh medical-chatbot-vm --zone=us-central1-a
```

### Azure Container Instances

```bash
# Create resource group
az group create --name medical-chatbot-rg --location eastus

# Deploy container
az container create \
  --resource-group medical-chatbot-rg \
  --name medical-chatbot \
  --image medical-chatbot:latest \
  --cpu 2 \
  --memory 4 \
  --ports 5000 \
  --environment-variables GROQ_API_KEY=your_key
```

## 🏭 Production Considerations

### Security

#### 1. Environment Variables

```bash
# Use secure secret management
# AWS: AWS Secrets Manager
# GCP: Secret Manager
# Azure: Key Vault

# Example: AWS Secrets Manager integration
pip install boto3

# In application code:
import boto3
def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']
```

#### 2. Network Security

```bash
# Firewall rules (UFW on Ubuntu)
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Application-level rate limiting
pip install flask-limiter
```

#### 3. HTTPS Configuration

```bash
# Force HTTPS in Flask
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, force_https=True)
```

### Performance Optimization

#### 1. Application Scaling

```yaml
# docker-compose.yml with load balancing
version: '3.8'
services:
  medical-chatbot:
    build: .
    deploy:
      replicas: 3
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
```

#### 2. Caching Strategy

```python
# Redis caching for vector search results
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args))}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator
```

#### 3. Database Optimization

```python
# Vector store optimization for production
def load_vector_store_optimized():
    """Load vector store with optimized settings for production"""
    embedding_model = get_embedding_model()
    
    if os.path.exists(DB_FAISS_PATH):
        # Load with memory mapping for large datasets
        return FAISS.load_local(
            DB_FAISS_PATH,
            embedding_model,
            allow_dangerous_deserialization=True,
            # Enable memory mapping for better performance
            normalize_L2=True
        )
```

### Monitoring Setup

#### 1. Application Metrics

```python
# Prometheus metrics
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Custom metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests')
REQUEST_LATENCY = Histogram('app_request_duration_seconds', 'Request latency')
```

#### 2. Health Checks

```python
@app.route('/health')
def health_check():
    """Health check endpoint for load balancers"""
    try:
        # Test vector store
        db = load_vector_store()
        if db is None:
            return jsonify({'status': 'unhealthy', 'issue': 'vector_store'}), 503
        
        # Test LLM
        llm = load_llm()
        if llm is None:
            return jsonify({'status': 'unhealthy', 'issue': 'llm'}), 503
        
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503
```

#### 3. Logging Configuration

```python
# Production logging setup
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/medical_chatbot.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

## 📊 Monitoring & Maintenance

### System Monitoring

#### 1. Grafana Dashboard Setup

```yaml
# docker-compose-monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana

volumes:
  grafana-storage:
```

#### 2. Alert Configuration

```yaml
# alerts.yml
groups:
  - name: medical-chatbot
    rules:
      - alert: HighResponseTime
        expr: flask_http_request_duration_seconds > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          
      - alert: ServiceDown
        expr: up{job="medical-chatbot"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Medical chatbot service is down"
```

### Backup Strategy

#### 1. Vector Store Backup

```bash
#!/bin/bash
# backup_vectorstore.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/vector_store"

# Create backup
mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/vector_store_$DATE.tar.gz vector_store/

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "vector_store_*.tar.gz" -mtime +7 -delete
```

#### 2. Database Backup Automation

```bash
# Crontab entry for daily backups
0 2 * * * /path/to/backup_vectorstore.sh
```

### Update Procedures

#### 1. Rolling Updates

```bash
#!/bin/bash
# rolling_update.sh
echo "Starting rolling update..."

# Pull latest code
git pull origin main

# Build new image
docker build -t medical-chatbot:latest .

# Update services one by one
docker-compose up -d --no-deps medical-chatbot-1
sleep 30
docker-compose up -d --no-deps medical-chatbot-2
sleep 30
docker-compose up -d --no-deps medical-chatbot-3

echo "Rolling update completed"
```

#### 2. Blue-Green Deployment

```bash
#!/bin/bash
# blue_green_deploy.sh
NEW_TAG=$(date +%Y%m%d-%H%M%S)

# Build and tag new version
docker build -t medical-chatbot:$NEW_TAG .

# Deploy to green environment
docker-compose -f docker-compose-green.yml up -d

# Health check
if curl -f http://localhost:5001/health; then
    # Switch traffic to green
    docker-compose -f docker-compose-blue.yml down
    docker-compose -f docker-compose-green.yml up -d
    echo "Deployment successful"
else
    echo "Health check failed, rolling back"
    docker-compose -f docker-compose-green.yml down
fi
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Vector Store Issues

**Problem**: "Vector store not present or empty"

```bash
# Solution 1: Regenerate vector store
python app/components/data_loader.py

# Solution 2: Check PDF files
ls -la data/  # Ensure PDFs are present and readable

# Solution 3: Check permissions
chmod 755 vector_store/
chmod 644 vector_store/db_faiss/*
```

#### 2. API Key Issues

**Problem**: "Invalid API key" or authentication errors

```bash
# Check environment variables
echo $GROQ_API_KEY

# Verify API key format
# Groq keys typically start with 'gsk_'

# Test API connectivity
curl -H "Authorization: Bearer $GROQ_API_KEY" \
     https://api.groq.com/openai/v1/models
```

#### 3. Memory Issues

**Problem**: Out of memory during vector store creation

```bash
# Monitor memory usage
top -p $(pgrep -f python)

# Solution 1: Reduce chunk size
# Edit app/config/config.py
CHUNK_SIZE = 300  # Reduce from 500
CHUNK_OVERLAP = 25  # Reduce from 50

# Solution 2: Process PDFs individually
# Modify data_loader.py to process one PDF at a time
```

#### 4. Docker Issues

**Problem**: Container fails to start

```bash
# Check container logs
docker logs medical-chatbot

# Check resource limits
docker stats medical-chatbot

# Rebuild without cache
docker build --no-cache -t medical-chatbot .
```

### Debug Mode

Enable debug mode for development:

```bash
# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=True

# Run with verbose logging
python app/application.py --log-level=DEBUG
```

### Performance Tuning

#### 1. Vector Search Optimization

```python
# Optimize retrieval parameters
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        'k': 3,  # Reduce from default 4
        'score_threshold': 0.7  # Increase threshold
    }
)
```

#### 2. Model Parameter Tuning

```python
# Optimize LLM parameters for speed
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant",  # Fastest model
    temperature=0.1,  # Reduce for more deterministic responses
    max_tokens=256,   # Reduce for faster responses
    timeout=30,       # Set reasonable timeout
)
```

### Maintenance Scripts

#### 1. Log Rotation

```bash
#!/bin/bash
# rotate_logs.sh
LOG_DIR="/app/logs"
ARCHIVE_DIR="/app/logs/archive"

mkdir -p $ARCHIVE_DIR
find $LOG_DIR -name "*.log" -mtime +30 -exec mv {} $ARCHIVE_DIR/ \;
gzip $ARCHIVE_DIR/*.log
```

#### 2. Health Check Script

```bash
#!/bin/bash
# health_check.sh
ENDPOINT="http://localhost:5000/health"

if curl -f $ENDPOINT > /dev/null 2>&1; then
    echo "$(date): Service is healthy"
else
    echo "$(date): Service is unhealthy - restarting..."
    docker-compose restart medical-chatbot
fi
```

---

## 📞 Support

For deployment issues or questions:

1. **Check logs**: Always start with application and container logs
2. **GitHub Issues**: [Report deployment issues](https://github.com/anishks07/Medical-Chatbot/issues)
3. **Documentation**: Refer to project README for additional details

---

**Successfully deployed?** ⭐ Star the repository and share your experience!