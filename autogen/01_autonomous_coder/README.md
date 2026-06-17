# AutoGen Project 1: Autonomous Software Engineer

## 🎯 Project Goal
The goal of this project is to explore **Autonomous Code Execution**.

While LangChain and CrewAI are great at writing text, AutoGen excels at writing and executing code. In this project, an AssistantAgent writes Python code, and a UserProxyAgent (acting as a secure local terminal) runs that code and replies with the terminal output. If the code fails, the AssistantAgent reads the traceback and fixes its own code!

---

## 🏗️ Architecture & Design

### 1. The Coder (`AssistantAgent`)
This agent is injected with our Azure LLM configuration. Its system prompt instructs it to write python code and reply with `TERMINATE` only when the code successfully accomplishes the task.

### 2. The Executor (`UserProxyAgent`)
This agent acts as a proxy for you, the human. 
- `human_input_mode="NEVER"` ensures it runs entirely autonomously.
- `code_execution_config={"use_docker": False, "work_dir": workspace_dir}` tells AutoGen to execute any python blocks it receives directly in the `workspace/` directory, rather than requiring a Docker container.

### 3. The Task
We ask the coder to calculate the Fibonacci sequence, save it to a CSV, and plot a graph. Because the executor runs the code locally, these files will actually appear on your hard drive in the `workspace/` folder!

---

## ⚠️ Python Version Note
*Note: This script uses the classic AutoGen `0.2.x` API, which is standard across most industry tutorials. Because Python 3.13 recently dropped support for some older AutoGen dependencies, running this exact script locally requires you to run it within a Python 3.11 or 3.12 virtual environment.*
