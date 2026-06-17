"""
LangGraph 02: Interrupt-Driven Support Bot
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state import SupportState
from nodes import categorize_node, auto_refund_node, human_review_node
from shared.utils import setup_logger

logger = setup_logger(__name__)

def refund_router(state: SupportState):
    """Routes based on the refund amount."""
    if state["status"] == "IRRELEVANT":
        return "end"
        
    amount = state.get("refund_amount", 0.0)
    if amount > 60.0:
        print("\n[Router] Refund exceeds $60 threshold. Routing to Human Review.")
        return "human_review"
    else:
        print("\n[Router] Refund is within auto-approve limits. Routing to Auto Refund.")
        return "auto_refund"

def main():
    logger.info("Initializing Interrupt-Driven Support Bot Graph...")
    
    workflow = StateGraph(SupportState)
    
    workflow.add_node("categorizer", categorize_node)
    workflow.add_node("auto_refund", auto_refund_node)
    workflow.add_node("human_review", human_review_node)
    
    workflow.set_entry_point("categorizer")
    workflow.add_conditional_edges("categorizer", refund_router, {
        "auto_refund": "auto_refund",
        "human_review": "human_review",
        "end": END
    })
    
    workflow.add_edge("auto_refund", END)
    workflow.add_edge("human_review", END)
    
    # We use a MemorySaver checkpointer to persist the graph state.
    # This allows us to freeze execution, wait for user input, and resume later.
    checkpointer = MemorySaver()
    
    # Compile with the interrupt_before flag
    app = workflow.compile(
        checkpointer=checkpointer,
        interrupt_before=["human_review"]
    )
    
    thread_config = {"configurable": {"thread_id": "ticket_1"}}
    
    print("\n" + "="*50)
    print("User: I bought the UltraX Headphones but they are defective. I want a refund of $150.")
    print("="*50 + "\n")
    
    # 1. Run the graph initially
    initial_input = {"user_query": "I bought the UltraX Headphones but they are defective. I want a refund of $150."}
    
    # Use stream instead of invoke, and iterate over events to force execution up to the breakpoint
    for event in app.stream(initial_input, thread_config, stream_mode="values"):
        pass
        
    # 2. Check the state. It should be paused before the human_review node.
    snapshot = app.get_state(thread_config)
    
    if snapshot.next:
        print(f"\n[SYSTEM] Graph execution paused. Next node to run: {snapshot.next[0]}")
        
        # 3. Simulate human input (In a real app, this would pause and wait for a webhook or terminal input)
        print("\n" + "*"*50)
        print(f"A refund of ${snapshot.values.get('refund_amount')} requires approval.")
        decision = "APPROVED" # Hardcoded for demo purposes so it doesn't block automated testing
        print(f"Human Input Received: {decision}")
        print("*"*50 + "\n")
        
        # 4. Update the state based on human input and resume
        if decision.upper() == "APPROVED":
            print("[SYSTEM] Resuming execution...")
            app.update_state(thread_config, {"status": "HUMAN_APPROVED"})
            
            for event in app.stream(None, thread_config, stream_mode="values"):
                pass
                
        else:
            print("[SYSTEM] Refund rejected by human.")
            
    print("\n--- Final Ticket Status ---")
    final_snapshot = app.get_state(thread_config)
    print(final_snapshot.values)

if __name__ == "__main__":
    main()
