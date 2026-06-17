"""
AutoGen 02: Interactive Strategic Debate Room
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import autogen
from llm_config import llm_config

def main():
    print("\n" + "="*50)
    print("AutoGen Kickoff: Strategic Debate Room")
    print("="*50 + "\n")

    # Define the Agents
    pm = autogen.AssistantAgent(
        name="Product_Manager",
        system_message="You are a highly optimistic Product Manager. You love buzzwords, innovation, and moving fast. You want to push all user data to a decentralized blockchain matrix.",
        llm_config=llm_config,
    )
    
    cfo = autogen.AssistantAgent(
        name="Chief_Financial_Officer",
        system_message="You are a skeptical CFO. You care only about costs, ROI, and risk. You think blockchain is an expensive scam and prefer cheap, traditional cloud storage.",
        llm_config=llm_config,
    )
    
    security = autogen.AssistantAgent(
        name="Security_Specialist",
        system_message="You are a paranoid Security Specialist. You see vulnerabilities everywhere. You trust no one and think decentralized systems expose data to too many external nodes.",
        llm_config=llm_config,
    )
    
    user_proxy = autogen.UserProxyAgent(
        name="CEO",
        system_message="You are the CEO. You just watch the debate and end the meeting after everyone has made their point.",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config=False,
    )

    # Create the GroupChat
    groupchat = autogen.GroupChat(
        agents=[user_proxy, pm, cfo, security],
        messages=[],
        max_round=6, # Limit the debate to 6 messages
    )
    
    # Create the Manager that orchestrates the group chat
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Kickoff the debate
    prompt = "Team, I'm proposing we move all our core enterprise user data to a decentralized blockchain matrix. Give me your raw, unfiltered thoughts."
    
    user_proxy.initiate_chat(
        manager,
        message=prompt
    )

if __name__ == "__main__":
    main()
