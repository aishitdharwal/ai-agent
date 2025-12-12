"""
Stateful Research Agent - Production-grade approach using LangGraph

This version demonstrates proper state management:
- Clear state definition and tracking
- Step-by-step workflow visibility
- Error handling and recovery
- Debuggable and maintainable

This is the RIGHT way to build production agents.
"""

from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import operator
import os
import json

# Load environment variables
load_dotenv()

# Define the state that will be passed between nodes
class ResearchState(TypedDict):
    """
    State definition for our research agent.
    
    This is the KEY difference from the naive approach - we explicitly
    define what information needs to be tracked throughout the workflow.
    """
    topic: str                                          # Research topic
    search_queries: List[str]                          # Queries to search for
    search_results: Annotated[List[dict], operator.add]  # Accumulated search results
    key_findings: List[str]                            # Extracted findings
    summary: str                                       # Final summary
    current_step: str                                  # Track which step we're on
    error: str                                         # Track any errors


class StatefulResearchAgent:
    """A production-grade research agent with proper state management"""
    
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
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow.
        
        The graph defines:
        1. What nodes (steps) exist
        2. How data flows between them
        3. What state is maintained
        """
        # Create workflow
        workflow = StateGraph(ResearchState)
        
        # Add nodes (each represents a step in research)
        workflow.add_node("generate_queries", self._generate_queries)
        workflow.add_node("search_web", self._search_web)
        workflow.add_node("extract_findings", self._extract_findings)
        workflow.add_node("generate_summary", self._generate_summary)
        
        # Define the flow
        workflow.set_entry_point("generate_queries")
        workflow.add_edge("generate_queries", "search_web")
        workflow.add_edge("search_web", "extract_findings")
        workflow.add_edge("extract_findings", "generate_summary")
        workflow.add_edge("generate_summary", END)
        
        return workflow.compile()
    
    def _generate_queries(self, state: ResearchState) -> ResearchState:
        """
        Step 1: Generate search queries based on the topic
        
        This demonstrates state tracking - we update current_step
        and add our queries to the state.
        """
        print("\n📝 Step 1: Generating search queries...")
        
        messages = [
            SystemMessage(content="""You are a research assistant. Given a topic, 
generate 2-3 specific search queries that would help research this topic thoroughly.
Return ONLY a JSON array of strings, nothing else."""),
            HumanMessage(content=f"Topic: {state['topic']}")
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse the queries
        try:
            queries = json.loads(response.content)
        except:
            queries = [state['topic']]  # Fallback to simple query
        
        print(f"   Generated queries: {queries}")
        
        return {
            **state,
            "search_queries": queries,
            "current_step": "generate_queries"
        }
    
    def _search_web(self, state: ResearchState) -> ResearchState:
        """
        Step 2: Execute searches for each query
        
        Notice how we can access previous state (search_queries)
        and update state with new information (search_results)
        """
        print("\n🔍 Step 2: Searching the web...")
        
        all_results = []
        
        for query in state['search_queries']:
            print(f"   Searching: {query}")
            try:
                results = self.search_tool.invoke(query)
                all_results.extend(results)
            except Exception as e:
                print(f"   ⚠️  Search failed for '{query}': {e}")
        
        print(f"   Found {len(all_results)} total results")
        
        return {
            **state,
            "search_results": all_results,
            "current_step": "search_web"
        }
    
    def _extract_findings(self, state: ResearchState) -> ResearchState:
        """
        Step 3: Extract key findings from search results
        
        This shows how we can process accumulated state
        (all the search results) and transform it.
        """
        print("\n📊 Step 3: Extracting key findings...")
        
        # Prepare search results for LLM
        results_text = "\n\n".join([
            f"Source {i+1}: {result.get('content', 'No content')}"
            for i, result in enumerate(state['search_results'])
        ])
        
        messages = [
            SystemMessage(content="""You are a research analyst. Given search results,
extract 5-7 key findings. Each finding should be a clear, concise statement.
Return ONLY a JSON array of strings, nothing else."""),
            HumanMessage(content=f"Topic: {state['topic']}\n\nSearch Results:\n{results_text}")
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse findings
        try:
            findings = json.loads(response.content)
        except:
            findings = ["Unable to extract findings from search results"]
        
        print(f"   Extracted {len(findings)} key findings")
        
        return {
            **state,
            "key_findings": findings,
            "current_step": "extract_findings"
        }
    
    def _generate_summary(self, state: ResearchState) -> ResearchState:
        """
        Step 4: Generate final summary from findings
        
        Final step where we synthesize everything into
        a coherent summary. Notice we have access to
        the complete state history.
        """
        print("\n📝 Step 4: Generating summary...")
        
        findings_text = "\n".join([
            f"{i+1}. {finding}"
            for i, finding in enumerate(state['key_findings'])
        ])
        
        messages = [
            SystemMessage(content="""You are a research writer. Create a comprehensive,
well-structured summary based on the key findings provided. The summary should be
clear, informative, and properly organized."""),
            HumanMessage(content=f"""Topic: {state['topic']}

Key Findings:
{findings_text}

Generate a comprehensive summary based on these findings.""")
        ]
        
        response = self.llm.invoke(messages)
        
        print("   ✅ Summary generated")
        
        return {
            **state,
            "summary": response.content,
            "current_step": "generate_summary"
        }
    
    def research(self, topic: str) -> dict:
        """
        Execute the research workflow
        
        This is the public interface. Notice how clean it is -
        all the complexity is handled by the graph and state management.
        """
        print("\n" + "="*50)
        print("🎯 STATEFUL AGENT: Starting research workflow...")
        print("="*50)
        
        # Initialize state
        initial_state = {
            "topic": topic,
            "search_queries": [],
            "search_results": [],
            "key_findings": [],
            "summary": "",
            "current_step": "init",
            "error": ""
        }
        
        # Run the graph
        # print(self.graph.get_graph().draw_ascii())
        final_state = self.graph.invoke(initial_state)
        
        return {
            "topic": final_state["topic"],
            "search_queries": final_state["search_queries"],
            "num_results": len(final_state["search_results"]),
            "key_findings": final_state["key_findings"],
            "summary": final_state["summary"],
            "method": "stateful_langgraph"
        }


def main():
    """Test the stateful agent"""
    agent = StatefulResearchAgent()
    
    # Test research
    topic = "Latest developments in quantum computing"
    result = agent.research(topic)
    
    print("\n" + "="*50)
    print("📊 RESEARCH RESULTS")
    print("="*50)
    print(f"\n📌 Topic: {result['topic']}")
    print(f"\n🔍 Search Queries Used:")
    for i, query in enumerate(result['search_queries'], 1):
        print(f"   {i}. {query}")
    print(f"\n📈 Results Analyzed: {result['num_results']}")
    print(f"\n🎯 Key Findings:")
    for i, finding in enumerate(result['key_findings'], 1):
        print(f"   {i}. {finding}")
    print(f"\n📝 Summary:\n{result['summary']}")
    
    print("\n" + "="*50)
    print("✅ ADVANTAGES OF THIS APPROACH:")
    print("="*50)
    print("""
1. ✅ Clear state tracking - we know exactly what step we're on
2. ✅ Progress visibility - we can see intermediate results
3. ✅ Error recovery - we can retry failed steps without starting over
4. ✅ Resumable - we could save state and continue later
5. ✅ Easy to debug - we can inspect state at any point
6. ✅ Testable - each step can be tested independently
7. ✅ Maintainable - adding new steps is straightforward
    """)

if __name__ == "__main__":
    main()
