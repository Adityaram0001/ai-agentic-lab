"""
AutoGen 01: Autonomous Software Engineer
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import autogen
from llm_config import llm_config

# Ensure workspace exists
workspace_dir = os.path.join(os.path.dirname(__file__), "workspace")
os.makedirs(workspace_dir, exist_ok=True)

def main():
    print("\n" + "="*50)
    print("AutoGen Kickoff: Autonomous Software Engineer")
    print("="*50 + "\n")

    # The AssistantAgent acts as the Coder. It generates python code.
    coder = autogen.AssistantAgent(
        name="software_engineer",
        llm_config=llm_config,
        system_message="You are a senior python engineer. You write python code to solve tasks. Ensure the code is self-contained and ready to execute. If you get an error back, rewrite the code to fix it. Reply TERMINATE when the task is fully resolved."
    )

    # The UserProxyAgent acts as the Executor. It runs the code locally.
    executor = autogen.UserProxyAgent(
        name="local_executor",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": workspace_dir,
            "use_docker": False, # Executing locally instead of Docker
        }
    )

    # Start the conversation
    task = "Write a Python script that calculates the Fibonacci sequence up to 20 digits, saves it to 'fibonacci.csv' in the current directory, and plots a graph of the sequence saving it as 'fibonacci.png'. Do not show the plot, just save it."
    
    executor.initiate_chat(
        coder,
        message=task
    )

if __name__ == "__main__":
    main()
