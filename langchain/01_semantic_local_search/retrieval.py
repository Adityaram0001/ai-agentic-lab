"""
LCEL RAG Pipeline for Semantic Local File Search & QA
"""
import os
import sys

# Add root to sys.path to access shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from shared.llm_config import get_langchain_llm

DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain(reasoning_effort="low"):
    """
    Builds and returns the LCEL Retrieval-Augmented Generation chain.
    """
    # 1. Initialize Embeddings and Vector Store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 2. Initialize LLM
    llm = get_langchain_llm(reasoning_effort=reasoning_effort)

    # 3. Create Prompt
    template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:"""
    prompt = PromptTemplate.from_template(template)

    # 4. Construct LCEL Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
