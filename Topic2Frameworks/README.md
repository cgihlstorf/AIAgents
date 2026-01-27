# Table of Contents

Below are the names of the folders in this directory as well as explanations of what each file in each folder contains.

## Task1
This folder contains the starter code modified so that when the input to the model is `verbose`, the system prints tracing information as the program runs. When the input is `quiet`, the model stops printing this tracing information.

- `langgraph_llama_task_1.py` contains the modified code. 
- `lg_graph.png` contains a visualization of the graph. 
- `task_1_stdout.txt` contains the command line output of my interaction with the model demonstrating the use of `verbose` and `quiet` to enable and disable tracing information.

## Task2 

### Contents

- `task_2_stdout_empty_input_1.txt` and `task_2_stdout_empty_input_2.txt` show the model responses for each time I prompted it with an empty input.
- `langgraph_llama_task_2.py` shows the code modified for this task. Changes made from the previous code file are marked with comments containing the phrase `TASK 2:`. 
- `lg_graph.png` shows the updated graph after I made the changes.

### Empty Inputs Analysis
I gave `Llama-3.2 1B Instruct` an empty input twice and recorded its responses. In both cases, the model hallucinated a conversation between a user and an assistant, though the topic was different each time. The first empty input resulted in a simulated conversation about mental health in the workplace, while the second empty input resulted in a simulated conversation about organizing documents in folders. This suggests that smaller language models, like the one used here, are unable to interpret an empty input as a sign to perhaps wait for another input from the user or ask user a question to get a non-empty input that they can work with. Instead, they default to generating random conversations and ignore the fact that they should be waiting on the user to begin a conversation with a nonempty string.


## Task3

- `langgraph_llama_task_3.py` contains new changes to the code I made to get both `Llama` and `Qwen` to run in parallel. Comments in this file denoted with `TASK 3:` mark the lines where I modified/added code. 
- `lg_graph.png` contains the image of the new graph resulting from my changes. 
- `task_3_stdout.txt ` contains printouts to stdout of my conversation with both models in parallel.

## Task4

- `langgraph_llama_task_4.py` contains changes to the code from the previous tasks such that when "Hey Qwen" is the first part of the input, `Qwen` is run instead of `Llama`. My changes for this task are denoted by comments begining with `TASK 4`. 
- `lg_graph.png` shows the updated graph. 
- `task_4_stdout.txt` contains text from a conversation I had with the models demonstrating the use of "Hey Qwen" to call the `Qwen` model. 

## Task5

- `langgraph_llama_task_5.py` contains code modified to include a chat history using the Message API. Comments with changes made for this task contain the label `Task 5`.
- `lg_graph.png` contains the image of the graph for this task.
- `task_5_stdout.txt` contains a conversation I had with the model, and includes traces of the chat history build up after each conversation turn.

## Task6

- `langgraph_llama_task_6.py` contains code modified to call both `Llama` and `Qwen` in a conversation, specifiying different roles and system prompts in the chat history for each model depending on which model is currently the assistant. Changes made to the code are marked with comments starting with `TASK 6:`.
- `lg_graph.png` shows the graph for this task.
- `task_6_books_stdout.txt`, `task_6_ice_cream_stdout.txt`, and `task_6_study_breaks_stdout.txt` each contain conversations I had the models along with chat histories demonstrating the changes to roles and system prompts imlemented for this task.

## Task7

- `checkpoints.db` contains checkpint information in case the conversation crashes and the system needs to restart while maintaining conversation history.
- `langgraph_llama_task_7.py` contains the code modified to include checkpointing so that the system will resume where it left off if it crashes. Comments denoting changes to the code in this file begin with `TASK 7:`.
- `lg_graph.png` shows the graph for this task.
- `task_7_stdout.txt` contains text from a conversation I had with the model after crashing the program a few times. The file shows one point where I cancel the program and restart, but even before this I canceled the program a couple of times, and the conversation history from those previous runs is displayed on lines 38 and 107.
