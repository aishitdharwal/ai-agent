# Module 1: Building Your First Stateful AI Agent

## Overview
This module teaches you how to build a Research Assistant Agent that demonstrates the critical difference between stateless and stateful AI agents. You'll see firsthand why state management is essential for production AI systems.

## What You'll Build
A Research Assistant Agent that:
- Takes a research topic as input
- Searches the web for relevant information
- Extracts and organizes key findings
- Generates a comprehensive summary report
- **Maintains state** throughout the multi-step research process

## The Learning Journey

### Part 1: The Naive Approach (Stateless)
You'll first build a simple agent without proper state management. This agent will work but will have critical flaws:
- Cannot track research progress
- May lose context between steps
- Produces inconsistent results
- Difficult to debug when things go wrong

### Part 2: The Production Approach (Stateful with LangGraph)
Then you'll rebuild the same agent using LangGraph with proper state management:
- Tracks research progress through each step
- Maintains context across the entire workflow
- Produces reliable, consistent outputs
- Easy to debug and monitor

## Setup Instructions

1. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure API keys:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. **Get your API keys:**
- OpenAI API: https://platform.openai.com/api-keys
- Tavily API (for web search): https://tavily.com/

## Files Structure

```
module-1-stateful-agent/
├── naive_agent.py          # Stateless version (shows the problems)
├── stateful_agent.py       # LangGraph version (shows the solution)
├── run_agent.py            # Simple CLI to test both agents
└── README.md               # This file
```

## Running the Agents

### Test the Naive Agent:
```bash
python run_agent.py --agent naive --topic "Latest developments in quantum computing"
```

### Test the Stateful Agent:
```bash
python run_agent.py --agent stateful --topic "Latest developments in quantum computing"
```

## Key Concepts You'll Learn

1. **State Management**: How to maintain context across multi-step workflows
2. **LangGraph Architecture**: Using nodes, edges, and state to build reliable agents
3. **Tool Integration**: Connecting external tools (web search) to your agent
4. **Error Handling**: Building agents that gracefully handle failures
5. **Debugging**: Understanding what's happening at each step

## What's Next?

After completing this module, you'll understand:
- ✅ Why state management is critical for production agents
- ✅ How to build multi-step agents with LangGraph
- ✅ How to integrate external tools into your agent workflow

But you'll also realize there are production concerns we haven't addressed:
- ❓ How do I deploy this to handle real user requests?
- ❓ What happens when multiple users access this simultaneously?
- ❓ How do I persist state between user sessions?
- ❓ How do I monitor and debug this in production?

These questions lead us to **Module 2: AWS Deployment** where we'll deploy this agent to the cloud.

## Notes

1. Show the naive agent working for simple cases
2. Demonstrate where it breaks (losing context, inconsistent results)
3. Introduce LangGraph as the solution
4. Show the same agent working reliably with proper state
5. Connect this to broader production engineering principles
