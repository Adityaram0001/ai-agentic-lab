# LangGraph Project 1: Self-Correcting Article Writer

## 🎯 Project Goal
The goal of this project is to explore **Agentic Loops and State Management**. 

Standard LLM chains (like LCEL) are linear: Input -> Prompt -> LLM -> Output. If the LLM hallucinates or fails to follow instructions, the chain simply fails. LangGraph solves this by treating the LLM workflow as a state machine. In this project, we create a loop where an agent drafts an essay, and a separate "Critic" agent reviews it. If it fails the strict checklist, the graph routes *backwards*, forcing the writer to rewrite the essay based on the feedback.

---

## 🏗️ Architecture & Design

### 1. The Shared State (`state.py`)
In LangGraph, all nodes communicate by reading from and writing to a shared `State` object. We defined `WriterState` using a Python `TypedDict`. It holds the `topic`, the current `draft`, the `critique`, and an `iteration_count`. 

### 2. The Nodes (`nodes.py`)
Nodes are standard Python functions that take the `State` as input, do some work, and return a dictionary of updates to that state.
- **`writer_node`**: Invokes the LLM to write a draft. Crucially, if a `critique` exists in the state, it appends that critique to its prompt, effectively learning from its past mistakes.
- **`critic_node`**: Invokes the LLM to act as a strict grader. It checks if the draft is <300 words and has 3 facts. It returns either 'PASSED' or a detailed failure explanation.

### 3. The Graph & Conditional Edges (`main.py`)
The `StateGraph` is compiled by defining edges (how state flows).
- We have a normal edge: `Writer -> Critic`
- We have a **Conditional Edge**: A router function evaluates the state after the `Critic` node. If the critique says "PASSED" or we hit a max loop count (to prevent infinite API loops), it routes to `END`. Otherwise, it routes back to `Writer`.

---

## 🚀 How to Run the Project

1. Activate the environment: `source ../../venv/bin/activate`
2. Run the graph: `python main.py`
3. Observe the terminal. You will see the Writer draft an essay, the Critic review it, and potentially loop back if the essay was too long or lacked facts.
