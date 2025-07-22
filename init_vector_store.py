#!/usr/bin/env python3
"""
Medical Chatbot Vector Store Initialization

This script initializes the FAISS vector database by processing medical PDF documents
and creating embeddings for semantic search. It should be run once after setup or
whenever new medical documents are added to the data directory.

Usage:
    python init_vector_store.py [--force] [--data-path PATH] [--output-path PATH]

Arguments:
    --force         Force regeneration even if vector store exists
    --data-path     Path to directory containing PDF files (default: data/)
    --output-path   Path for vector store output (default: vector_store/db_faiss)
    --chunk-size    Text chunk size in characters (default: 500)
    --chunk-overlap Overlap between chunks in characters (default: 50)

Examples:
    python init_vector_store.py
    python init_vector_store.py --force --chunk-size 750
    python init_vector_store.py --data-path /path/to/pdfs --output-path /path/to/output

Requirements:
    - Medical PDF files in the data directory
    - Sufficient RAM (4GB+ recommended for large document sets)
    - Internet connection for downloading embedding models (first run)

Author: Anish Konda
License: MIT
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.components.data_loader import process_and_store_pdfs
from app.config.config import DB_FAISS_PATH, DATA_PATH
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def check_prerequisites():
    """Check if all prerequisites are met before processing."""
    logger.info("Checking prerequisites...")
    
    # Check if data directory exists and has PDF files
    if not os.path.exists(DATA_PATH):
        raise CustomException(f"Data directory not found: {DATA_PATH}")
    
    pdf_files = [f for f in os.listdir(DATA_PATH) if f.lower().endswith('.pdf')]
    if not pdf_files:
        raise CustomException(f"No PDF files found in {DATA_PATH}")
    
    logger.info(f"Found {len(pdf_files)} PDF files in {DATA_PATH}")
    for pdf_file in pdf_files:
        file_path = os.path.join(DATA_PATH, pdf_file)
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        logger.info(f"  - {pdf_file} ({file_size_mb:.1f} MB)")
    
    # Check available disk space
    import shutil
    free_space_gb = shutil.disk_usage('.').free / (1024**3)
    if free_space_gb < 1:
        logger.warning(f"Low disk space: {free_space_gb:.1f} GB available")
    
    logger.info("Prerequisites check completed successfully")

def estimate_processing_time(pdf_count, total_size_mb):
    """Estimate processing time based on document count and size."""
    # Rough estimates: 1MB per minute of processing
    estimated_minutes = max(1, int(total_size_mb / 1))
    return estimated_minutes

def main():
    """Main function to initialize vector store with command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Initialize FAISS vector store from medical PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--force', 
        action='store_true',
        help='Force regeneration even if vector store exists'
    )
    
    parser.add_argument(
        '--data-path',
        default=DATA_PATH,
        help=f'Path to directory containing PDF files (default: {DATA_PATH})'
    )
    
    parser.add_argument(
        '--output-path',
        default=DB_FAISS_PATH,
        help=f'Path for vector store output (default: {DB_FAISS_PATH})'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=500,
        help='Text chunk size in characters (default: 500)'
    )
    
    parser.add_argument(
        '--chunk-overlap',
        type=int,
        default=50,
        help='Overlap between chunks in characters (default: 50)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel('DEBUG')
    
    try:
        logger.info("="*60)
        logger.info("Medical Chatbot Vector Store Initialization")
        logger.info("="*60)
        
        # Update configuration if custom paths provided
        if args.data_path != DATA_PATH:
            import app.config.config as config
            config.DATA_PATH = args.data_path
            logger.info(f"Using custom data path: {args.data_path}")
        
        if args.output_path != DB_FAISS_PATH:
            import app.config.config as config
            config.DB_FAISS_PATH = args.output_path
            logger.info(f"Using custom output path: {args.output_path}")
        
        if args.chunk_size != 500:
            import app.config.config as config
            config.CHUNK_SIZE = args.chunk_size
            logger.info(f"Using custom chunk size: {args.chunk_size}")
        
        if args.chunk_overlap != 50:
            import app.config.config as config
            config.CHUNK_OVERLAP = args.chunk_overlap
            logger.info(f"Using custom chunk overlap: {args.chunk_overlap}")
        
        # Check if vector store already exists
        if os.path.exists(args.output_path) and not args.force:
            logger.warning(f"Vector store already exists at {args.output_path}")
            logger.warning("Use --force to regenerate or remove the directory manually")
            
            response = input("Do you want to continue and overwrite? (y/N): ")
            if response.lower() != 'y':
                logger.info("Operation cancelled by user")
                return
        
        # Check prerequisites
        check_prerequisites()
        
        # Calculate estimates
        pdf_files = [f for f in os.listdir(args.data_path) if f.lower().endswith('.pdf')]
        total_size_mb = sum(
            os.path.getsize(os.path.join(args.data_path, f)) 
            for f in pdf_files
        ) / (1024 * 1024)
        
        estimated_time = estimate_processing_time(len(pdf_files), total_size_mb)
        
        logger.info(f"Processing {len(pdf_files)} PDF files ({total_size_mb:.1f} MB total)")
        logger.info(f"Estimated processing time: {estimated_time} minutes")
        logger.info(f"Output directory: {args.output_path}")
        
        # Start processing
        start_time = time.time()
        logger.info("Starting vector store creation...")
        
        # Call the main processing function
        process_and_store_pdfs()
        
        # Calculate actual processing time
        end_time = time.time()
        actual_time_minutes = (end_time - start_time) / 60
        
        logger.info("="*60)
        logger.info("Vector Store Creation Completed Successfully!")
        logger.info("="*60)
        logger.info(f"Processing time: {actual_time_minutes:.1f} minutes")
        logger.info(f"Vector store location: {args.output_path}")
        
        # Verify the created vector store
        if os.path.exists(args.output_path):
            index_file = os.path.join(args.output_path, "index.faiss")
            pkl_file = os.path.join(args.output_path, "index.pkl")
            
            if os.path.exists(index_file) and os.path.exists(pkl_file):
                index_size_mb = os.path.getsize(index_file) / (1024 * 1024)
                pkl_size_mb = os.path.getsize(pkl_file) / (1024 * 1024)
                
                logger.info(f"Vector index size: {index_size_mb:.1f} MB")
                logger.info(f"Metadata size: {pkl_size_mb:.1f} MB")
                logger.info("Vector store files verified successfully")
            else:
                logger.error("Vector store files not found after creation")
                return 1
        else:
            logger.error("Vector store directory not found after creation")
            return 1
        
        logger.info("\nNext steps:")
        logger.info("1. Start the Flask application: python app/application.py")
        logger.info("2. Or use Docker: docker-compose up -d")
        logger.info("3. Access the chatbot at http://localhost:5000")
        
        return 0
        
    except CustomException as e:
        logger.error(f"Application error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error("Please check the logs for more details")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)