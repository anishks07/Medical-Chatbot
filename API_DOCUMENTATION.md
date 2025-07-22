# 📡 Medical Chatbot API Documentation

> Comprehensive API reference for the AI Medical Chatbot application

## 🌐 Base URL

```
http://localhost:5000  # Development
https://your-domain.com  # Production
```

## 🔐 Authentication

Currently, the API does not require authentication for basic usage. For production deployments, consider implementing:

- API key authentication
- JWT tokens for session management
- Rate limiting per IP/user

## 📋 Endpoints Overview

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/` | Main chat interface | None |
| POST | `/` | Submit medical query | `prompt` |
| GET | `/clear` | Clear chat history | None |
| GET | `/health` | Health check | None |
| GET | `/api/status` | API status | None |

## 🎯 Detailed API Reference

### 1. Main Chat Interface

#### Get Chat Interface
```http
GET /
```

**Description**: Returns the main chat interface HTML page

**Response**:
- **Content-Type**: `text/html`
- **Status**: `200 OK`

**Example**:
```bash
curl -X GET http://localhost:5000/
```

---

### 2. Submit Medical Query

#### Process Medical Question
```http
POST /
Content-Type: application/x-www-form-urlencoded
```

**Description**: Processes a medical question and returns AI-generated response

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The medical question to be answered |

**Request Example**:
```bash
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "prompt=What are the symptoms of diabetes?"
```

**Response**:
- **Content-Type**: `text/html`
- **Status**: `200 OK` (success) or `500 Internal Server Error` (error)

**Success Response**:
Returns updated chat interface with the AI response included in the conversation history.

**Error Response**:
Returns chat interface with error message displayed.

**Session Management**:
The application uses Flask sessions to maintain conversation history:
```python
session["messages"] = [
    {"role": "user", "content": "What are the symptoms of diabetes?"},
    {"role": "assistant", "content": "Diabetes symptoms include..."}
]
```

---

### 3. Clear Chat History

#### Clear Conversation
```http
GET /clear
```

**Description**: Clears the current chat session and redirects to main interface

**Response**:
- **Status**: `302 Found` (redirect to `/`)

**Example**:
```bash
curl -X GET http://localhost:5000/clear
```

---

### 4. Health Check

#### System Health Status
```http
GET /health
```

**Description**: Returns the health status of the application and its components

**Response**:
- **Content-Type**: `application/json`
- **Status**: `200 OK` (healthy) or `503 Service Unavailable` (unhealthy)

**Success Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-07-21T10:30:00Z",
  "components": {
    "vector_store": "operational",
    "llm": "operational",
    "embeddings": "operational"
  },
  "version": "1.0.0"
}
```

**Error Response**:
```json
{
  "status": "unhealthy",
  "timestamp": "2025-07-21T10:30:00Z",
  "issue": "vector_store",
  "error": "Vector store not found",
  "components": {
    "vector_store": "failed",
    "llm": "operational",
    "embeddings": "operational"
  }
}
```

**Example**:
```bash
curl -X GET http://localhost:5000/health
```

---

### 5. API Status (Extended)

#### Detailed API Information
```http
GET /api/status
```

**Description**: Returns detailed API status and configuration information

**Response**:
```json
{
  "api": {
    "name": "Medical Chatbot API",
    "version": "1.0.0",
    "status": "operational"
  },
  "models": {
    "llm": {
      "provider": "groq",
      "model": "llama-3.1-8b-instant",
      "status": "ready"
    },
    "embeddings": {
      "model": "sentence-transformers/all-MiniLM-L6-v2",
      "status": "ready"
    }
  },
  "database": {
    "type": "FAISS",
    "documents_count": 2,
    "chunks_count": 1247,
    "last_updated": "2025-07-21T08:00:00Z"
  },
  "performance": {
    "avg_response_time_ms": 2500,
    "total_queries": 156,
    "uptime_seconds": 86400
  }
}
```

## 🔧 Request/Response Examples

### Medical Query Processing

#### Example 1: Diabetes Information
**Request**:
```bash
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "prompt=What%20are%20the%20common%20symptoms%20of%20type%202%20diabetes?"
```

**Expected AI Response** (within HTML):
```
"Type 2 diabetes commonly presents with increased thirst (polydipsia), frequent urination (polyuria), excessive hunger, fatigue, and blurred vision. Many patients also experience slow-healing wounds, recurring infections, and unexplained weight loss. Early stages may be asymptomatic, making regular screening important for at-risk individuals."
```

#### Example 2: Treatment Information
**Request**:
```bash
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "prompt=How%20is%20hypertension%20typically%20treated?"
```

**Expected AI Response** (within HTML):
```
"Hypertension treatment typically begins with lifestyle modifications including dietary changes (reduced sodium, DASH diet), regular physical activity, weight management, and smoking cessation. Pharmacological options include ACE inhibitors, ARBs, calcium channel blockers, beta-blockers, and diuretics, often used in combination based on patient response and comorbidities."
```

