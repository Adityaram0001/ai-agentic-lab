"""
CrewAI 02: Social Media Content Multi-Format Factory
"""
import sys
import os

# Add root to sys.path to access shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.llm_config import get_langchain_llm
from shared.utils import setup_logger

logger = setup_logger(__name__)

def main():
    logger.info("Starting CrewAI 02: Social Media Content Multi-Format Factory")
    # TODO: Implement agent logic here

if __name__ == "__main__":
    main()
