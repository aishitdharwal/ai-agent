# Workshop Teaching Guide: Module 1

## Overview
This module creates the foundational "aha moment" about state management. The teaching flow is designed to show participants the problem first, then provide the solution.

## Teaching Flow (45 minutes)

### Part 1: Introduction (5 minutes)

**Opening Question:**
"When you build an AI agent that needs to do multiple steps - search the web, analyze results, generate a summary - how does it remember what it learned in step 1 when it gets to step 3?"

This question frames the core problem. Most participants haven't thought deeply about state management, so this makes it concrete.

**Show the Goal:**
Briefly demo the final working agent. Show it taking a research topic and producing a structured summary. This shows them what they're building toward.

### Part 2: The Naive Approach (15 minutes)

**Live Code Walkthrough:**
1. Open `naive_agent.py`
2. Walk through the code explaining each part:
   - LLM initialization
   - Simple prompt structure
   - Agent executor setup
   - The `research()` method

**Key Teaching Point:**
"This works, but notice what's missing - there's no way to track what step we're on, no way to see intermediate results, and if something fails, we have no idea where it failed."

**Run the Agent:**
```bash
python run_agent.py --agent naive --topic "Latest AI breakthroughs"
```

**Highlight the Problems:**
As it runs, point out:
- We can't see the individual steps
- If it fails, we don't know where
- The LLM decides the entire flow - we have no control
- No way to inspect what's happening

**Ask the Group:**
"What happens if this agent needs to make 10 searches instead of 3? How do we know which searches succeeded? How do we resume if it crashes halfway?"

Let them wrestle with these questions briefly. This creates the tension that LangGraph solves.

### Part 3: Introducing LangGraph (10 minutes)

**The State Concept:**
"LangGraph solves this by making state explicit and manageable."

Open `stateful_agent.py` and walk through the `ResearchState` TypedDict:

```python
class ResearchState(TypedDict):
    topic: str
    search_queries: List[str]
    search_results: Annotated[List[dict], operator.add]
    key_findings: List[str]
    summary: str
    current_step: str
    error: str
```

**Key Teaching Point:**
"This is our state contract. Every step in our workflow reads from this state and updates it. This makes the entire process transparent and debuggable."

**The Graph Structure:**
Show the `_build_graph()` method:
```python
workflow.add_node("generate_queries", self._generate_queries)
workflow.add_node("search_web", self._search_web)
workflow.add_node("extract_findings", self._extract_findings)
workflow.add_node("generate_summary", self._generate_summary)
```

**Key Teaching Point:**
"Each node is a discrete step. Data flows through them in a defined order. We can test each step independently, add error handling at each point, and see exactly where we are in the process."

### Part 4: Walkthrough Each Node (10 minutes)

**Don't rush this part.** Walk through each node function explaining:

**Node 1 - Generate Queries:**
- Takes the topic from state
- Generates search queries
- Updates state with queries and current_step
- Returns the updated state

**Pattern Recognition:**
"Notice the pattern: read from state → process → update state → return. Every node follows this pattern."

**Node 2 - Search Web:**
- Reads search_queries from state
- Executes searches
- Accumulates results
- Updates state with results

**Teaching Point:**
"See how this node accesses what the previous node produced? That's state management in action."

**Node 3 & 4:**
Walk through extract_findings and generate_summary more quickly since they follow the same pattern.

### Part 5: Run and Compare (5 minutes)

**Run the Stateful Agent:**
```bash
python run_agent.py --agent stateful --topic "Latest AI breakthroughs"
```

**Point Out the Differences:**
- Clear step-by-step progress
- Visible intermediate results
- Structured output with all components
- Debuggable workflow

**Run Comparison:**
```bash
python run_agent.py --agent both --topic "Latest AI breakthroughs"
```

Read the comparison summary together.

## Critical Teaching Moments

### Moment 1: State as Contract
When showing `ResearchState`, emphasize:
"This TypedDict is our contract. Every node agrees on this structure. This is how we avoid the chaos of implicit state."

### Moment 2: Graph as Blueprint
When showing the graph construction:
"This graph is our workflow blueprint. We can visualize it, test it, modify it. In the naive approach, the workflow is hidden inside the LLM's decision-making."

### Moment 3: Production Reality
Before moving to Module 2:
"This works great on your laptop. But what happens when 100 users hit this simultaneously? What happens if a search takes 30 seconds? What happens when your AWS Lambda times out?"

These questions create appetite for Module 2 (deployment) and ultimately your course.

## Common Questions to Expect

**Q: "Isn't the naive approach simpler? Why add complexity?"**
A: "It is simpler - until it breaks in production. Then you're debugging a black box. The stateful approach is more code upfront but infinitely more debuggable and maintainable."

**Q: "Could I just use a database to store state between steps?"**
A: "Great question! Yes, and that's exactly what we do in production. LangGraph can integrate with databases for persistent state. We'll cover that in Module 2."

**Q: "What if I need conditional logic in my workflow?"**
A: "Excellent question. LangGraph supports conditional edges - you can route to different nodes based on state. The graph doesn't have to be linear."

**Q: "How does this compare to LangChain's agent executor?"**
A: "LangChain's agent executor is like the naive approach - the LLM controls flow. LangGraph gives YOU control over the flow while still using LLMs for decision-making within steps."

## Workshop Setup Checklist

Before the workshop, ensure:
- [ ] You have valid OpenAI and Tavily API keys
- [ ] All dependencies install cleanly
- [ ] Both agents run successfully
- [ ] You've tested with 2-3 different topics
- [ ] You can explain each line of code in both files
- [ ] You've practiced the 45-minute timing

## Connection to Module 2

End with this bridge:
"You now have a working, stateful agent. You understand why state management matters. But this is running on your laptop with your API keys. In Module 2, we're going to deploy this to AWS so real users can access it. That's when you'll see why production deployment is its own discipline - it's not just about making code work, it's about making it work reliably, securely, and scalably for real users."

## Connection to Course Upsell

The seeds you've planted:
- State persistence across user sessions (needs databases)
- Handling concurrent users (needs proper architecture)
- Monitoring and debugging in production (needs observability)
- Cost management (needs optimization strategies)
- Security and authentication (needs AWS IAM, API keys management)

Each of these is a rabbit hole. You've shown them ONE - state management within a single execution. The course teaches them all four projects worth of production patterns.
