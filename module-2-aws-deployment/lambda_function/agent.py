"""
Research Agent - Adapted from Module 1 for Lambda deployment

This is a simplified version of the stateful agent from Module 1,
optimized for Lambda execution.

Key differences from Module 1:
1. Removed verbose printing (use CloudWatch logs instead)
2. Optimized for cold start performance
3. Error handling for Lambda timeouts
4. Simplified output format for API responses
"""

from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
import operator
import os
import json


class ResearchState(TypedDict):
    """State definition for research workflow"""
    topic: str
    search_queries: List[str]
    search_results: Annotated[List[dict], operator.add]
    key_findings: List[str]
    summary: str
    current_step: str
    error: str


class ResearchAgent:
    """Production-ready research agent for Lambda deployment"""
    
    def __init__(self):
        """
        Initialize the agent
        
        IMPORTANT: This runs on every cold start.
        Keep initialization lightweight to minimize cold start time.
        """
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        
        # Initialize search tool
        self.search_tool = TavilySearchResults(
            max_results=3,
            api_key=os.environ.get("TAVILY_API_KEY")
        )
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("generate_queries", self._generate_queries)
        workflow.add_node("search_web", self._search_web)
        workflow.add_node("extract_findings", self._extract_findings)
        workflow.add_node("generate_summary", self._generate_summary)
        
        # Define flow
        workflow.set_entry_point("generate_queries")
        workflow.add_edge("generate_queries", "search_web")
        workflow.add_edge("search_web", "extract_findings")
        workflow.add_edge("extract_findings", "generate_summary")
        workflow.add_edge("generate_summary", END)
        
        return workflow.compile()
    
    def _generate_queries(self, state: ResearchState) -> ResearchState:
        """Generate search queries based on topic"""
        print(f"[generate_queries] Topic: {state['topic']}")
        
        messages = [
            SystemMessage(content="""Generate 2-3 specific search queries for researching this topic.

IMPORTANT: Return ONLY a valid JSON array of strings. Example:
["query 1", "query 2", "query 3"]

Do not include any other text, markdown, or formatting."""),
            HumanMessage(content=f"Topic: {state['topic']}")
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            # Clean the response
            content = response.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith('```'):
                content = content.split('\n', 1)[1]
                content = content.rsplit('\n', 1)[0]
                content = content.strip()
            
            if content.startswith('json'):
                content = content[4:].strip()
            
            queries = json.loads(content)
            
            # Ensure it's a list of strings
            if not isinstance(queries, list):
                queries = [state['topic']]
            
            queries = [str(q) for q in queries]
            
        except Exception as e:
            print(f"[generate_queries] Error parsing queries: {e}")
            queries = [state['topic']]  # Fallback to simple query
        
        print(f"[generate_queries] Generated: {queries}")
        
        return {
            **state,
            "search_queries": queries,
            "current_step": "generate_queries"
        }
    
    def _search_web(self, state: ResearchState) -> ResearchState:
        """Execute web searches"""
        print(f"[search_web] Searching {len(state['search_queries'])} queries")
        
        all_results = []
        
        for query in state['search_queries']:
            try:
                results = self.search_tool.invoke(query)
                all_results.extend(results)
                print(f"[search_web] Query '{query}': {len(results)} results")
            except Exception as e:
                print(f"[search_web] Error for '{query}': {str(e)}")
        
        return {
            **state,
            "search_results": all_results,
            "current_step": "search_web"
        }
    
    def _extract_findings(self, state: ResearchState) -> ResearchState:
        """Extract key findings from search results"""
        print(f"[extract_findings] Processing {len(state['search_results'])} results")
        
        # Check if we have search results
        if not state['search_results']:
            print(f"[extract_findings] No search results to process")
            return {
                **state,
                "key_findings": ["No search results found"],
                "current_step": "extract_findings"
            }
        
        results_text = "\n\n".join([
            f"Source {i+1}: {result.get('content', 'No content')}"
            for i, result in enumerate(state['search_results'])
        ])
        
        messages = [
            SystemMessage(content="""You are a research analyst. Extract 5-7 key findings from the search results.
            
IMPORTANT: Return ONLY a valid JSON array of strings. Example:
["Finding 1", "Finding 2", "Finding 3"]

Do not include any other text, markdown, or formatting."""),
            HumanMessage(content=f"Topic: {state['topic']}\n\nSearch Results:\n{results_text}")
        ]
        
        response = self.llm.invoke(messages)
        
        # More robust JSON parsing
        try:
            # Try to extract JSON from response (in case LLM adds backticks)
            content = response.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith('```'):
                content = content.split('\n', 1)[1]  # Remove first line
                content = content.rsplit('\n', 1)[0]  # Remove last line
                content = content.strip()
            
            # Remove 'json' language identifier if present
            if content.startswith('json'):
                content = content[4:].strip()
            
            findings = json.loads(content)
            
            # Ensure it's actually a list
            if not isinstance(findings, list):
                print(f"[extract_findings] Response was not a list: {type(findings)}")
                findings = [str(findings)]
            
            # Ensure all items are strings
            findings = [str(f) for f in findings]
            
            print(f"[extract_findings] Successfully extracted {len(findings)} findings")
            
        except json.JSONDecodeError as e:
            print(f"[extract_findings] JSON parse error: {e}")
            print(f"[extract_findings] Response was: {response.content[:200]}...")
            
            # Fallback: try to extract meaningful text
            findings = [
                "Analysis: " + response.content[:500] if response.content else "Unable to extract findings from search results"
            ]
        except Exception as e:
            print(f"[extract_findings] Unexpected error: {e}")
            findings = ["Error processing search results"]
        
        return {
            **state,
            "key_findings": findings,
            "current_step": "extract_findings"
        }
    
    def _generate_summary(self, state: ResearchState) -> ResearchState:
        """Generate final summary"""
        print(f"[generate_summary] Summarizing {len(state['key_findings'])} findings")
        
        findings_text = "\n".join([
            f"{i+1}. {finding}"
            for i, finding in enumerate(state['key_findings'])
        ])
        
        messages = [
            SystemMessage(content="""Create a comprehensive summary based on these findings.
Be clear, informative, and well-structured."""),
            HumanMessage(content=f"""Topic: {state['topic']}

Key Findings:
{findings_text}

Generate summary:""")
        ]
        
        response = self.llm.invoke(messages)
        
        print(f"[generate_summary] Summary generated ({len(response.content)} chars)")
        
        return {
            **state,
            "summary": response.content,
            "current_step": "generate_summary"
        }
    
    def research(self, topic: str) -> dict:
        """
        Execute research workflow
        
        Returns a clean dictionary suitable for JSON API responses
        """
        print(f"[research] Starting for topic: {topic}")
        
        initial_state = {
            "topic": topic,
            "search_queries": [],
            "search_results": [],
            "key_findings": [],
            "summary": "",
            "current_step": "init",
            "error": ""
        }
        
        final_state = self.graph.invoke(initial_state)
        
        # Return clean output for API
        return {
            "topic": final_state["topic"],
            "search_queries": final_state["search_queries"],
            "num_results": len(final_state["search_results"]),
            "key_findings": final_state["key_findings"],
            "summary": final_state["summary"]
        }
