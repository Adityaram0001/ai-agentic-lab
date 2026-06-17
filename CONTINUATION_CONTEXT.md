# Continuation Context

This file serves as a persistent anchor for the `ai-agentic-lab` project. If a chat hits its context limits or needs to be restarted, point the new agent to this file to instantly resume progress.

## Global Context
- **Goal:** Learn agentic AI libraries (LangChain, LangGraph, CrewAI, AutoGen) through 8 optimized, hands-on projects.
- **LLM Configuration:** Azure Foundry `gpt-5-nano` deployment. Credentials are stored safely in `.env`.
- **Dynamic Effort:** The LLM client setup (`shared/llm_config.py`) takes a `reasoning_effort` parameter so each task can be optimized for speed.

## Current Progress Tracker

- [x] Initial Architecture & Directory Setup
- [x] Global Configuration (`.env`, `.gitignore`, `CONTINUATION_CONTEXT.md`)
- [ ] Shared Logic (`shared/llm_config.py`, `shared/utils.py`)
- [ ] Base Files (READMEs and `main.py` placeholders for all 8 projects)

### Projects Status:
- **LangChain 01: Semantic Local Search & QA** [Not Started]
- **LangChain 02: Structured E-Commerce Competitor Monitor** [Not Started]
- **LangGraph 01: Self-Correcting Article Writer** [Not Started]
- **LangGraph 02: Interrupt-Driven Customer Support Bot** [Not Started]
- **CrewAI 01: Automated Market Research & Report Team** [Not Started]
- **CrewAI 02: Social Media Content Multi-Format Factory** [Not Started]
- **AutoGen 01: Autonomous Software Engineer & Tester** [Not Started]
- **AutoGen 02: Interactive Strategic Debate Room** [Not Started]

## Next Step upon resumption
If picking up from here, check the "Current Progress Tracker" and continue with the first unchecked item.
