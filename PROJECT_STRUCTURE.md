# 📁 Project Structure Documentation

> Detailed breakdown of the Medical Chatbot project architecture and file organization

## 🏗️ Project Overview

The Medical Chatbot is organized following Python best practices with a modular, scalable architecture. The project uses a component-based design that separates concerns and enables easy maintenance and testing.

```
Medical-Chatbot/
├── 📄 Configuration Files
├── 🐳 Deployment Files  
├── 📚 Application Code
├── 📊 Data & Models
├── 📝 Documentation
└── 🔧 Development Tools
```

## 📂 Complete Directory Structure

```
Medical-Chatbot/
│
├── 📄 README.md                    # Main project documentation
├── 📄 DEPLOYMENT_GUIDE.md          # Deployment instructions
├── 📄 API_DOCUMENTATION.md         # API reference guide
├── 📄 requirements.txt             # Python dependencies
├── 📄 pyproject.toml              # Modern Python project config
├── 📄 setup.py                    # Package installation script
├── 📄 uv.lock                     # Dependency lock file
├── 📄 .env.example                # Environment variables template
│
├── 🐳 Dockerfile                   # Container configuration
├── 🐳 docker-compose.yml          # Multi-container deployment
├── 🔧 Jenkinsfile                 # CI/CD pipeline configuration
│
├── 🚀 main.py                     # Entry point (simple version)
├── 🚀 startup.py                  # Production startup script
├── 📊 init_vector_store.py        # Vector database initialization
├── 🧪 test_deployment.py          # Deployment testing
│
├── 📚 app/                        # Main application package
│   ├── 📄 __init__.py             # Package initialization
│   ├── 🌐 application.py          # Flask web application
│   │
│   ├── 🧠 components/             # Core AI/ML components
│   │   ├── 📄 __init__.py
│   │   ├── 📊 data_loader.py      # PDF processing pipeline
│   │   ├── 🔤 embeddings.py       # Text embedding models
│   │   ├── 🤖 llm.py             # Language model integration
│   │   ├── 📖 pdf_loader.py       # PDF document processing
│   │   ├── 🔍 retriever.py        # Question-answering chain
│   │   └── 💾 vector_store.py     # FAISS database management
│   │
│   ├── ⚙️ config/                # Configuration management
│   │   ├── 📄 __init__.py
│   │   └── 📄 config.py           # Application settings
│   │
│   ├── 🛠️ common/                # Shared utilities
│   │   ├── 📄 __init__.py
│   │   ├── ⚠️ custom_exception.py # Error handling
│   │   └── 📝 logger.py           # Logging configuration
│   │
│   ├── 🎨 templates/             # Web interface templates
│   │   └── 📄 index.html          # Main chat interface
│   │
│   └── 📁 __pycache__/           # Python bytecode cache
│
├── 📊 data/                       # Medical literature storage
│   ├── 📖 Oxford_Handbook_Clinical_Medicine.pdf
│   └── 📖 Gale_Encyclopedia_Medicine.pdf
│
├── 💾 vector_store/              # FAISS vector database
│   └── 📁 db_faiss/
│       ├── 📄 index.faiss         # Vector index file
│       └── 📄 index.pkl           # Metadata pickle file
│
├── 📝 logs/                      # Application logs
│   ├── 📄 log_2025-07-17.log
│   ├── 📄 log_2025-07-19.log
│   ├── 📄 log_2025-07-20.log
│   └── 📄 log_2025-07-21.log
│
├── 🔧 custom_jenkins/            # Custom Jenkins configuration
│   └── 🐳 Dockerfile             # Jenkins container setup
│
└── 📦 medical_chatbot.egg-info/  # Package metadata
    ├── 📄 dependency_links.txt
    ├── 📄 PKG-INFO
    ├── 📄 requires.txt
    ├── 📄 SOURCES.txt
    └── 📄 top_level.txt
```

## 🔍 Detailed File Analysis

### 📄 Root Configuration Files

#### `requirements.txt`
```txt
langchain>=0.1.0           # LLM orchestration framework
langchain_community>=0.3.0 # Community extensions
langchain_huggingface      # HuggingFace integrations
langchain-groq            # Groq API integration
faiss-cpu                 # Vector similarity search
pypdf                     # PDF document processing
python-dotenv             # Environment variable management
flask                     # Web framework
huggingface-hub          # Model hub access
sentence-transformers    # Text embeddings
```

#### `setup.py`
```python
from setuptools import setup, find_packages

# Package configuration for pip installation
setup(
    name="Medical-Chatbot",
    version="0.1.0", 
    author="Anish Konda",
    packages=find_packages(),
    install_requires=[...],  # From requirements.txt
)
```

#### `pyproject.toml`
Modern Python project configuration following PEP 518 standards.

### 🐳 Deployment Files

