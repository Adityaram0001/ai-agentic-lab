import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm_config import get_langchain_llm
from crewai import Agent

# CrewAI uses Langchain LLMs natively
llm = get_langchain_llm(reasoning_effort="low")

trend_researcher = Agent(
    role="Senior Tech Trend Researcher",
    goal="Identify the top 3 emerging AI trends for 2026.",
    backstory="You are a veteran technology analyst who has successfully predicted major shifts in AI. You look past the hype to find what is actually being built in labs.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

data_analyst = Agent(
    role="Business Data Analyst",
    goal="Filter technical trends into actionable business impacts.",
    backstory="You are a pragmatic MBA graduate who analyzes technical reports and extracts exactly how they will affect enterprise revenue and operational costs.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

technical_writer = Agent(
    role="Executive Technical Writer",
    goal="Format analysis into a beautiful, easy-to-read markdown report.",
    backstory="You are an editor at Harvard Business Review. You excel at taking raw data and formatting it with clear headings, bullet points, and executive summaries.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
