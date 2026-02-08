# Topic3Tools

NOTE: for tasks 2, 4, and 5, I used ChatOllama instead of OpenAI, as it was a free service that allowed for running larger models on the cloud. I used `qwen3-next:80b-cloud` for this assignment. The functions used to call tools for ChatOllama were almost entirely the same as those used to call OpenAI.

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

## Notes on Tool Use
For the most part, the model was able to use the tools provided to perform the calculations required from the prompt. There were, however, a few occasions where the model attempted to perform the calculations itself, for example when the model was asked to compute sin(0) but used its own knowledge instead of the calculator tool. For conversations where the model successfully used tools, I kept the original prompt given without adding any instructions to use tools. For conversations where the model failed to use at least one tool, I changed the prompt from "You are a helpful assistant." (the original prompt) to "You are a helpful assistant that uses tools. If there is a tool available to perform a calculation, use that tool. Do not attempt to do the calculation on your own." The model behavior was random in that it did not always use the required tools on every run, but I was able to get the model to use the required tools with this new prompt after a few runs. 

Output files whose conversations used the new prompt insisting on tool use were `Task4/langgraph_advanced_output.txt`,  `Task5/task_5_stdout_all_tools_convo.txt`, and `Task5/task_5_stdout_letters_counts_retry.txt`. The last file contains an example of successfully calling the `num_letters` tool twice on the phrase "Mississippi riverboats" when asked if the phrase had more i's than s's, which the model had quote a bit of difficulty with when using the original prompt. The model only called the tool once with the original prompt to get the number of i's, though it is worth noting that at this point I had already asked the model to find the number of s's, so it is aso possible that model simply retrieved this value from its conversation history instead of calculating it again. I tested the model's ability to access information in its conversation history by asking it "How many r are in that same phrase?" and it correctly identified the number of r's in "Mississippi riverboats", confirming that it does have access to information in its conversation history.
