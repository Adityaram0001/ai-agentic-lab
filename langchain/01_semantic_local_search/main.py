"""
LangChain 01: Semantic Local File Search & QA
CLI Chat Interface
"""
import sys
import os

# Add root to sys.path to access shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from retrieval import build_rag_chain
from shared.utils import setup_logger

logger = setup_logger(__name__)

def main():
    logger.info("Initializing Local Semantic Search Pipeline...")
    
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "chroma_db")):
        logger.error("Vector database not found. Please run 'python ingest.py' first.")
        return

    logger.info("Building RAG Chain...")
    chain = build_rag_chain(reasoning_effort="low")
    
    print("\n" + "="*50)
    print("Welcome to Local File RAG Agent!")
    print("Type your question below. Type 'exit' or 'quit' to stop.")
    print("="*50 + "\n")
    
    while True:
        try:
            query = input("\nQ: ")
            if query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not query.strip():
                continue
                
            print("Thinking...")
            # Run the LCEL chain
            response = chain.invoke(query)
            print(f"\nA: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
