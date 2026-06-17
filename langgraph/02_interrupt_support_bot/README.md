# LangGraph Project 2: Interrupt-Driven Customer Support Bot

## 🎯 Project Goal
The goal of this project is to explore **Human-in-the-Loop Validation** and **State Persistence**.

Fully autonomous agents are dangerous when handling sensitive actions like issuing refunds. LangGraph allows you to build agents that run autonomously until they hit a critical threshold, at which point they freeze execution, save their state to memory, and wait for human approval before proceeding.

---

## 🏗️ Architecture & Design

### 1. State and Nodes
- **`categorize_node`**: Parses a user's complaint, looking for the word "refund" and extracting the dollar amount.
- **`auto_refund_node`**: Automatically handles refunds under a safe threshold (e.g., $60).
- **`human_review_node`**: A dummy node that acts as a breakpoint.

### 2. The MemorySaver Checkpointer (`main.py`)
To freeze an agent, its state must be serialized. We attach a `MemorySaver` to the graph during compilation:
```python
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer, interrupt_before=["human_review"])
```
This tells LangGraph: "If the router decides the next node is `human_review`, pause immediately and save the state."

### 3. Execution & Resumption
We invoke the graph using `.stream()` with a specific `thread_id`. When the graph hits the breakpoint, the stream ends, but the state is preserved in the checkpointer.
The script then uses standard Python `input()` to ask you to type 'APPROVED' or 'REJECTED'.
Once approved, we use `app.update_state()` to modify the frozen state, and call `.stream(None)` to resume execution from exactly where it left off.

---

## 🚀 How to Run the Project

1. Activate the environment: `source ../../venv/bin/activate`
2. Run the graph: `python main.py`
3. The script feeds a $150 refund request into the bot. The bot categorizes it, realizes it exceeds the $60 auto-approve limit, and pauses. 
4. The terminal will explicitly simulate the human input required to resume the graph!
