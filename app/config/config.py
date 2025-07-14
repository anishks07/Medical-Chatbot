import os
HF_TOKEN = os.environ.get("HF_TOKEN")

HUGGINGFACEHUB_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
DB_FIASS_PATH="vector_store/db_faiss"
DATA_PATH = "data/"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50