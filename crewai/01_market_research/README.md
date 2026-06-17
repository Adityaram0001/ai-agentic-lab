# CrewAI Project 1: Automated Market Research & Report Team

## 🎯 Project Goal
The goal of this project is to explore **Role Assignment and Sequential Workflows** using CrewAI.

Instead of writing complex code to manage state or loop logic (like in LangGraph), CrewAI allows you to think like a manager. You define a team of "Agents" with distinct roles, assign them "Tasks," and instruct them to work sequentially. CrewAI handles the context passing automatically.

---

## 🏗️ Architecture & Design

### 1. The Agents (`agents.py`)
We created three specialized workers:
- **Trend Researcher**: A veteran tech analyst focused on emerging 2026 trends.
- **Data Analyst**: An MBA graduate focused on extracting business impact from raw tech data.
- **Technical Writer**: A Harvard Business Review editor focused on formatting markdown.

Notice the `backstory` parameter for each agent. In CrewAI, the backstory is heavily injected into the system prompt. The more detailed and specific the backstory, the better the agent adopts the persona.

### 2. The Tasks (`tasks.py`)
We defined three tasks corresponding to our three agents. Each task has a clear `description` and `expected_output`. 

### 3. The Crew (`main.py`)
We assemble the crew and set `process=Process.sequential`. 
Because it is sequential, CrewAI automatically takes the output from the `research_task` and feeds it as hidden context into the `analysis_task`. Then, it takes the output of the `analysis_task` and feeds it into the `writing_task`. 

---

## 🚀 How to Run the Project

1. Activate the environment: `source ../../venv/bin/activate`
2. Run the crew: `python main.py`
3. Watch the terminal output carefully! You will see each agent "thinking," executing their task, and handing off the baton to the next agent in line until the final executive report is printed.
