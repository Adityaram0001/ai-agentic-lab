# LangChain Project 1: Semantic Local File Search & QA

## 🎯 Project Goal
The primary objective of this project is to master the fundamentals of **Retrieval-Augmented Generation (RAG)** using LangChain. Rather than relying on an LLM's pre-trained knowledge, which is static and generalized, this project demonstrates how to ground the LLM's responses in your own private, local documents. 

By building a script that watches a local directory, automatically splits text, chunks PDF/Markdown files, and queries this local knowledge base, we learn the core pipeline logistics of LangChain: moving unstructured data from the file system into a structured vector space, and seamlessly routing it to an LLM using the LangChain Expression Language (LCEL).

---

## 🏗️ Architecture & Design

This project is divided into two distinct, decoupled pipelines: the **Ingestion Pipeline** (offline processing) and the **Retrieval Pipeline** (online querying).

### 1. The Ingestion Pipeline (`ingest.py`)
Before we can chat with our documents, we must convert them into a format the LLM can understand semantically. This involves four steps:

- **Document Loading (`DirectoryLoader`)**: We use LangChain's loaders (`TextLoader`, `PyPDFLoader`) to scan the `data/` directory. These loaders handle the messy work of extracting raw text from different file formats, returning a standardized `Document` object containing the `page_content` and `metadata` (like source file path).
- **Text Splitting (`RecursiveCharacterTextSplitter`)**: LLMs have finite context windows. We cannot feed a 500-page PDF into a prompt. The text splitter breaks documents into manageable "chunks" (e.g., 1000 characters) with a slight overlap (200 characters). The overlap is critical; it prevents sentences or thoughts from being cut in half, preserving semantic meaning across chunks.
- **Embedding Generation (`HuggingFaceEmbeddings`)**: We pass each chunk through an embedding model (`all-MiniLM-L6-v2`). This model maps the text into a high-dimensional vector space. In this space, chunks with similar meanings (e.g., "puppy" and "dog") are mathematically closer together than unrelated chunks (e.g., "puppy" and "laptop").
- **Vector Storage (`Chroma`)**: Finally, these vectors and their corresponding text chunks are saved into a local database (`ChromaDB`). Because it's local, your private data never leaves your machine during the ingestion phase.

### 2. The Retrieval Pipeline (`retrieval.py` & `main.py`)
When a user asks a question, the system must find the relevant context and generate an answer.

- **The Retriever**: The user's query is converted into a vector using the *exact same* embedding model used during ingestion. ChromaDB then performs a "similarity search" (often Cosine Similarity), finding the top `k` chunks in the database that are mathematically closest to the query vector.
- **The Prompt Template**: We inject the retrieved chunks and the user's original question into a strict prompt template. This template specifically instructs the LLM: *"Use the following pieces of context to answer the question... If you don't know the answer based on the context, just say that you don't know."* This mitigates hallucinations.
- **LCEL (LangChain Expression Language)**: We tie it all together using LangChain's declarative syntax:
  ```python
  rag_chain = (
      {"context": retriever | format_docs, "question": RunnablePassthrough()}
      | prompt
      | llm
      | StrOutputParser()
  )
  ```
  This reads beautifully: Take the query, pass it to the retriever to get the context, pass both to the prompt, send the prompt to the Azure LLM, and parse the output as a simple string.

---

## 💻 Detailed Code Walkthrough

### The Shared Configuration (`shared/llm_config.py`)
A cornerstone of this lab's architecture is the central LLM configuration. Instead of hardcoding API keys in every script, we use a shared utility that loads Azure credentials from a `.env` file. 

```python
def get_langchain_llm(reasoning_effort="low", temperature=1):
    return AzureChatOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
        azure_deployment=AZURE_DEPLOYMENT_NAME,
        temperature=temperature,
        model_kwargs={"reasoning_effort": reasoning_effort}
    )
```
Notice the `model_kwargs={"reasoning_effort": reasoning_effort}`. This allows us to dynamically tell the `gpt-5-nano` deployment how much compute to spend on the prompt, optimizing for speed or depth depending on the task. The `temperature` is strictly set to `1` as required by this specific model generation.

### The Ingestion Script (`ingest.py`)
This script is executed manually whenever new documents are added to the `data/` folder. 

1. **Safety Checks**: It ensures the `data/` directory exists.
2. **Iterative Loading**: It iterates through a dictionary mapping file extensions (`.txt`, `.md`, `.pdf`) to their respective LangChain loaders.
3. **Chunking**: It applies the `RecursiveCharacterTextSplitter`.
4. **Persisting**: It initializes `Chroma.from_documents` and saves the database to the `chroma_db/` folder.

### The Retrieval Logic (`retrieval.py`)
This file encapsulates the complex RAG logic into a single callable function `build_rag_chain()`. By separating the chain definition from the CLI interface, we make the RAG pipeline highly reusable. If we later wanted to attach a Flask/FastAPI web server, we could simply import `build_rag_chain()` without touching the core logic.

### The CLI Interface (`main.py`)
The user-facing entry point. It features a robust `while True` loop that continuously accepts standard input. It wraps the `chain.invoke(query)` call in a `try/except` block to gracefully handle API timeouts or Keyboard Interrupts (Ctrl+C).

---

## 🧠 Key Learnings & Takeaways

1. **The Importance of Clean Chunking**: During development, it becomes obvious that RAG is only as good as its data ingestion. If chunk sizes are too small, the LLM loses context (e.g., a pronoun without its noun). If chunks are too large, the context window fills up with irrelevant noise, diluting the LLM's attention and increasing API costs. The `chunk_overlap` parameter is a critical safety net.
2. **Local Embeddings Save Money**: By utilizing HuggingFace's `sentence-transformers` for embeddings locally, we avoided paying per-token API costs just to index our documents. We only utilize the expensive, powerful Azure `gpt-5-nano` model for the final reasoning and generation step.
3. **The Elegance of LCEL**: Prior to LCEL, LangChain required clunky, opaque wrapper classes (like `ConversationalRetrievalChain`). LCEL (`|`) exposes the exact data flow. You can see exactly how the dictionary is constructed, how the prompt consumes it, and how the LLM receives it. It embraces the Unix philosophy of chaining small, predictable functions.
4. **Preventing Hallucinations**: By strictly prompting the model to *only* use the provided context and to admit ignorance if the answer isn't there, we transform a creative, hallucination-prone text generator into a highly deterministic, reliable query engine.

---

## 🚀 How to Run the Project

1. Activate the environment: `source ../../venv/bin/activate`
2. Add your documents to the `data/` folder.
3. Build the database: `python ingest.py`
4. Start the chat: `python main.py`
