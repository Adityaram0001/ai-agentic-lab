import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm_config import get_langchain_llm
from crewai import Agent

llm = get_langchain_llm(reasoning_effort="low")

script_writer = Agent(
    role="YouTube Shorts Scriptwriter",
    goal="Convert dense articles into engaging, fast-paced 60-second video scripts.",
    backstory="You are a Gen-Z content creator who understands retention. You use hooks, fast pacing, and clear visuals in your scripts.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

thread_specialist = Agent(
    role="X (Twitter) Thread Specialist",
    goal="Convert articles into highly engaging 5-post threads.",
    backstory="You are a top-tier tech influencer. Your threads always start with a contrarian hook and end with a strong call to action.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

qa_reviewer = Agent(
    role="Content Quality Assurance Reviewer",
    goal="Ensure all generated content strictly adheres to the facts in the original article with zero hallucinations.",
    backstory="You are a meticulous fact-checker. You despise when content creators exaggerate or invent statistics. You will ruthlessly correct any claims not found in the source text.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
