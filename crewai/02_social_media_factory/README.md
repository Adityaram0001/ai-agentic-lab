# CrewAI Project 2: Social Media Content Multi-Format Factory

## 🎯 Project Goal
The goal of this project is to explore **Task Dependencies and Content QA** using CrewAI.

A common enterprise use case for multi-agent systems is taking a single "Source of Truth" document and fanning it out into multiple formats, then using a separate agent to verify the new formats didn't hallucinate. This project demonstrates exactly that.

---

## 🏗️ Architecture & Design

### 1. The Raw Data (`data/raw_post.md`)
We use a mock blog post about the "Future of AI Agents" as our source of truth.

### 2. The Agents (`agents.py`)
- **Script Writer**: Focuses on high-retention, fast-paced YouTube short scripts with visual cues.
- **Thread Specialist**: Focuses on engaging X/Twitter threads with hooks.
- **Quality Assurance Reviewer**: A strict fact-checker specifically instructed to cross-reference against the original text and fix hallucinations.

### 3. Task Contexts (`tasks.py`)
The most important part of this project is how the tasks are structured:
```python
qa_task = Task(
    description=...,
    agent=qa_reviewer,
    context=[youtube_task, twitter_task] 
)
```
By explicitly passing `youtube_task` and `twitter_task` into the `context` array of the `qa_task`, CrewAI knows that the QA agent MUST wait for the first two tasks to complete, and then it injects both of their outputs into the QA agent's prompt simultaneously.

---

## 🚀 How to Run the Project

1. Activate the environment: `source ../../venv/bin/activate`
2. Run the crew: `python main.py`
3. The agents will read the `raw_post.md` file. The creators will draft the content, and the QA agent will review both outputs in a final pass before printing the verified text to the terminal.
