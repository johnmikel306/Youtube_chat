from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain.tools import Tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from config.settings import SYSTEM_PROMPT, MAX_ITERATIONS

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    iterations: int

class Agent:
    def __init__(self, llm, retriever):
        self.tool = self._create_tool(retriever)
        # Bind tools to LLM - this enables tool calling
        self.llm = llm.bind_tools([self.tool])
        # Also create a version that forces tool use on first call
        self.llm_force_tool = llm.bind_tools([self.tool], tool_choice="search_video")
        self.llm_base = llm
        self.graph = self._build_graph()

    def _create_tool(self, retriever):
        def search(query: str) -> str:
            """Search the YouTube video transcript for relevant information.

            This tool retrieves relevant excerpts from the video transcript based on the query.
            ALWAYS use this tool before answering questions about the video.

            Args:
                query: The question or topic to search for in the video transcript

            Returns:
                Relevant transcript excerpts that contain information about the query
            """
            # Use invoke instead of deprecated get_relevant_documents
            docs = retriever.invoke(query)
            if not docs:
                return "No relevant information found in the video transcript."
            return "\n\n".join([d.page_content for d in docs])

        return Tool(
            name="search_video",
            description=(
                "REQUIRED TOOL: Search the YouTube video transcript to find relevant information. "
                "You MUST use this tool for EVERY question about the video content. "
                "Input should be the user's question or key topics to search for. "
                "Returns relevant excerpts from the video transcript."
            ),
            func=search
        )

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        def call_model(state):
            messages = [HumanMessage(content=SYSTEM_PROMPT)] + state["messages"]

            # Force tool use on first iteration to ensure we always search the video
            iterations = state.get("iterations", 0)
            if iterations == 0:
                # First call - force the agent to use the search_video tool
                response = self.llm_force_tool.invoke(messages)
            else:
                # Subsequent calls - let agent decide
                response = self.llm.invoke(messages)

            return {
                "messages": [response],
                "iterations": iterations + 1
            }

        def should_continue(state):
            last_msg = state["messages"][-1]
            if not hasattr(last_msg, "tool_calls") or not last_msg.tool_calls:
                return "end"
            if state.get("iterations", 0) >= MAX_ITERATIONS:
                return "end"
            return "continue"

        # Use ToolNode for automatic tool execution
        tool_node = ToolNode([self.tool])

        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", should_continue, {
            "continue": "tools",
            "end": END
        })
        workflow.add_edge("tools", "agent")

        return workflow.compile()

    def run(self, question: str) -> str:
        result = self.graph.invoke({
            "messages": [HumanMessage(content=question)],
            "iterations": 0
        })
        return result["messages"][-1].content

    def stream(self, question: str):
        # Stream the graph execution
        for event in self.graph.stream({
            "messages": [HumanMessage(content=question)],
            "iterations": 0
        }):
            # Yield final answer when agent finishes
            if "agent" in event:
                msg = event["agent"]["messages"][-1]
                if hasattr(msg, "content") and msg.content:
                    yield msg.content

