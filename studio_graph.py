"""
LangGraph Studio Configuration File

This file creates a standalone graph that can be loaded and tested in LangGraph Studio.
LangGraph Studio is a visual debugging tool that lets you:
- See the graph structure visually
- Step through agent execution
- Inspect state at each node
- Test without building a UI

To use in LangGraph Studio:
1. Install LangGraph Studio: https://github.com/langchain-ai/langgraph-studio
2. Open this project folder in LangGraph Studio
3. The studio will automatically detect this file via langgraph.json
4. You can then interact with the graph visually

Note: You need to set GROQ_API_KEY in your .env file for this to work.
"""

# Load environment variables FIRST before any other imports
from dotenv import load_dotenv
load_dotenv()

import os
from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain.tools import Tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq

# Import configuration (after load_dotenv)
from config.settings import GROQ_MODEL_NAME, SYSTEM_PROMPT, MAX_ITERATIONS, DEFAULT_TEMPERATURE, get_api_key

# ============================================================================
# AGENT STATE DEFINITION
# ============================================================================
# This defines what data the agent tracks as it processes a question
class AgentState(TypedDict):
    """
    State that flows through the graph.

    Attributes:
        messages: List of conversation messages (user questions, AI responses, tool outputs)
                  The 'operator.add' annotation means new messages are appended to the list
        iterations: Counter to prevent infinite loops in the ReAct cycle
        video_url: The YouTube URL being analyzed (set once at the start)
        video_loaded: Boolean flag indicating if video transcript is loaded
        temperature: LLM temperature setting (0.0-1.0) for controlling randomness
    """
    messages: Annotated[List[BaseMessage], operator.add]
    iterations: int
    video_url: str
    video_loaded: bool
    temperature: float


# ============================================================================
# GLOBAL VARIABLES FOR VIDEO CONTEXT
# ============================================================================
# These store the loaded video data so the graph can access it
# In a production system, you might use a database or cache instead
_vector_store = None
_retriever = None


# ============================================================================
# HELPER FUNCTION: LOAD VIDEO
# ============================================================================
def load_video_for_studio(video_url: str):
    """
    Load a YouTube video and create a vector store for searching.
    This function is called before running the graph in LangGraph Studio.
    
    Args:
        video_url: YouTube video URL (e.g., "https://youtube.com/watch?v=...")
    
    Returns:
        bool: True if successful, False otherwise
    """
    global _vector_store, _retriever
    
    try:
        # Import here to avoid circular dependencies
        from src.youtube_loader import YouTubeLoader
        from src.vector_store import VectorStore
        
        # Load YouTube transcript
        print(f"Loading video: {video_url}")
        loader = YouTubeLoader()
        docs = loader.load(video_url)
        print(f"Loaded {len(docs)} document chunks")
        
        # Create vector store for semantic search
        _vector_store = VectorStore()
        _vector_store.create(docs)
        _retriever = _vector_store.as_retriever()
        
        print("✅ Video loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading video: {e}")
        return False


# ============================================================================
# TOOL DEFINITION: SEARCH VIDEO TRANSCRIPT
# ============================================================================
def create_search_tool():
    """
    Create the search tool that the agent can use to find information in the video.
    
    The tool performs semantic search over the video transcript chunks and returns
    the most relevant passages based on the query.
    
    Returns:
        Tool: LangChain Tool object that the agent can call
    """
    def search_video_transcript(query: str) -> str:
        """
        Search the video transcript for relevant information.
        
        Args:
            query: The search query (what to look for in the video)
        
        Returns:
            str: Concatenated relevant transcript chunks
        """
        global _retriever
        
        # Check if video is loaded
        if _retriever is None:
            return "Error: No video loaded. Please load a video first using load_video_for_studio(url)"

        # Perform semantic search using invoke (not deprecated get_relevant_documents)
        docs = _retriever.invoke(query)

        # Combine results into a single string
        result = "\n\n".join([doc.page_content for doc in docs])

        return result if result else "No relevant information found in the video."
    
    # Create the Tool object that LangChain/LangGraph can use
    return Tool(
        name="search_video",
        description="Search the YouTube video transcript for relevant information. Use this to find specific content from the video.",
        func=search_video_transcript
    )