## 🚨 Error Handling

### Common Error Scenarios

#### 1. Missing Query Parameter
**Request**:
```bash
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d ""
```

**Response**: Returns to chat interface without processing (empty prompt ignored)

#### 2. LLM Service Unavailable
**Scenario**: Groq API is down or API key is invalid

**Response**: HTML page with error message:
```html
<div class="error-message">
    Error: Failed to load an LLM from Groq - Invalid API key
</div>
```

#### 3. Vector Store Issues
**Scenario**: FAISS database is corrupted or missing

**Response**: HTML page with error message:
```html
<div class="error-message">
    Error: Vector store not present or empty
</div>
```

### Error Response Format

All errors are displayed within the chat interface with the following structure:

```html
<div class="message assistant-message error">
    <div class="message-content">
        <strong>Error:</strong> [Error Description]
    </div>
    <div class="message-timestamp">[Timestamp]</div>
</div>
```

## 🔒 Security Considerations

### Input Validation
- All user inputs are sanitized to prevent XSS attacks
- SQL injection protection (though not using SQL database)
- Length limits on input queries (max 1000 characters)

### Rate Limiting (Recommended for Production)
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "10 per minute"]
)

@app.route("/", methods=["POST"])
@limiter.limit("5 per minute")
def process_query():
    # Process medical query
    pass
```

### CORS Configuration
For API access from web applications:
```python
from flask_cors import CORS

CORS(app, origins=["https://your-frontend-domain.com"])
```

## 📊 Performance Characteristics

### Response Times
- **Simple queries**: 1-3 seconds
- **Complex queries**: 3-7 seconds
- **Vector search**: 200-500ms
- **LLM inference**: 1-5 seconds

### Throughput
- **Concurrent users**: Up to 10 (single instance)
- **Queries per minute**: ~20 (depending on complexity)
- **Memory usage**: 2-4GB (with vector database loaded)

### Optimization Tips
1. **Caching**: Implement Redis for frequently asked questions
2. **Load Balancing**: Use multiple instances behind a load balancer
3. **CDN**: Serve static assets through CDN
4. **Database Optimization**: Regular FAISS index optimization

## 🛠️ Development & Testing

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run in debug mode
export FLASK_ENV=development
export FLASK_DEBUG=True
python app/application.py
```

### API Testing Scripts

#### Basic Health Check
```python
import requests

def test_health():
    response = requests.get("http://localhost:5000/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

test_health()
print("Health check passed!")
```

#### Query Testing
```python
import requests

def test_query():
    data = {"prompt": "What causes headaches?"}
    response = requests.post("http://localhost:5000/", data=data)
    assert response.status_code == 200
    # Check if response contains expected content
    assert "headache" in response.text.lower()

test_query()
print("Query test passed!")
```

### Load Testing
```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:5000/

# Using curl for POST requests
for i in {1..10}; do
  curl -X POST http://localhost:5000/ \
    -d "prompt=Test query $i" &
done
wait
```

## 📈 Monitoring & Analytics

### Metrics Collection
Implement custom metrics for monitoring:

```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
QUERY_COUNT = Counter('medical_queries_total', 'Total medical queries processed')
RESPONSE_TIME = Histogram('query_response_seconds', 'Time spent processing queries')
ERROR_COUNT = Counter('query_errors_total', 'Total query errors', ['error_type'])

@app.route('/metrics')
def metrics():
    return generate_latest()
```

### Usage Analytics
Track common query patterns:

```python
# Log query categories
QUERY_CATEGORIES = {
    'symptoms': ['symptom', 'sign', 'feel', 'hurt'],
    'treatment': ['treat', 'cure', 'medicine', 'therapy'],
    'diagnosis': ['diagnose', 'test', 'exam', 'check']
}

def categorize_query(query):
    query_lower = query.lower()
    for category, keywords in QUERY_CATEGORIES.items():
        if any(keyword in query_lower for keyword in keywords):
            return category
    return 'general'
```

## 🔄 Version History

### API Versions

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-21 | Initial API release |
| 1.1.0 | TBD | Add authentication endpoints |
| 1.2.0 | TBD | Add query history API |
| 2.0.0 | TBD | REST API with JSON responses |

## 📞 Support & Contact

### API Support
- **GitHub Issues**: [Report API issues](https://github.com/anishks07/Medical-Chatbot/issues)
- **Documentation**: [Main README](README.md)
- **Deployment Guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### Contributing to API
1. Fork the repository
2. Create feature branch for API changes
3. Add tests for new endpoints
4. Update this documentation
5. Submit pull request

---

**Note**: This API is designed for educational and informational purposes. Always consult healthcare professionals for medical advice.
