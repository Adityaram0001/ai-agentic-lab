import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from state import SupportState

def categorize_node(state: SupportState):
    """Parses the user query to find a refund request and amount."""
    query = state.get("user_query", "").lower()
    
    # Simple regex to find an amount like $50 or 50.00
    match = re.search(r'\$?(\d+(\.\d{2})?)', query)
    amount = float(match.group(1)) if match else 0.0
    
    status = "PROCESSING" if "refund" in query and amount > 0 else "IRRELEVANT"
    
    print(f"\n[Categorize Node] Extracted refund amount: ${amount}. Status: {status}")
    return {"refund_amount": amount, "status": status}

def auto_refund_node(state: SupportState):
    """Processes refunds under the threshold automatically."""
    print(f"\n[Auto Refund Node] Automatically processing refund for ${state['refund_amount']}.")
    return {"status": "REFUND_PROCESSED"}

def human_review_node(state: SupportState):
    """A breakpoint node. Reaching here means human intervention is required."""
    print("\n[Human Review Node] Reviewing large refund request...")
    # The actual human input logic will happen in the main.py execution loop
    return {"status": "PENDING_HUMAN_REVIEW"}
