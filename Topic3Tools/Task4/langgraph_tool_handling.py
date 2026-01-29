"""
Tool Calling with LangChain
Shows how LangChain abstracts tool calling.
"""

#from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import ast
from simpleeval import simple_eval

# ============================================
# PART 1: Define Your Tools
# ============================================

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
    return weather_data.get(location, f"Weather data not available for {location}")

@tool
def calculator(expr: str):
    """Evaluate the input mathematical expression."""
    calc_data = {
        expr : str(simple_eval(expr))
    }
    return calc_data.get(expr, f"Expression could not be parsed: {expr}")


@tool
def num_letters(phrase: str, letter:str):

    """Count how many times the given letter occurs in the phrase"""

    num_occurrances = 0
    letter = letter.lower() #lowercase for equal comparison

    for c in phrase.lower(): #count characters
        if c == letter:
            num_occurrances += 1

    return num_occurrances





# ============================================
# PART 2: Create LLM with Tools
# ============================================

# Create LLM
llm = ChatOllama(model="qwen3-next:80b-cloud")

# Bind tools to LLM
# At the top with tool definitions
tools = [get_weather, calculator, num_letters]
tool_map = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)


# ============================================
# PART 3: The Agent Loop
# ============================================

def run_agent(user_query: str):
    """
    Simple agent that can use tools.
    Shows the manual loop that LangGraph automates.
    """
    
    # Start conversation with user query
    messages = [
        SystemMessage(content="You are a helpful assistant. Use the provided tools when needed."),
        HumanMessage(content=user_query)
    ]
    
    print(f"User: {user_query}\n")
    
    # Agent loop - can iterate up to 5 times
    for iteration in range(5):
        print(f"--- Iteration {iteration + 1} ---")
        
        # Call the LLM
        response = llm_with_tools.invoke(messages)
        
        # Check if the LLM wants to call a tool
        if response.tool_calls:
            print(f"LLM wants to call {len(response.tool_calls)} tool(s)")
            
            # Add the assistant's response to messages
            messages.append(response)
            
            # Execute each tool call
            for tool_call in response.tool_calls:
                function_name = tool_call["name"]
                function_args = tool_call["args"]
                
                print(f"  Tool: {function_name}")
                print(f"  Args: {function_args}")
                
                # Execute the tool
                if function_name in tool_map:
                    result = tool_map[function_name].invoke(function_args)
                else:
                    result = f"Error: Unknown function {function_name}"
                
                # Add the tool result back to the conversation
                messages.append(ToolMessage(
                    content=result,
                    tool_call_id=tool_call["id"]
                ))
            
            print()
            # Loop continues - LLM will see the tool results
            
        else:
            # No tool calls - LLM provided a final answer
            print(f"Assistant: {response.content}\n")
            return response.content
    
    return "Max iterations reached"


# ============================================
# PART 4: Test It
# ============================================

if __name__ == "__main__":
    #Test query that requires tool use
    print("="*60)
    print("TEST 1: Query requiring tool")
    print("="*60)
    run_agent("What's the weather like in San Francisco?")
    
    print("\n" + "="*60)
    print("TEST 2: Query not requiring tool")
    print("="*60)
    run_agent("Say hello!")
    
    print("\n" + "="*60)
    print("TEST 3: Multiple tool calls")
    print("="*60)
    run_agent("What's the weather in New York and London?")

    print("\n" + "="*60)
    print("TEST 4: Calculator")
    print("="*60)
    run_agent("What is 8 + 2?")

    print("\n" + "="*60)
    print("TEST 5: Calculator")
    print("="*60)
    run_agent("What is (5 ** 2) * 10 / 4?")

    print("\n" + "="*60)
    print("TEST 6: Counting letters")
    print("="*60)
    run_agent("How many s are in Mississippi riverboats?")