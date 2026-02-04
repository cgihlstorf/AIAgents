# Topic3Tools

NOTE: for this assignment, I used ChatOllama() instead of OpenAI, as it was a free service that allowed for running larger models on the cloud. I used `qwen3-next:80b-cloud` for this assignment. The functions used to call tools for ChatOllama were almost entirely tha same as those used to call OpenAI, so only minimal changed to the code were made.

## Task 1

The real times taken by each process are as follows:

1. Original - sequential: 63.22s
2. Original - parallel: 82.75s 
3. Ollama - sequential: 2183s
4. Ollama - parallel: 2862s

Running Ollama took far more time than running the original models from HuggingFace. For both the HuggingFace and Ollama models, running the two programs sequentially took less time than running the two programs in parallel.


## Task 2

- `manual_tool_handling.py` contains code to run the LLM with manually defined tools.
- `manual_tools_stdout.txt` contains model outputs from test prompts that require the model to use the defined tools.



## Task 4

I created the following query that used all my tools: `What is the sine of the weather in San Francisco times the number of l in lullaby plus the ratio of consonants to vowels in computer science?`
This query should call the weather tool to get the weather in San Francisco and the calculator tool to get the sine of this value. It should also call the tool to calculate the number of letters in a word (`num_letters`) to get the number of l's in `lullaby` and the `consonant_vowel_ratio` tool to get the ratio of consonants to vowel ratio of letters in `computer science`. The model output for this query is located in `langgraph_tools_combined_stdout.txt`. The model successfully called all tools. This query also took the model through 4 sequential chain loops, which is the closest I achieved to reaching the 5-loop limit.

## Task 5

- `checkpoints.db` contains the checkpoints for program recovery.
- `lg_graph.png` contains a Mermaid diagram of the graph used for calling the model and tools.
- `task_5_stdout_convo_1.txt` contains a conversation I had with the model using LangGraph nodes to facilitate model inference and tool calls. I use several prompts for the model, each of which calls a different tool/combination of tools such that all tools are called at least once during the conversation. The file also demonstrates recovery from a keyboard interrupt.
- `task_5_stdout_all_tools_convo.txt` contains a conversation I had with the model using a prompt that required the model to call all tools. 

## Task 6
### Question: where is there an opportunity for parallelization in your agent that is not yet being taken advantage of?  

Right now, the code I have to call tools requires tools to be called sequentially, each time after the LLM is called (this is displayed in the Mermaid diagram between the `call_llm` and `call_tools` nodes (`Task5/lg_graph.png`)). There is, however, an opportunity to parallelize tool calls. Once the model knows which tools it has to call for a certain input, it could call multiple tools in parallel instead of calling them sequentially. This would speed up the computation by allowing different tools to run at the same time.