# ============================================================================
# GRAPH NODE: CALL MODEL (AGENT REASONING)
# ============================================================================
def call_model(state: AgentState) -> dict:
    """
    Agent node: The LLM reasons about the question and decides what to do.

    This is where the "Reasoning" part of ReAct happens. The agent:
    1. Looks at the conversation history
    2. Decides if it needs to search the video
    3. Either calls a tool or provides a final answer

    Args:
        state: Current agent state with messages and metadata

    Returns:
        dict: Updated state with new message and incremented iteration count
    """
    # Get the LLM (Groq GPT-OSS model)
    api_key = get_api_key()
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Please set it in your .env file")

    # Get temperature from state, or use default
    temperature = state.get("temperature", DEFAULT_TEMPERATURE)

    # Create LLM with specified temperature
    # Temperature controls randomness: 0.0 = deterministic, 1.0 = creative
    llm = ChatGroq(model=GROQ_MODEL_NAME, temperature=temperature, api_key=api_key)

    # Bind the search tool to the LLM so it can call it
    llm_with_tools = llm.bind_tools([create_search_tool()])

    # Prepare messages: system prompt + conversation history
    messages = [HumanMessage(content=SYSTEM_PROMPT)] + state["messages"]

    # Call the LLM - it will decide whether to use tools or answer directly
    response = llm_with_tools.invoke(messages)

    # Return updated state
    return {
        "messages": [response],
        "iterations": state.get("iterations", 0) + 1
    }


# ============================================================================
# GRAPH NODE: CALL TOOL (AGENT ACTING)
# ============================================================================
# Tool node is created using ToolNode (see graph building section below)
# ToolNode automatically handles tool execution, so we don't need a custom call_tool function


# ============================================================================
# GRAPH ROUTING: SHOULD CONTINUE?
# ============================================================================
def should_continue(state: AgentState) -> str:
    """
    Routing function: Decide whether to continue the ReAct loop or end.
    
    The agent continues if:
    - The last message has tool calls (agent wants to search)
    - We haven't exceeded MAX_ITERATIONS
    
    Otherwise, we end (agent has final answer).
    
    Args:
        state: Current agent state
    
    Returns:
        str: "continue" to call tools, "end" to finish
    """
    last_message = state["messages"][-1]
    
    # Check if there are tool calls
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return "end"  # No tools to call, agent has final answer
    
    # Check iteration limit (prevent infinite loops)
    if state.get("iterations", 0) >= MAX_ITERATIONS:
        return "end"  # Too many iterations, force stop
    
    return "continue"  # Continue the ReAct loop


# ============================================================================
# BUILD THE GRAPH
# ============================================================================
def build_graph():
    """
    Build the LangGraph ReAct agent graph.
    
    Graph structure:
        START → agent → [decision] → tools → agent → ... → END
                           ↓
                          END
    
    The agent alternates between reasoning (agent node) and acting (tools node)
    until it has a final answer.
    
    Returns:
        CompiledGraph: The compiled graph ready for execution
    """
    # Create the graph with our state schema
    workflow = StateGraph(AgentState)

    # Create tool node using ToolNode (handles tool execution automatically)
    tool_node = ToolNode([create_search_tool()])

    # Add nodes
    workflow.add_node("agent", call_model)    # Reasoning node
    workflow.add_node("tools", tool_node)     # Acting node (using ToolNode)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional routing from agent
    workflow.add_conditional_edges(
        "agent",           # From the agent node
        should_continue,   # Use this function to decide
        {
            "continue": "tools",  # If continue, go to tools
            "end": END            # If end, finish
        }
    )
    
    # Add edge from tools back to agent (ReAct loop)
    workflow.add_edge("tools", "agent")
    
    # Compile the graph
    return workflow.compile()


# ============================================================================
# EXPORT THE GRAPH FOR LANGGRAPH STUDIO
# ============================================================================
# This is what LangGraph Studio will import and display
graph = build_graph()


