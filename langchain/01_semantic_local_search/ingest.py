"""
Ingestion script for Semantic Local File Search & QA
"""
import os
import sys

# Add root to sys.path to access shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.utils import setup_logger
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

logger = setup_logger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def main():
    logger.info(f"Starting ingestion process for directory: {DATA_DIR}")
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        logger.info(f"Created {DATA_DIR}. Please add some files and run again.")
        return

    # 1. Load Documents
    logger.info("Loading documents...")
    loaders = {
        ".txt": TextLoader,
        ".md": TextLoader,
        ".pdf": PyPDFLoader,
    }
    
    documents = []
    for ext, loader_cls in loaders.items():
        loader = DirectoryLoader(DATA_DIR, glob=f"**/*{ext}", loader_cls=loader_cls)
        docs = loader.load()
        if docs:
            logger.info(f"Loaded {len(docs)} {ext} documents.")
            documents.extend(docs)

    if not documents:
        logger.warning("No documents found in the data directory.")
        return

    # 2. Split Documents
    logger.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # 3. Create Embeddings & Store in Chroma
    logger.info("Initializing HuggingFace Embeddings model...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    logger.info("Creating local Chroma vector store...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    logger.info(f"Successfully ingested {len(chunks)} chunks into {DB_DIR}")

if __name__ == "__main__":
    main()
