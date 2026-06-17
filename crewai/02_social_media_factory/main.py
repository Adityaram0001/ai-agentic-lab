"""
CrewAI 02: Social Media Factory
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from crewai import Crew, Process
from agents import script_writer, thread_specialist, qa_reviewer
from tasks import get_tasks
from shared.utils import setup_logger

logger = setup_logger(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "raw_post.md")

def main():
    logger.info("Initializing Social Media Factory Crew...")
    
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw_content = f.read()
        
    tasks = get_tasks(raw_content)
    
    # We use a sequential process. The QA task explicitly requires the context of the first two tasks.
    factory_crew = Crew(
        agents=[script_writer, thread_specialist, qa_reviewer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    print("\n" + "="*50)
    print("CrewAI Kickoff: Content Factory")
    print("="*50 + "\n")
    
    result = factory_crew.kickoff()
    
    print("\n" + "="*50)
    print("FINAL QA-APPROVED CONTENT")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()
