import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.llm_config import get_langchain_llm
from state import WriterState
from langchain_core.messages import HumanMessage

def writer_node(state: WriterState):
    """Generates the essay or rewrites it based on critique."""
    llm = get_langchain_llm(reasoning_effort="low")
    
    prompt = f"Write a short essay on the topic: '{state['topic']}'. It MUST be under 300 words and contain at least 3 verifiable facts."
    if state.get("critique") and "PASSED" not in state.get("critique", ""):
        prompt += f"\n\nHere is feedback from the critic that you MUST incorporate into your rewrite: {state['critique']}"
        
    print(f"\n[Writer Node] Drafting... (Iteration {state.get('iteration_count', 0) + 1})")
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "draft": response.content,
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def critic_node(state: WriterState):
    """Reviews the draft against a strict checklist."""
    llm = get_langchain_llm(reasoning_effort="low")
    
    draft = state.get("draft")
    prompt = f"""
    Review the following draft.
    Checklist:
    1. Is it strictly under 300 words? (Count the words carefully)
    2. Does it contain at least 3 distinct factual statements?
    
    If it fails ANY criteria, provide a specific critique on what to fix and end your response with exactly the word 'FAILED'.
    If it passes ALL criteria, your entire response should just be the word 'PASSED'.
    
    Draft:
    {draft}
    """
    
    print("\n[Critic Node] Reviewing draft...")
    response = llm.invoke([HumanMessage(content=prompt)])
    
    critique = response.content
    print(f"[Critic Feedback]: {critique.strip()[:100]}...") # Print preview
    
    return {"critique": critique}
