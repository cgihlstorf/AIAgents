# Topic7MCP - Task 1

# TOC
- `exercise_a/exercise_a.py`: the python script to run exercise a
- `exercise_a/exercise_a_response.txt`: the output from exercise a
- `exercise_b/exercise_b.py`: the python script to run exercise b
- `exercise_b/exercise_b_drill_1_results.txt`: results from drill 1 of exercise b
- `exercise_b/drill_2_results.txt`: results from drill 2 of exercise b
- `exercise_b/drill_3_results.txt`: results from drill 3 of exercise b
- `exercise_c/exercise_c.py`: the python script to run exercise c
- `exercise_c/prompt_1_response.txt`: the chatbot's response to prompt 1 in the assignment
- `exercise_c/prompt_2_response.txt`: the chatbot's response to prompt 2 in the assignment
- `exercise_c/prompt_3_response.txt`: the chatbot's response to prompt 3 in the assignment
- `exercise_c/prompt_4_response.txt`: the chatbot's response to prompt 4 in the assignment
- `exercise_c/lg_graph.png`: the langgraph graph for the chatbot
- `exercise_d/exercise_d.py`: the python script to run exercise d
- `exercise_d/model_response.md `: the model's response for exercise d

### Exercise A

#### Which tool would you use to find all papers about "transformer attention mechanisms"? 

I would use the 'search_papers_by_relevance' tool, as it searches for papers based on the keywords in the input.

#### 2. Which would you use to find who else published in the same area as a specific author?
There are two approaches I could use: First, I could use is choosing a few papers by the authors that are representative of their research area and, for each paper, using the 'get_citations' tool to get the papers that cite the paper (assuming these papers will be in a similar research area). I could then use the 'get_paper' tool to get the authors from each paper (if author information is provided by the tool and if the paper id is available). Second, I could first use the 'get_author_papers' tool to get the papers written by the author to get a sense of what the author's research area is. Then I would use the 'search_papers_by_relevance' tool to do a keyword search for similar papers in that area and for each paper found, I could either manually inspect who the authors are or I could use the 'get_paper' tool if the paper id is provided to get the names of the authors of that paper, if that information is available via this tool call.

### Exercise B

#### What differences did you notice in the structure of results across the three tools? How did you handle the JSON returned inside the content[0]["text"] field?

The results for all three drills are structured similarly. All are lists of dictionaries, with the relevant fields to be printed located in the value of the "text" key. One issue, however, was that this value was structured as a dictionary but was a string. I used the `json.loads()` function to transform this string into a dictionary so I could access the fields using normal dictionary calls. The dictionaries returned for each drill contained the information that was specified in the "fields" key of the payload, and this information differed for each drill depending on which information I wanted (e.g., references for a publication, its year title, authors, etc). 

### Exercise C

#### What changed compared to calling tools manually in Exercise B? You wrote almost no tool-specific code — the schema came from the server. The chatbot would work identically if Asta added new tools tomorrow. That is the core value of MCP.

In Exercise B, I manually defined calls to specific tools that I knew were available based on the set of tools I found from Exercise A. In order to call a specific tool, I would have to manually specify the tool I wanted to use and code a unique parsing algorithm to get the desired information from the output of the tool call. I would also have to ensure that the tool I wanted to call was available, which, when relying on the fixed list of tools from Exercise A, might be limiting if new tools are added, tools are removed, or the names of tools change. The chatbot in this exercise allows for all available tools to be called using the same configuration, as the language model does the work of deciding which tools to use based on the query. Additionally, the model has access to the most current set of tools at every call because it retrieves them before asking for the input query. This configuration is thus more generalizable to different tools and most current with respect to the tools available.

### Closing Discussion

#### You wrote tool schemas by hand in concept, then saw MCP provide them dynamically. What does this automation buy you? What does it cost (complexity, new failure modes)?

This level of automation saves time by removing the need to write a new tool schema every time you want to use a new tool with your model. Depending on the reliability of the automatic retrieval system, however, it may result in some information being missed when a particular source is requested due to errors in the retrieval process that miss important details.

#### The Asta tools return rich JSON. How did you decide what to include in the context window and what to discard? What happened to response quality when you passed everything vs. a summary?

For most tasks, I simply added the output json string from the MCP call into the model's context. For results like the top 5 most-cited references, I only took the first 5 references to make that input string simpler, but I left it in dictionary format. When getting the most-cited work for each author, I first got the list of dictionaries containing information about each author, then wrote a script to get the most-cited work for each author and simply added that information back into the original dictionary for each author.

#### In Exercise D, you controlled the tool-calling order. What would it take to let the LLM decide the order? What could go wrong?

The LLM would have to be carefully prompted to determine the proper order of operations of each tool call. If the LLM is good enough to do this, automting this step could reduce the human effort required to make the calls. But LLMs are nondeterministic and prone to mistakes and hallucinations, so even if an LLM produces the proper order or operations on one call, it might fail to produce the proper order on another call due to the randomness in its generation algorithm. Though it might not be fully possible to prevent such errors, it might be possible to mitigate them via prompting by either providing very specific instructions about the order of operations or giving one or more in-context examples. It might also be helpful to have the LLM "self-check" its answer before it gives its final output, allowing it another chance to fix order of operations errors before the final result is returned.

#### MCP is a relatively young standard. What would you want a mature MCP ecosystem to offer that is not available today?

In the context of the system used for this assignment, I would like a mature version of the system to be able to summarize the different research areas that a particular author has worked in over time and return representative works for each of those areas. This would be helpful in tracking the research foci of authors over time as well as the particular contributions they made in each area. 
