"""
Naive Research Agent - Demonstrates the problems with stateless agents

This version works for simple cases but has critical flaws:
- No proper state management
- Loses context between steps
- Difficult to debug
- Can produce inconsistent results

This is intentionally simplistic to show what NOT to do.
"""

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class NaiveResearchAgent:
    """A simple agent without proper state management"""
    
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize search tool
        self.search_tool = TavilySearchResults(
            max_results=3,
            api_key=os.getenv("TAVILY_API_KEY")
        )
        
        # Create a simple prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research assistant. Your job is to:
1. Search for information about the given topic
2. Extract key findings from search results
3. Generate a comprehensive summary

Be thorough and cite your sources."""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        # Create agent
        self.agent = create_tool_calling_agent(
            self.llm, 
            [self.search_tool], 
            self.prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=[self.search_tool],
            verbose=True,
            handle_parsing_errors=True
        )
    
    def research(self, topic: str) -> dict:
        """
        Conduct research on a topic
        
        Problems with this approach:
        - No way to track research progress
        - Can't persist findings between runs
        - No clear separation of research steps
        - Difficult to debug what went wrong
        """
        print("\n" + "="*50)
        print("🔍 NAIVE AGENT: Starting research...")
        print("="*50 + "\n")
        
        result = self.agent_executor.invoke({
            "input": f"Research the following topic and provide a comprehensive summary with key findings: {topic}"
        })
        
        return {
            "topic": topic,
            "output": result["output"],
            "method": "naive_stateless"
        }

def main():
    """Test the naive agent"""
    agent = NaiveResearchAgent()
    
    # Test research
    topic = "Latest developments in quantum computing"
    result = agent.research(topic)
    
    print("\n" + "="*50)
    print("📊 RESEARCH RESULTS")
    print("="*50)
    print(f"\nTopic: {result['topic']}")
    print(f"\nSummary:\n{result['output']}")
    print("\n" + "="*50)
    print("⚠️  PROBLEMS WITH THIS APPROACH:")
    print("="*50)
    print("""
1. No state tracking - we don't know what step the agent is on
2. No progress visibility - can't see intermediate results
3. No error recovery - if it fails midway, we start over
4. No way to resume - each run starts from scratch
5. Difficult to debug - can't inspect state between steps
    """)

if __name__ == "__main__":
    main()
