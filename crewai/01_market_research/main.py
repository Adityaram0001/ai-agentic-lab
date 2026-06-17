"""
CrewAI 01: Automated Market Research
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from crewai import Crew, Process
from agents import trend_researcher, data_analyst, technical_writer
from tasks import research_task, analysis_task, writing_task
from shared.utils import setup_logger

logger = setup_logger(__name__)

def main():
    logger.info("Assembling the Market Research Crew...")
    
    # Instantiate your crew with a sequential process
    research_crew = Crew(
        agents=[trend_researcher, data_analyst, technical_writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.sequential,
        verbose=True
    )
    
    print("\n" + "="*50)
    print("CrewAI Kickoff: Market Research Workflow")
    print("="*50 + "\n")
    
    # Get your crew to work!
    # In a sequential process, the output of Task 1 is automatically passed as context to Task 2, etc.
    result = research_crew.kickoff()
    
    print("\n" + "="*50)
    print("FINAL EXECUTIVE REPORT")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()
