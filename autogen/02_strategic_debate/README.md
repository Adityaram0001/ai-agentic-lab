# AutoGen Project 2: Interactive Strategic Debate Room

## 🎯 Project Goal
The goal of this project is to explore **Dynamic Group Chats and Speaker Selection**.

Instead of a strict sequential pipeline (like CrewAI) or a hardcoded graph loop (like LangGraph), AutoGen allows you to drop agents into a shared chatroom. A Manager agent reads the conversation history and dynamically decides who should speak next based on the context of the debate.

---

## 🏗️ Architecture & Design

### 1. The Debate Panel (`AssistantAgents`)
We created three highly opinionated agents:
- **Product Manager**: Optimistic about decentralized blockchain storage.
- **CFO**: Skeptical about costs and ROI.
- **Security Specialist**: Paranoid about decentralized vulnerabilities.

### 2. The Chat Manager (`GroupChatManager`)
The `GroupChat` object defines the participants and limits the conversation to `max_round=6` to prevent infinite API billing loops. 
The `GroupChatManager` is the orchestrator. When the CEO (UserProxyAgent) drops the initial prompt into the chat, the Manager invokes the LLM under the hood to decide: *"Based on what was just said, who is the most logical person to reply?"*

If the PM pitches the blockchain, the Manager will likely select the Security Specialist to attack the vulnerabilities, followed by the CFO to attack the cost. 

---

## 🚀 Key Takeaways
AutoGen's group chat dynamic is unparalleled for brainstorming, red-teaming, and simulating board meetings. By combining specialized personas, you can stress-test business strategies autonomously before ever presenting them to a real team.
