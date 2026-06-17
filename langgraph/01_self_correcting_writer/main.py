"""
LangGraph 01: Self-Correcting Article Writer
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from langgraph.graph import StateGraph, END
from state import WriterState
from nodes import writer_node, critic_node
from shared.utils import setup_logger

logger = setup_logger(__name__)

def router(state: WriterState):
    """
    Conditional edge router. 
    Routes to END if critic says PASSED or max iterations reached.
    Otherwise routes back to writer.
    """
    critique = state.get("critique", "")
    iteration_count = state.get("iteration_count", 0)
    
    if "PASSED" in critique:
        print("\n[Router] Critic approved! Moving to Publisher (END).")
        return "end"
    
    if iteration_count >= 3:
        print("\n[Router] Max iterations reached (3). Forcing publish.")
        return "end"
        
    print("\n[Router] Critic rejected draft. Routing back to Writer.")
    return "writer"

def main():
    logger.info("Initializing Self-Correcting Writer Graph...")
    
    # Initialize the graph with our TypedDict State
    workflow = StateGraph(WriterState)
    
    # Add our nodes
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)
    
    # Define the execution flow
    workflow.set_entry_point("writer")
    workflow.add_edge("writer", "critic")
    
    # Conditional edge decides where to go after the critic
    workflow.add_conditional_edges(
        "critic",
        router,
        {
            "writer": "writer", # Loop back to writer
            "end": END          # Exit the graph
        }
    )
    
    # Compile the graph into a runnable LangChain object
    app = workflow.compile()
    
    print("\n" + "="*50)
    print("LangGraph Self-Correcting Writer")
    print("="*50 + "\n")
    
    topic = "The invention and impact of the electric telegraph"
    print(f"Topic: {topic}\n")
    
    # Invoke the graph with the initial state
    final_state = app.invoke({"topic": topic, "iteration_count": 0})
    
    print("\n" + "="*50)
    print("FINAL PUBLISHED DRAFT")
    print("="*50)
    print(final_state["draft"])
    print(f"\nTotal Writer Iterations: {final_state['iteration_count']}")

if __name__ == "__main__":
    main()
