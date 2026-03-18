# Import necessary libraries
import torch
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver 
from typing import TypedDict
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from simpleeval import simple_eval
import requests, os
import json
import math

# Determine the best available device for inference
# Priority: CUDA (NVIDIA GPU) > MPS (Apple Silicon) > CPU
def get_device():
    """
    Detect and return the best available compute device.
    Returns 'cuda' for NVIDIA GPUs, 'mps' for Apple Silicon, or 'cpu' as fallback.
    """
    if torch.cuda.is_available():
        print("Using CUDA (NVIDIA GPU) for inference")
        return "cuda"
    elif torch.backends.mps.is_available():
        print("Using MPS (Apple Silicon) for inference")
        return "mps"
    else:
        print("Using CPU for inference")
        return "cpu"

# =============================================================================
# STATE DEFINITION
# =============================================================================
# The state is a TypedDict that flows through all nodes in the graph.
# Each node can read from and write to specific fields in the state.
# LangGraph automatically merges the returned dict from each node into the state.

class AgentState(TypedDict):

    user_input: str
    should_exit: bool
    llm_with_tools: ChatOllama
    tools: list
    tool_calls: list
    messages: list
    llm_response: str



def create_llm():
    """
    Create and configure the LLM using HuggingFace's transformers library.
    Downloads llama-3.2-1B-Instruct from HuggingFace Hub and wraps it
    for use with LangChain via HuggingFacePipeline.
    """

    print(f"Loading model...")

    # Create LLM
    llm = ChatOllama(model="qwen3-next:80b-cloud")

    return llm


def get_result(result):

    result_items = []

    for l in result.iter_lines():
        result_items.append(l)

    result_str = result_items[1].decode("utf-8").replace("data:", "").strip()
    result_dict = json.loads(result_str)
    
    result_final = result_dict["result"]["content"]

    return result_final


