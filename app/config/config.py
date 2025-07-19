import os
HF_TOKEN = os.environ.get("HF_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Groq model configuration
GROQ_MODEL_NAME = "llama3-8b-8192"  # You can change this to other Groq models like "mixtral-8x7b-32768"

# Legacy HuggingFace config (keeping for reference)
HUGGINGFACEHUB_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

DB_FAISS_PATH="vector_store/db_faiss"
DATA_PATH = "data/"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50