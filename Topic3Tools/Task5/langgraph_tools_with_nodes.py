# Import necessary libraries
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver #TASK 7: use for checkpointing
from typing import TypedDict
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from simpleeval import simple_eval
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
    print_trace: bool
    llm_with_tools: ChatOllama
    tools: list
    llm_response: str
    messages : list
    chat_history: list


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


def create_graph(llm):

    # =========================================================================
    # NODE 1: get_user_input
    # =========================================================================
    # This node reads a line of text from stdin and updates the state.
    # State changes:
    #   - user_input: Set to the text entered by the user
    #   - should_exit: Set to True if user typed quit/exit/q, False otherwise
    #   - llm_response: Unchanged (not modified by this node)
    def get_user_input(state: AgentState) -> dict:
        """
        Node that prompts the user for input via stdin.

        Reads state: Nothing (fresh input each iteration)
        Updates state:
            - user_input: The raw text entered by the user
            - should_exit: True if user wants to quit, False otherwise
        """

        tools = [get_weather, calculator, num_letters, consonant_vowel_ratio]
        
        llm_with_tools = state.get("llm_with_tools", llm.bind_tools(tools))

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
        
        if user_input.lower() == "verbose": #TASK 1: enable tracing, then cycle back to the user input node to get the next input from the user
            print("[TRACE]: verbose trace enabled!")
            return {
                "user_input": user_input,
                "should_exit": False,
                "print_trace": True,     
                "llm_with_tools": llm_with_tools, 
                "tools": tools,
            }
        
        elif user_input.lower() == "quiet": #TASK 1: disable tracing, then cycle back to the user input node to get the next input from the user
            return {
                "user_input": user_input,
                "should_exit": False,
                "print_trace": False,
                "llm_with_tools": llm_with_tools, 
                "tools": tools,
            }
        

        system_prompt = [{"role": "system", "content": "You are a helpful assistant."}] #TASK 5: initialize a system prompt to begin the chat history
        chat_history = state.get("chat_history", system_prompt) #TASK 5: get the current state or initialize it with a system prompt
        
        return { #Otherwise, accept the user input and move forward
            "user_input" : user_input,
            "should_exit" : False,
            "chat_history" : chat_history, 
            "llm_with_tools": llm_with_tools, 
            "tools": tools,
        }
    

    @tool
    def get_weather(location: str) -> str:
        """Get the current weather for a given location"""
        # Simulated weather data
        weather_data = {
            "San Francisco": "Sunny, 72Â°F",
            "New York": "Cloudy, 55Â°F",
            "London": "Rainy, 48Â°F",
            "Tokyo": "Clear, 65Â°F"
        }

        result = weather_data.get(location, f"Weather data not available for {location}")

        print(f'[TRACE] calling tool: get_weather() with input: {location}, got result: {result}')

        return result

    @tool
    def calculator(expr: str):

        """Evaluate the input mathematical expression."""

        allowed_functions = {"sin": math.sin, "cos": math.cos}
        calc_data = {
            expr : str(simple_eval(expr, functions=allowed_functions))
        }

        result = calc_data.get(expr, f"Expression could not be parsed: {expr}")

        print(f'[TRACE] calling tool: calculator() with input: {expr}, got result: {result}')

        return result


    @tool
    def num_letters(phrase: str, letter:str):

        """Count how many times the given letter occurs in the phrase"""

        num_occurrances = 0
        letter = letter.lower() #lowercase for equal comparison

        for c in phrase.lower(): #count characters
            if c == letter:
                num_occurrances += 1

        print(f'[TRACE] calling tool: num_letters() with inputs: {phrase}, {letter}, got result: {num_occurrances}')

        return num_occurrances


    @tool
    def consonant_vowel_ratio(phrase:str):

        '''Return the ratio of consonants to vowels in a given phrase.'''

        vowels = ["a", "e", "i", "o", "u"]
        v = 0
        c = 0

        for letter in phrase.lower():
            if letter in vowels:
                v +=1
            else:
                if letter == " ": #ignore spaces
                    continue
                c += 1

        c_v_ratio = round((c / v), 2)

        print(f'[TRACE] calling tool: consonant_vowel_ratio() with input: {phrase}, got result: {c_v_ratio}')

        return c_v_ratio
    

    def call_llm(state: AgentState):

        user_query = state["user_input"]
        llm_with_tools = state["llm_with_tools"]
        chat_history = state["chat_history"]

        if not chat_history or not isinstance(chat_history[-1], HumanMessage):
            chat_history.append(HumanMessage(content=user_query))

        response = llm_with_tools.invoke(chat_history)

        return {"llm_response": response, "chat_history": chat_history + [response]}
    


    def route_user_input(state: AgentState):

        if state.get("should_exit", False):
            if state.get("print_trace", False): #if tracing is enabled, print tracing information here
                print(f'[TRACE] Routing: exiting program...')
            return END
        
        user_input = state.get("user_input", "")

        if user_input == "" or user_input.lower() in ["verbose", "quiet"]:
            return "get_user_input"

        if state.get("print_trace", False): #if tracing is enabled, print tracing information here
            print(f'[TRACE] Routing: calling LLM...')

        if user_input.lower() in ["verbose", "quiet"]: #if the user enters a keyword to update the tracing information, go back to the user input node to get the next input
            print(f'Got input {user_input}, updating trace variable...')
            return "get_user_input"
        
        if state.get("should_exit", False):
            return END
    
        return "call_llm"
    
    
    def route_after_llm(state: AgentState):

        if state.get("should_exit", False):
            if state.get("print_trace", False): #if tracing is enabled, print tracing information here
                print(f'[TRACE] Routing: exiting program...')
            return END

        last_message = state["llm_response"]

        if last_message.tool_calls:
            return "call_tools"
        
        return "print_response"
    

    def call_tools(state: AgentState):

        last_message = state["llm_response"]
        tools = state["tools"]
        tool_map = {tool.name: tool for tool in tools}
        chat_history = state["chat_history"]
        tool_messages = []

        for tool_call in last_message.tool_calls:
            tool = tool_map[tool_call["name"]]
            result = tool.invoke(tool_call["args"])
            tool_messages.append(ToolMessage(content=str(result), tool_call_id = tool_call["id"]))

        return{"chat_history": chat_history + tool_messages} 
    

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
    graph_builder.add_node("call_llm", call_llm)
    graph_builder.add_node("call_tools", call_tools)
    graph_builder.add_node("print_response", print_response)

    # Define edges:
    # 1. START -> get_user_input (always start by getting user input)
    graph_builder.add_edge(START, "get_user_input")
    graph_builder.add_edge("print_response", "get_user_input")
    graph_builder.add_edge("call_tools", "call_llm")

  
    graph_builder.add_conditional_edges(
        "call_llm",
        route_after_llm,
        {
            "call_tools": "call_tools",
            "print_response": "print_response"
        }
    )
    
    graph_builder.add_conditional_edges(
        "get_user_input",      # Source node
        route_user_input,      # Routing function that examines state
        {   "get_user_input": "get_user_input",
            "call_llm": "call_llm",
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

    #TASK 7: initialize checkpointer
    with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:

        graph = graph_builder.compile(checkpointer=checkpointer)

        thread_id = "workflow_1"
        config = {"configurable": {"thread_id": thread_id}}

        # Check for existing state
        current_state = graph.get_state(config)


        # Step 3: Save a visual representation of the graph before execution
        # This happens BEFORE any graph execution, showing the graph structure
        print("\nSaving graph visualization...")
        save_graph_image(graph)

        initial_state: AgentState = {
            "user_input": "",
            "should_exit": False,
            "llm_response": "",
            "print_trace" : False,
        }


        if current_state.next:
            print("🔄 Found incomplete workflow. Resuming...")
            print(f"   Completed so far: {current_state.values.get('messages', [])}")
            print(f"   Resuming at: {current_state.next}")
            graph.invoke(None, config=config)

        else:
            print("▶️  Starting new workflow...")
            graph.invoke(initial_state, config=config)


if __name__ == "__main__":
    main()