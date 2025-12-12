"""
CLI tool to run and compare both agent versions

Usage:
    python run_agent.py --agent naive --topic "Your research topic"
    python run_agent.py --agent stateful --topic "Your research topic"
    python run_agent.py --agent both --topic "Your research topic"
"""

import argparse
from naive_agent import NaiveResearchAgent
from stateful_agent import StatefulResearchAgent
import time


def run_naive(topic: str):
    """Run the naive agent"""
    print("\n" + "🚀 "*25)
    print("RUNNING NAIVE (STATELESS) AGENT")
    print("🚀 "*25 + "\n")
    
    start_time = time.time()
    agent = NaiveResearchAgent()
    result = agent.research(topic)
    elapsed = time.time() - start_time
    
    print(f"\n⏱️  Time taken: {elapsed:.2f} seconds")
    return result


def run_stateful(topic: str):
    """Run the stateful agent"""
    print("\n" + "🎯 "*25)
    print("RUNNING STATEFUL (LANGGRAPH) AGENT")
    print("🎯 "*25 + "\n")
    
    start_time = time.time()
    agent = StatefulResearchAgent()
    result = agent.research(topic)
    elapsed = time.time() - start_time
    
    print(f"\n⏱️  Time taken: {elapsed:.2f} seconds")
    return result


def compare_agents(topic: str):
    """Run both agents and compare results"""
    print("\n" + "="*60)
    print("COMPARING BOTH AGENT APPROACHES")
    print("="*60 + "\n")
    
    # Run naive agent
    naive_result = run_naive(topic)
    
    print("\n" + "-"*60 + "\n")
    
    # Run stateful agent
    stateful_result = run_stateful(topic)
    
    # Comparison summary
    print("\n" + "="*60)
    print("📊 COMPARISON SUMMARY")
    print("="*60 + "\n")
    
    print("NAIVE AGENT:")
    print("  ✅ Pros: Simple to implement")
    print("  ❌ Cons: No state tracking, difficult to debug, not production-ready")
    print("\nSTATEFUL AGENT:")
    print("  ✅ Pros: Clear state management, debuggable, maintainable, production-ready")
    print("  ✅ Can track progress at each step")
    print("  ✅ Easy to add error handling and recovery")
    print("  ✅ Can persist state for resume capability")
    
    print("\n" + "="*60)
    print("💡 KEY TAKEAWAY")
    print("="*60)
    print("""
For production AI agents, proper state management isn't optional - it's essential.

The stateful approach gives you:
1. Visibility into what your agent is doing
2. Ability to debug when things go wrong
3. Foundation for adding monitoring and observability
4. Path to handling errors gracefully
5. Capability to scale to complex workflows

This is just the beginning. In production, you'll also need:
- Persistent state storage (databases, not just memory)
- Handling concurrent users
- API endpoints for real users
- Monitoring and logging
- Cost optimization
- Security and authentication

These production concerns are what we cover in the full course.
""")


def main():
    parser = argparse.ArgumentParser(
        description="Run research agents and compare approaches"
    )
    parser.add_argument(
        "--agent",
        choices=["naive", "stateful", "both"],
        default="both",
        help="Which agent to run (default: both)"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Latest developments in quantum computing",
        help="Research topic"
    )
    
    args = parser.parse_args()
    
    if args.agent == "naive":
        run_naive(args.topic)
    elif args.agent == "stateful":
        run_stateful(args.topic)
    else:
        compare_agents(args.topic)


if __name__ == "__main__":
    main()
