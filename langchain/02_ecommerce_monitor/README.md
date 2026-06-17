# LangChain Project 2: Structured E-Commerce Competitor Monitor

## 🎯 Project Goal
The goal of this project is to master **Deterministic Data Extraction** using LangChain. 

While LLMs are inherently probabilistic text generators, building software pipelines requires deterministic, strongly-typed data. This project bridges that gap. By simulating an e-commerce competitor monitoring tool, we take messy, unstructured HTML (which is notoriously difficult to parse with regular expressions) and force the LLM to extract specific data points into a strict, validated JSON schema.

---

## 🏗️ Architecture & Design

This project avoids vector databases entirely and instead focuses on precision parsing using **Pydantic** and the `.with_structured_output()` feature of LangChain.

### 1. The Schema (`schema.py`)
At the heart of the application is a Pydantic `BaseModel` called `ProductInfo`.
- We define the exact fields we want: `product_name` (string), `price` (float), `currency` (string), and `in_stock` (boolean).
- **Descriptions are Prompts**: Notice how each field includes a `description`. In LangChain, these descriptions are not just documentation; they are actively injected into the system prompt. For example, `description="True if the item is currently in stock... False if out of stock"` explicitly teaches the LLM how to resolve ambiguity.

### 2. The Extraction Chain (`main.py`)
Instead of a simple string output parser, we construct a chain that guarantees a Python object in return.
- `structured_llm = llm.with_structured_output(ProductInfo)`
- When this chain is invoked, LangChain automatically translates the Pydantic schema into an OpenAI JSON Schema function call (or tool call).
- The LLM is forced to invoke this tool with arguments that strictly match the types we defined.

### 3. The Data (`data/`)
We include two messy HTML files:
- `product1.html`: A standard page structure.
- `product2.html`: A messy page with a discount span, a strikethrough, a bootstrap danger alert, and a disabled button.
- The beauty of LLM extraction is that no CSS selectors or XPath rules are required. The semantic understanding of the model bypasses DOM structure variations entirely.

---

## 🧠 Key Learnings & Takeaways

1. **Schema-Driven Development**: When using LLMs for data pipelines, the Pydantic schema *is* your prompt. By refining the type hints and descriptions, you exert maximum control over the output.
2. **Robustness Over Regex**: Writing an HTML parser for `product2.html` using BeautifulSoup would require edge-case handling for the `<strike>` tag, the `alert-danger` class, and the `<button disabled>` tag just to figure out stock status and price. The LLM handles all of this semantic reasoning instantly.
3. **Data Type Coercion**: Notice how `product2.html` lists the price as `₹14,500.00`. The LLM successfully strips the comma, extracts `14500.0` as a float, and maps `₹` to the `currency` field. This kind of automatic sanitization saves hundreds of lines of boilerplate parsing code.

---

## 🚀 How to Run the Project

1. Activate the environment: `source ../../venv/bin/activate`
2. Run the extraction pipeline: `python main.py`
3. Observe how it processes both HTML files and prints a perfectly clean representation of the data.
