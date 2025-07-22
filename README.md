# 🏥 AI Medical Chatbot

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)](https://langchain.readthedocs.io/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Database-red.svg)](https://faiss.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A sophisticated AI-powered medical chatbot that provides accurate medical information using Retrieval-Augmented Generation (RAG) with LLaMA 3.1 and medical literature databases.

## 🌟 Key Features

- **🤖 Advanced AI Model**: Powered by LLaMA 3.1 8B Instant via Groq API for fast, accurate responses
- **📚 Medical Knowledge Base**: Built on comprehensive medical literature including Oxford Handbook of Clinical Medicine and Gale Encyclopedia of Medicine
- **🔍 Intelligent Retrieval**: FAISS vector database with semantic search for contextually relevant answers
- **💬 Interactive Web Interface**: Clean, responsive Flask-based chat interface
- **🔒 Secure & Scalable**: Docker containerization with proper environment variable management
- **📊 Production Ready**: Comprehensive logging, error handling, and deployment automation

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │ -> │   Flask Web App  │ -> │   QA Chain      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                │                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Chat Interface │    │ Vector Retriever│
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ FAISS Database  │
                                              │ (Medical PDFs)  │
                                              └─────────────────┘
```

### 🧠 Technical Stack

- **Backend**: Python 3.10+, Flask
- **AI/ML**: LangChain, LLaMA 3.1 (via Groq), HuggingFace Sentence Transformers
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Document Processing**: PyPDF for medical literature processing
- **Deployment**: Docker, Jenkins CI/CD pipeline
- **Frontend**: HTML5, CSS3, JavaScript with modern responsive design

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Docker (optional, for containerized deployment)
- Groq API key ([Get it here](https://console.groq.com/))

### 1. Clone & Setup

```bash
git clone https://github.com/anishks07/Medical-Chatbot.git
cd Medical-Chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here  # Optional, for additional models
```

### 3. Initialize Vector Database

```bash
# Process medical PDFs and create vector store
python app/components/data_loader.py
```

### 4. Launch Application

```bash
# Start the Flask application
python app/application.py
```

Visit `http://localhost:5000` to access the medical chatbot interface.

## 🐳 Docker Deployment

### Build and Run

```bash
# Build Docker image
docker build -t medical-chatbot .

# Run container
docker run -p 5000:5000 --env-file .env medical-chatbot
```

### Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  medical-chatbot:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - HF_TOKEN=${HF_TOKEN}
    volumes:
      - ./vector_store:/app/vector_store
      - ./logs:/app/logs
```

Run with: `docker-compose up -d`

## 📁 Project Structure

```
Medical-Chatbot/
├── app/
│   ├── __init__.py
│   ├── application.py          # Main Flask application
│   ├── common/
│   │   ├── custom_exception.py # Custom error handling
│   │   └── logger.py          # Logging configuration
│   ├── components/
│   │   ├── data_loader.py     # PDF processing pipeline
│   │   ├── embeddings.py      # Text embedding models
│   │   ├── llm.py            # LLaMA model integration
│   │   ├── pdf_loader.py     # PDF document processing
│   │   ├── retriever.py      # QA chain creation
│   │   └── vector_store.py   # FAISS database management
│   ├── config/
│   │   └── config.py         # Application configuration
│   └── templates/
│       └── index.html        # Web interface
├── data/                     # Medical literature PDFs
├── vector_store/            # FAISS vector database
├── logs/                    # Application logs
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
└── setup.py               # Package installation
```

## 🔧 Configuration Options

### Model Configuration (`app/config/config.py`)

```python
# Groq LLaMA Configuration
GROQ_MODEL_NAME = "llama3-8b-8192"  # or "mixtral-8x7b-32768"

# Vector Database
DB_FAISS_PATH = "vector_store/db_faiss"
CHUNK_SIZE = 500          # Text chunk size for processing
CHUNK_OVERLAP = 50        # Overlap between chunks

# Data Processing
DATA_PATH = "data/"       # Path to medical PDFs
```

### Custom Prompt Template

The system uses a specialized medical prompt template:

```python
CUSTOM_PROMPT_TEMPLATE = """
Answer the following medical question in 4-5 lines maximum using only 
the information provided in the context.

Context: {context}
Question: {question}
Answer:
"""
```

## 🧪 Usage Examples

### Basic Medical Query
```
User: "What are the symptoms of diabetes?"
Bot: "Based on medical literature, diabetes symptoms include increased thirst, 
frequent urination, extreme fatigue, blurred vision, and slow-healing wounds. 
Type 1 diabetes may also present with rapid weight loss, while Type 2 diabetes 
often develops gradually with these symptoms becoming more apparent over time."
```

### Diagnostic Information
```
User: "Explain hypertension treatment options"
Bot: "Hypertension treatment typically involves lifestyle modifications including 
dietary changes (reduced sodium, DASH diet), regular exercise, and weight management. 
Pharmacological options include ACE inhibitors, ARBs, calcium channel blockers, 
and diuretics, often used in combination based on patient response and comorbidities."
```

## 🛠️ Development

### Adding New Medical Documents

1. Place PDF files in the `data/` directory
2. Run the vector store initialization:
   ```bash
   python app/components/data_loader.py
   ```

### Customizing the AI Model

Modify `app/components/llm.py` to use different models:

```python
def load_llm(model_name: str = "llama-3.1-70b-versatile"):  # Larger model
    # Configuration here
```

### Extending Functionality

- **Add new document types**: Extend `pdf_loader.py` to support DOCX, TXT files
- **Implement user authentication**: Add session management and user profiles
- **Create API endpoints**: Build REST API for mobile app integration
- **Add conversation memory**: Implement chat history and context retention

## 📊 Performance & Monitoring

### Logging

Comprehensive logging is implemented across all components:

- **Application logs**: Stored in `logs/` directory
- **Error tracking**: Custom exception handling with detailed error messages
- **Performance monitoring**: Response time and model inference tracking

### Metrics

- **Response Time**: Typically 2-5 seconds for complex medical queries
- **Accuracy**: Based on medical literature corpus coverage
- **Scalability**: Supports concurrent users with proper resource allocation

## 🚀 Production Deployment

### Environment Setup

1. **Server Requirements**:
   - 4+ GB RAM for vector database
   - 2+ CPU cores for concurrent requests
   - SSD storage for fast vector search

2. **Security Considerations**:
   - Environment variable management
   - HTTPS implementation
   - Rate limiting for API protection

3. **Scaling Options**:
   - Load balancer for multiple instances
   - Redis for session management
   - Kubernetes for orchestration

### CI/CD Pipeline

The project includes Jenkins pipeline configuration:

```bash
# Automated testing and deployment
./Jenkinsfile  # Contains complete CI/CD workflow
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 coding standards
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation for API changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Important**: This chatbot is designed for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.

## 👨‍💻 Author

**Anish Konda**
- GitHub: [@anishks07](https://github.com/anishks07)
- Email: [Contact Information]

## 🙏 Acknowledgments

- **Medical Literature**: Oxford Handbook of Clinical Medicine, Gale Encyclopedia of Medicine
- **AI Models**: Meta's LLaMA 3.1, Groq for fast inference
- **Vector Database**: Facebook AI Similarity Search (FAISS)
- **Framework**: LangChain for RAG implementation

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

[Report Bug](https://github.com/anishks07/Medical-Chatbot/issues) • [Request Feature](https://github.com/anishks07/Medical-Chatbot/issues) • [Documentation](https://github.com/anishks07/Medical-Chatbot/wiki)

</div>