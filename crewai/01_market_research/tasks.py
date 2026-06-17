from crewai import Task
from agents import trend_researcher, data_analyst, technical_writer

research_task = Task(
    description="Research and summarize the top 3 emerging AI trends specifically for the year 2026. Focus on agentic workflows, quantum AI, and edge computing.",
    expected_output="A 3-paragraph summary of the top 3 trends.",
    agent=trend_researcher
)

analysis_task = Task(
    description="Take the research provided and outline exactly 2 business impacts (e.g., cost savings, new revenue streams) for EACH of the 3 trends.",
    expected_output="A list of the 3 trends, each with 2 bullet points detailing business impacts.",
    agent=data_analyst
)

writing_task = Task(
    description="Take the analyzed data and format it into a professional markdown report. It must include an 'Executive Summary' header, followed by the trends and their business impacts properly formatted with markdown.",
    expected_output="A clean, professional markdown document.",
    agent=technical_writer
)