#### `Dockerfile`
```dockerfile
FROM python:3.10-slim       # Lightweight Python base image
ENV PYTHONDONTWRITEBYTECODE=1  # Prevent .pyc files
ENV PYTHONUNBUFFERED=1      # Real-time output
WORKDIR /app                # Application directory
# System dependencies, Python packages, app setup
EXPOSE 5000                 # Flask default port
CMD ["python", "app/application.py"]
```

#### `Jenkinsfile`
CI/CD pipeline configuration for automated:
- Code checkout and testing
- Docker image building
- Deployment automation
- Health checks and rollback

### 📚 Application Code Structure

#### `app/application.py` - Web Server
```python
# Main Flask application
# - Route handling (/,  /clear)
# - Session management
# - Template rendering
# - Error handling integration
# - QA chain orchestration
```

**Key Features:**
- Session-based chat history
- Custom Jinja2 filters for formatting
- Error boundary implementation
- Integration with AI components

#### `app/components/` - AI/ML Core

##### `llm.py` - Language Model Integration
```python
from langchain_groq import ChatGroq

def load_llm(model_name="llama-3.1-8b-instant"):
    """Load LLaMA model via Groq API"""
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=model_name,
        temperature=0.3,        # Balanced creativity
        max_tokens=512,         # Response length limit
    )
```

##### `embeddings.py` - Text Embeddings
```python
from sentence_transformers import SentenceTransformer

def get_embedding_model():
    """Load sentence transformer for text embeddings"""
    return SentenceTransformer('all-MiniLM-L6-v2')
    # Fast, efficient embeddings for semantic search
```

##### `vector_store.py` - FAISS Database
```python
from langchain_community.vectorstores import FAISS

def load_vector_store():
    """Load existing FAISS vector database"""
    return FAISS.load_local(
        DB_FAISS_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

def save_vector_store(text_chunks):
    """Create new vector database from documents"""
    db = FAISS.from_documents(text_chunks, embedding_model)
    db.save_local(DB_FAISS_PATH)
```

##### `pdf_loader.py` - Document Processing
```python
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdf_files():
    """Extract text from medical PDF files"""
    
def create_text_chunks(documents):
    """Split documents into searchable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,      # 500 characters
        chunk_overlap=CHUNK_OVERLAP # 50 character overlap
    )
```

##### `retriever.py` - QA Chain Orchestration
```python
from langchain.chains import RetrievalQA

def create_qa_chain():
    """Create question-answering chain"""
    qa_chain = RetrievalQA.from_chain_type(
        llm=load_llm(),
        chain_type="stuff",                    # Concatenate context
        retriever=db.as_retriever(            # Vector search
            search_kwargs={'k': 3}             # Top 3 results
        ),
        chain_type_kwargs={
            'prompt': set_custom_prompt()      # Medical-specific prompt
        }
    )
```

##### `data_loader.py` - Processing Pipeline
```python
def process_and_store_pdfs():
    """Complete pipeline: PDF → Text → Chunks → Vectors"""
    documents = load_pdf_files()      # Extract text
    text_chunks = create_text_chunks() # Split into chunks  
    save_vector_store(text_chunks)    # Create FAISS index
```

#### `app/config/config.py` - Configuration Management
```python
import os

# API Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")

# Model Settings
GROQ_MODEL_NAME = "llama3-8b-8192"

# Database Paths
DB_FAISS_PATH = "vector_store/db_faiss"
DATA_PATH = "data/"

# Processing Parameters
CHUNK_SIZE = 500          # Optimal for medical text
CHUNK_OVERLAP = 50        # Maintains context continuity
```

#### `app/common/` - Shared Utilities

##### `logger.py` - Logging System
```python
import logging
from logging.handlers import RotatingFileHandler

def get_logger(name):
    """Create configured logger with file rotation"""
    logger = logging.getLogger(name)
    
    # File handler with rotation (10MB, 5 backups)
    file_handler = RotatingFileHandler(
        f'logs/log_{datetime.now().strftime("%Y-%m-%d")}.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
```

##### `custom_exception.py` - Error Handling
```python
class CustomException(Exception):
    """Enhanced exception with context and chaining"""
    
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception
        self.timestamp = datetime.now()
```

### 🎨 Web Interface

#### `app/templates/index.html`
Modern, responsive chat interface featuring:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Modern fonts and icons -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <!-- Gradient background with glassmorphism effects -->
    <!-- Responsive chat container -->
    <!-- Message bubbles with user/assistant styling -->
    <!-- Auto-scroll and typing indicators -->
    <!-- Error handling with elegant display -->
</body>
</html>
```

**UI Features:**
- 🎨 Modern glassmorphism design
- 📱 Fully responsive layout
- 💬 Chat bubble interface
- ⚡ Real-time message updates
- 🚨 Elegant error display
- 🔄 Auto-scroll to latest messages

## 💾 Data Architecture

### Vector Database Structure

```
vector_store/db_faiss/
├── index.faiss          # Binary vector index (FAISS format)
│   ├── Vector dimensions: 384 (all-MiniLM-L6-v2)
│   ├── Index type: IndexFlatL2 (exact search)
│   ├── Document count: ~1,247 chunks
│   └── Total size: ~15MB
│
└── index.pkl           # Metadata pickle file
    ├── Document mappings
    ├── Source file references  
    ├── Chunk boundaries
    └── Embedding metadata
