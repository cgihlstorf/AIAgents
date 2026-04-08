## Topic7MCP

### Exercise B

#### What differences did you notice in the structure of results across the three tools? How did you handle the JSON returned inside the content[0]["text"] field?

The results for all three drills are structured similarly. All a lists of dictionaries, with the relevant fields to be printed located in the value to the "text" key. One issue, however, was that this value was structured as a dictionary but was a string. I used the `json.loads()` function to transform this string into a dictionary so I could access the fields using normal dictionary calls. The dictionaries returned for each drill contained the information that was specified in the "fields" key of the payload, and this information differed for each drill depending on which information I wanted (e.g., references for a publication, its year title, authors, etc). 

**TODO** need results for drill 3

### Exercise C

#### What changed compared to calling tools manually in Exercise B? You wrote almost no tool-specific code — the schema came from the server. The chatbot would work identically if Asta added new tools tomorrow. That is the core value of MCP.

In Exercise B, I manually defined calls to specific tools that I knew were available based on the set of tools I found from Exercise A. In order to call a specific tool, I would have to manually specify the tool I wanted to use and code a unique parsing algorithm to get the desired information from the output of the tool call. I would also have to ensure that the tool I wanted to call was available, which, when relying on the fixed list of tools from Exercise A, might be limiting if new tools are added, tools are removed, or the names of tools change. The chatbot in this exercise allows for all available tools to be called using the same configuration, as the language model does the work of deciding which tools to use based on the query. Additionally, the model has access to the most current set of tools at every call because it retrieves them before asking for the input query. This configuration is thus more generalizable to different tools and most current with respect to the tools available.
