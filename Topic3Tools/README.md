# Topic3Tools

## Task 1

The real times taken by each process are as follows:

1. Original - sequential: 63.22s
2. Original - parallel: 82.75s 
3. Ollama - sequential: 2183s
4. Ollama - parallel: 2862s

Running Ollama took far more time than running the original models from HuggingFace. For both the HuggingFace and Ollama models, running the two programs sequentially took less time than running the two programs in parallel.


## Task 4

I created the following query that used all my tools: `What is the sine of the weather in San Francisco times the number of l in lullaby plus the ratio of consonants to vowels in computer science?`
This query should call the weather tool to get the weather in San Francisco and the calculator tool to get the sine of this value. It should also call the tool to calculate the number of letters in a word (`num_letters`) to get the number of l's in `lullaby` and the `consonant_vowel_ratio` tool to get the ratio of consonants to vowel ratio of letters in `computer science`. The model output for this query is located in `langgraph_tools_combined_stdout.txt`. The model successfully called all tools. This query also took the model through 4 sequential chain loops, which is the closest I achieved to reaching the 5-loop limit.