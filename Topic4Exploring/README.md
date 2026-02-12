#NOTE: for this assignment I also used Ollama with `qwen3-next:80b-cloud` as the model.

## Task 1
1. What features of Python does ToolNode use to dispatch tools in parallel?  What kinds of tools would most benefit from parallel dispatch?

I used Gemini to look up the answer to the first question. ToolNode implements different methods of parallelization depending on whether it recieves a synchronous call (via `invoke()`) or an asynchronous call (via `ainvoke()`). For synchronous calls, ToolNode uses Python's `ThreadPoolExecutor` to run tools in parallel. For asynchronous calls, ToolNode uses Python's `asyncio.gather()` function to run the tools in parallel. 

Tools that would benefit most from parallel dispatch are tools that do not need to wait for information from other tools to be found before they are called (for example, a calculator tool might need to wait for a temparature to be computed using a weather tool if that temperature is to be used in its calculation). On the other hand, tools that retrieve information like the weather for a particular location, the population of a city, or facts about a certain subject (e.g., from a Wikipedia article) are unlikely to have to wait to recieve information from other tools before they can be called. They can thus run in parallel.

2. How do the two programs handle special inputs such as "verbose" and "exit"?

The programs keep variables in the state to keep track of any keyword commands have been entered by the user (including "verbose" and "exit") and what their values are. The name of the most recently typed command is kept as a string in the `command` cell of the state. For verbose tracing, an additional boolean variable named `verbose` is kept in the state, whose value is `True` any time after the user types the keyword "verbose" and `False` by default or whenever the user inputs the keyword "quiet". This allows the program to check the value of these variables at different points during computation and, according to their value, to determine whether to exit the program, or turn on/turn off tracing and perform the appropriate routing call to the next node.

3. Compare the graph diagrams of the two programs.  How do they differ if at all?

I compared the following graphs: `langchain_manual_tool_graph.png` for the manual ToolNode agent, and `langchain_conversation_graph.png` for the ReAct agent. The graphs are very similar, but they differ in how they call the agent. The ReAct agent's graph combines running the agent and tool calls into one singular node, after which the only possible path is to the output node. By contrast, the manual ToolNode graph uses separate nodes for calling the model and calling tools such that if there are no tools to call, the computation shifts directly to the `output` node, and if there are tools to call, the graph goes back and forth between the `call_model` node and the `tools` node until all tools have been called and the computation is ready to proceed to the `output` node. 

4. What is an example of a case where the structure imposed by the LangChain react agent is too restrictive and you'd want to pursue the toolnode approach? 

The ReAct agent might be too restrictive if some of the queries require tool calls while other don't. The manual ToolNode graph allows for the model to skip the `tools` node and go straight to the `output` node if no tools need to be called, while the ReAct agent graph requires all inputs to be passed to the `call_react_agent` node, which handles tool calls, regardless of whether the input requires them or not. Therefore, the manual ToolNode structure might provide some flexibility for queries not requiring tool calls to not have to interact with any tool-calling structure at all and simply be passed along to the `output` node.

## Task 3

Task 3 TOC:
- `info_search.py`: my code file for running the Wikipedia and DuckDuckGo tools, based on the ReAct agent code provided.
- `langchain_conversation_graph.png`: the general graph for the ReAct agent pipeline
- `langchain_react_agent.png `: the ReAct agent specific graph
- `task_3_chili_recipe.txt`: the conversation with the model in response to prompt #4
- `task_3_linguistics_and_cs.txt`: the conversation with the model in response to prompt #3
- `task_3_rainbows_convo.txt`: the conversation with the model in response to prompt #1
- `task_3_scrambled_eggs.txxt`: the conversation with the model in response to pormpt #2

In this task, I implement an agent that takes a search query and searches both Wikipedia and DuckDuckGo for a response. The model outputs a summary of the responses from both sources and compares and contrasts the information in the responses. I query the model with the following prompts:

1. "What are rainbows?" 
2. "How to make scrambled eggs"
3. "How is linguistics related to computer science?"
4. "Chili recipe"

The first query asks for factual information, which both Wikipedia and DuckDuckGo provide, though from different angles (`Task3/task3_rainbows_convo.txt`). Queries number 2 and 4 ask for instructions on how to cook food, and there is a divergence in the information given by Wikipedia and DuckDuckGo. Perhaps unsurprisingly, information from Wikipedia focuses more on the historical and cultural angles of the dishes while DuckDuckGo provides resources on how to prepare the dishes, demonstrating that DuckDuckGo might be a more reliable source when it comes to learning how to do something step by step. Conversations for prompts 2 and 4 can be found in `Task3/task3_scrambled_eggs.txt` and `Task3/task3_chili_recipe.txt`, respectively. Query number 3 asks a more specific question about how linguistics is related to computer science, as much interdisciplenary research has stemmed from the interactions between both fields. Both Wikipedia and DuckDuckGo return meaningful responses, though from different angles, suggesting that the best source to use depends on type of information you're searching for.






