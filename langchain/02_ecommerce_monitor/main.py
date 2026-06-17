"""
LangChain 02: Structured E-Commerce Competitor Monitor
"""
import sys
import os
import json

# Add root to sys.path to access shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared.utils import setup_logger
from shared.llm_config import get_langchain_llm
from schema import ProductInfo
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

logger = setup_logger(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def main():
    logger.info("Initializing Structured E-Commerce Extractor...")
    
    # 1. Initialize LLM
    llm = get_langchain_llm(reasoning_effort="low")
    
    # 2. Setup Output Parser
    parser = PydanticOutputParser(pydantic_object=ProductInfo)
    
    # 3. Create the Prompt Template
    prompt = PromptTemplate(
        template="Extract the product information from the following raw HTML snippet.\n\n{format_instructions}\n\nHTML:\n{html_snippet}\n",
        input_variables=["html_snippet"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # 4. Construct LCEL Chain
    extraction_chain = prompt | llm | parser

    # 5. Process files
    if not os.path.exists(DATA_DIR):
        logger.error(f"Data directory not found at {DATA_DIR}")
        return

    html_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.html')]
    if not html_files:
        logger.warning(f"No HTML files found in {DATA_DIR}")
        return

    print("\n" + "="*50)
    print("Competitor Product Extraction System")
    print("="*50 + "\n")

    for filename in sorted(html_files):
        filepath = os.path.join(DATA_DIR, filename)
        logger.info(f"Processing {filename}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        try:
            # Execute extraction
            product_data = extraction_chain.invoke({"html_snippet": html_content})
            
            # product_data is a strongly-typed ProductInfo Pydantic object
            print(f"\n--- Extracted Data from {filename} ---")
            print(f"Name:     {product_data.product_name}")
            print(f"Price:    {product_data.price} ({product_data.currency})")
            print(f"In Stock: {product_data.in_stock}")
            print("-" * 40)
            
        except Exception as e:
            logger.error(f"Failed to extract data from {filename}: {e}")

if __name__ == "__main__":
    main()