# ============================================================================
# HELPER FUNCTION FOR TESTING
# ============================================================================
def test_graph(video_url: str, question: str, temperature: float = DEFAULT_TEMPERATURE):
    """
    Test the graph with a video and question.
    This is a helper function for testing outside of LangGraph Studio.

    Args:
        video_url: YouTube video URL
        question: Question to ask about the video
        temperature: LLM temperature (0.0-1.0). Controls randomness.

    Returns:
        str: The agent's answer
    """
    # Load the video
    if not load_video_for_studio(video_url):
        return "Failed to load video"

    # Run the graph with specified temperature
    result = graph.invoke({
        "messages": [HumanMessage(content=question)],
        "iterations": 0,
        "video_url": video_url,
        "video_loaded": True,
        "temperature": temperature
    })

    # Return the final answer
    return result["messages"][-1].content


# ============================================================================
# MAIN: FOR COMMAND LINE TESTING
# ============================================================================
if __name__ == "__main__":
    """
    Run this file directly to test the graph from command line.

    Usage:
        python studio_graph.py
    """
    # Ensure .env is loaded (redundant but safe)
    load_dotenv()

    # Set UTF-8 encoding for Windows console
    if os.name == 'nt':  # Windows
        import sys
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')

    print("🎥 YouTube Q&A Agent - LangGraph Studio Version\n")

    # Check for API key
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: GROQ_API_KEY not set")
        print("Please set it in your .env file or environment variables")
        print(f"\nDebug info:")
        print(f"  - Current directory: {os.getcwd()}")
        print(f"  - .env file exists: {os.path.exists('.env')}")
        if os.path.exists('.env'):
            print(f"  - .env file location: {os.path.abspath('.env')}")
        exit(1)

    print(f"✅ API key loaded successfully (length: {len(api_key)} chars)\n")
    
    # Get video URL
    video_url = input("Enter YouTube URL: ").strip()
    if not video_url:
        print("No URL provided")
        exit(1)
    
    # Get temperature setting
    print(f"\n🌡️  Temperature (0.0-1.0, default {DEFAULT_TEMPERATURE}):")
    print("   0.0 = Deterministic, focused")
    print("   0.7 = Balanced (recommended)")
    print("   1.0 = Creative, diverse")
    temp_input = input("Temperature (press Enter for default): ").strip()

    if temp_input:
        try:
            temperature = float(temp_input)
            if not 0.0 <= temperature <= 1.0:
                print("⚠️  Temperature must be between 0.0 and 1.0. Using default.")
                temperature = DEFAULT_TEMPERATURE
        except ValueError:
            print("⚠️  Invalid input. Using default temperature.")
            temperature = DEFAULT_TEMPERATURE
    else:
        temperature = DEFAULT_TEMPERATURE

    print(f"Using temperature: {temperature}")

    # Load video
    print("\nLoading video...")
    if not load_video_for_studio(video_url):
        exit(1)

    # Interactive Q&A loop
    print("\n✅ Ready! Ask questions (type 'quit' to exit, 'temp' to change temperature)\n")

    while True:
        question = input("Q: ").strip()

        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        # Allow changing temperature mid-session
        if question.lower() == 'temp':
            temp_input = input(f"New temperature (current: {temperature}): ").strip()
            try:
                new_temp = float(temp_input)
                if 0.0 <= new_temp <= 1.0:
                    temperature = new_temp
                    print(f"✅ Temperature updated to {temperature}")
                else:
                    print("⚠️  Temperature must be between 0.0 and 1.0")
            except ValueError:
                print("⚠️  Invalid input")
            continue

        if not question:
            continue

        try:
            # Run the graph with current temperature
            result = graph.invoke({
                "messages": [HumanMessage(content=question)],
                "iterations": 0,
                "video_url": video_url,
                "video_loaded": True,
                "temperature": temperature
            })

            # Print answer
            answer = result["messages"][-1].content
            print(f"\nA: {answer}\n")
            
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