```

### Document Processing Flow

```
📖 Medical PDFs (data/)
    ↓
📝 Text Extraction (PyPDF)
    ↓  
📊 Text Chunking (500 chars, 50 overlap)
    ↓
🔤 Embedding Generation (SentenceTransformer)
    ↓
💾 Vector Storage (FAISS)
    ↓
🔍 Semantic Search (Similarity)
    ↓
🤖 Context Retrieval (Top-K)
    ↓
💬 AI Response (LLaMA 3.1)
```

## 🔧 Development Workflow

### Local Development Setup

1. **Environment Preparation**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   ```bash
   cp .env.example .env
   # Add GROQ_API_KEY
   ```

3. **Database Initialization**
   ```bash
   python app/components/data_loader.py
   ```

4. **Application Start**
   ```bash
   python app/application.py
   ```

### Testing Structure

```
tests/                    # Test directory (to be created)
├── unit/
│   ├── test_llm.py      # LLM integration tests
│   ├── test_vector_store.py  # Vector database tests
│   ├── test_pdf_loader.py    # Document processing tests
│   └── test_retriever.py     # QA chain tests
├── integration/
│   ├── test_api.py      # API endpoint tests
│   └── test_workflow.py # End-to-end tests
└── fixtures/
    ├── sample.pdf       # Test documents
    └── expected_responses.json
```

### Code Quality Tools

```bash
# Linting and formatting
pip install black flake8 isort mypy

# Format code
black app/
isort app/

# Type checking  
mypy app/

# Linting
flake8 app/
```

## 🚀 Production Considerations

### Performance Optimization

1. **Vector Search Optimization**
   - FAISS index tuning for large datasets
   - Approximate search for speed (IndexIVFFlat)
   - GPU acceleration for embeddings

2. **Caching Strategy**
   - Redis for frequent queries
   - Vector search result caching
   - Embedding computation caching

3. **Scaling Architecture**
   ```
   Load Balancer (Nginx)
       ↓
   Flask App Instances (3+)
       ↓
   Shared Vector Store (NFS/S3)
       ↓
   Shared Cache (Redis Cluster)
   ```

### Security Enhancements

1. **Input Validation**
   ```python
   from wtforms import Form, TextAreaField, validators
   
   class QueryForm(Form):
       prompt = TextAreaField('Query', [
           validators.Length(min=1, max=1000),
           validators.DataRequired()
       ])
   ```

2. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   
   limiter = Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["100 per hour"]
   )
   ```

3. **Authentication** (Future Enhancement)
   ```python
   from flask_jwt_extended import JWTManager
   
   # JWT token-based authentication
   # User session management
   # API key validation
   ```

## 📊 Monitoring & Observability

### Logging Strategy

```python
# app/common/logger.py configuration
LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10*1024*1024,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['file', 'console'],
            'level': 'INFO'
        }
    }
}
```

### Metrics Collection

```python
# Prometheus metrics (future enhancement)
from prometheus_client import Counter, Histogram

QUERY_COUNT = Counter('medical_queries_total', 'Total queries')
RESPONSE_TIME = Histogram('query_duration_seconds', 'Response time')
ERROR_COUNT = Counter('query_errors_total', 'Query errors')
```

## 🔄 Future Enhancements

### Planned Features

1. **API Improvements**
   - RESTful JSON API
   - GraphQL endpoint
   - WebSocket for real-time chat

2. **AI Enhancements**
   - Multi-model support
   - Conversation memory
   - Citation tracking
   - Confidence scoring

3. **User Features**
   - User authentication
   - Chat history persistence
   - Favorite responses
   - Export conversations

4. **Medical Features**
   - Specialized medical models
   - Drug interaction checking
   - Symptom analysis
   - Medical image analysis

### Architecture Evolution

```
Current: Monolithic Flask App
    ↓
Phase 1: Microservices
    ├── API Gateway
    ├── Chat Service
    ├── Vector Search Service
    └── LLM Service
    ↓
Phase 2: Cloud-Native
    ├── Kubernetes Deployment
    ├── Managed Vector Database
    ├── Serverless Functions
    └── CDN Distribution
```

---

## 📞 Support & Contributing

### File-Specific Issues

- **PDF Processing**: Check `app/components/pdf_loader.py`
- **Vector Search**: Debug `app/components/vector_store.py`
- **AI Responses**: Investigate `app/components/llm.py`
- **Web Interface**: Examine `app/templates/index.html`

### Contributing Guidelines

1. **File Naming Convention**: snake_case for Python, kebab-case for configs
2. **Import Organization**: Standard library → Third-party → Local imports
3. **Documentation**: Docstrings for all functions and classes
4. **Error Handling**: Use custom exceptions with proper logging

---

This structure documentation provides a comprehensive understanding of how the Medical Chatbot project is organized and how each component contributes to the overall functionality.