def create_graph(llm):

    def get_user_input(state: AgentState) -> dict:
        """
        Node that prompts the user for input via stdin.

        Reads state: Nothing (fresh input each iteration)
        Updates state:
            - user_input: The raw text entered by the user
            - should_exit: True if user wants to quit, False otherwise
        """

        # Display banner before each prompt
        print("\n" + "=" * 50)
        print("Enter your text (or 'quit' to exit):")
        print("=" * 50)

        print("\n> ", end="")
        user_input = input()

        # Check if user wants to exit
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            return {
                "user_input": user_input,
                "should_exit": True        # Signal to exit the graph
            }

        # Any input (including empty) - continue to LLM
  
        system_prompt = [{"role": "system", "content": "You are a helpful assistant that uses tools. If there is a tool available to perform a calculation, use that tool. Do not attempt to do the calculation on your own."}] 
        messages = state["messages"]
        messages = messages + [HumanMessage(content=user_input)]
        
        return { #Otherwise, accept the user input and move forward
            "user_input" : user_input,
            "should_exit" : False,     
            "messages": messages
        }
    

    def get_asta_tools(state: AgentState):

        """Fetch tool schemas from MCP and convert to OpenAI format."""
        # Call tools/list, then transform each tool:
        # MCP: { name, description, inputSchema }
        # OpenAI: { type: "function", function: { name, description, parameters } }
        
        tools_openai_format = []
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "x-api-key": os.environ["ASTA_API_KEY"]
        }

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }

        resp = requests.post(
            "https://asta-tools.allen.ai/mcp/v1",
            headers=headers,
            json=payload,
            stream=True,
        )

        # Your printing logic here
        resp_items = []
        for l in resp.iter_lines():
            resp_items.append(l)

        resp_str = resp_items[1].decode("utf-8").replace("data:", "").strip()
        resp_dict = json.loads(resp_str)

        tools = resp_dict["result"]["tools"]

        for tool in tools:
            name = tool["name"]
            description = tool["description"].split("Args:")[0].strip()
            input_schema = tool["inputSchema"]

            tools_openai_format.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": input_schema,
                }
            })

        llm_with_tools = state.get("llm_with_tools", llm.bind_tools(tools))

        system_prompt = [{"role": "system", "content": "You are a helpful research assistant with Semantic Scholar access."}] 
        messages = state.get("messages", system_prompt) 

        return {"tools": tools_openai_format, "llm_with_tools": llm_with_tools, "messages": messages}

    def call_asta_tool(state: AgentState):
        
        """Execute a tools/call and return the text content."""

        tool_calls = state["tool_calls"]
        new_messages = []
        
        url = "https://asta-tools.allen.ai/mcp/v1"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "x-api-key": os.environ["ASTA_API_KEY"]
        }

        for t in tool_calls:

            name = t["name"]
            arguments = t["args"]

            print("====================Tool Call====================")
            print("Tool Name:", name)
            print("Tool Arguments:", arguments)
            print()

            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": name,
                    "arguments": arguments
                }
            }
            
            try:
                result = get_result(requests.post(url, headers=headers, json=payload)) #get the first item of the result
            
            except Exception as e:
                result = str(e) #use the error as the response
            
            new_messages.append(ToolMessage(content=str(result), tool_call_id=t["id"]))

        return {"messages": new_messages}

    def chat(state: AgentState):
        """One turn of the chatbot loop, handling tool calls."""

        messages = state["messages"]
        llm_with_tools = state["llm_with_tools"]

        llm_response = llm_with_tools.invoke(messages)
        tool_calls = llm_response.tool_calls

        return{"llm_response": llm_response, "messages": messages + [llm_response], "tool_calls": tool_calls}


    def route_user_input(state: AgentState):

        if state.get("should_exit", False):
            return END
        
        user_input = state.get("user_input", "")

        if user_input == "":
            return "get_user_input"
        
        if state.get("should_exit", False):
            return END
    
        return "chat"
    
    
    def route_after_llm(state: AgentState):

        if state.get("should_exit", False):
            return END

        tool_calls = state["tool_calls"]

        if tool_calls:
            return "call_asta_tool"
        
        return "print_response"
    
    

    # =========================================================================
    # NODE 3: print_response
    # =========================================================================
    # This node reads the LLM response from state and prints it to stdout.
    # State changes:
    #   - No changes (this node only reads state, doesn't modify it)
    def print_response(state: AgentState) -> dict:

        print("Assistant:", state["llm_response"].content)

        # Return empty dict - no state updates from this node
        return {}
    

    # =========================================================================
    # GRAPH CONSTRUCTION
    # =========================================================================
    # Create a StateGraph with our defined state structure
    graph_builder = StateGraph(AgentState)

    # Add all three nodes to the graph
    graph_builder.add_node("get_user_input", get_user_input)
    graph_builder.add_node("chat", chat)
    graph_builder.add_node("get_asta_tools", get_asta_tools)
    graph_builder.add_node("call_asta_tool", call_asta_tool)
    graph_builder.add_node("print_response", print_response)

    # Define edges:
    # 1. START -> get_user_input (always start by getting user input)
    graph_builder.add_edge(START, "get_asta_tools")
    graph_builder.add_edge("print_response", "get_user_input")
    graph_builder.add_edge("get_asta_tools", "get_user_input")
    graph_builder.add_edge("call_asta_tool", "chat")

  
    graph_builder.add_conditional_edges(
        "chat",
        route_after_llm,
        {
            "call_asta_tool": "call_asta_tool",
            "print_response": "print_response"
        }
    )
    
    graph_builder.add_conditional_edges(
        "get_user_input",      # Source node
        route_user_input,      # Routing function that examines state
        {   "get_user_input": "get_user_input",
            "chat": "chat",
            END: END                  # Quit command -> terminate graph
        }
    )

    return graph_builder
    
    

def save_graph_image(graph, filename="lg_graph.png"):
    """
    Generate a Mermaid diagram of the graph and save it as a PNG image.
    Uses the graph's built-in Mermaid export functionality.
    """
    try:
        # Get the Mermaid PNG representation of the graph
        # This requires the 'grandalf' package for rendering
        png_data = graph.get_graph(xray=True).draw_mermaid_png()

        # Write the PNG data to file
        with open(filename, "wb") as f:
            f.write(png_data)

        print(f"Graph image saved to {filename}")
    except Exception as e:
        print(f"Could not save graph image: {e}")
        print("You may need to install additional dependencies: pip install grandalf")



def main():
 
    print("=" * 50)
    print("Starting conversation...")
    print("=" * 50)
    print()

    # Step 1: Create and configure the LLM
    llm = create_llm()

    # Step 2: Build the LangGraph with the LLM
    print("\nCreating LangGraph...")
    graph_builder = create_graph(llm)
    print("Graph created successfully!")

    initial_state: AgentState = {
            "user_input": "",
            "should_exit": False,
            "llm_response": "",
            "messages": [],
            "tool_calls": [],
        }
    
    graph = graph_builder.compile()
    graph.invoke(initial_state)


if __name__ == "__main__":
    main()