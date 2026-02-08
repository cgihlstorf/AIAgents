## Task 1
1. What features of Python does ToolNode use to dispatch tools in parallel?  What kinds of tools would most benefit from parallel dispatch?

TODO: can we look this up?

2. How do the two programs handle special inputs such as "verbose" and "exit"?

The programs keep variables in the state to keep track of any keyword commands have been entered by the user (including "verbose" and "exit") and what their values are. The name of the most recently typed command is kept as a string in the `command` cell of the state. For verbose tracing, an additional boolean variable named `verbose` is kept in the state, whose value is `True` any time after the user types the keyword "verbose" and `False` by default or whenever the user inputs the keyword "quiet". This allows the program to check the value of these variables at different points during computation and, according to their value, to determine whether to exit the program, or turn on/turn off tracing and perform the appropriate routing call to the next node.

3. Compare the graph diagrams of the two programs.  How do they differ if at all?

TODO: should it be the other graph?

4. What is an example of a case where the structure imposed by the LangChain react agent is too restrictive and you'd want to pursue the toolnode approach? 

TODO


## Task 3

In this task, I implement an agent that takes a search query and searches both Wikipedia and DuckDuckGo for a response. The model outputs a summary of the responses from both sources and compares and contrasts the information in the responses.