## Topic7MCP

### Exercise B

#### What differences did you notice in the structure of results across the three tools? How did you handle the JSON returned inside the content[0]["text"] field?

The results for drill 1 and drill 2 are structured similarly. Both are a lists of dictionaries, with the relevant fields to be printed located in the value to the "text" key. One issue, however, was that this value was structured as a dictionary but was a string. I used the `json.loads()` method to transform this string into a dictionary so I could access the fields using normal dictionary calls. The dictionaries returned for drill 1 and drill 2 share many of the same fields, though the result returned for drill 1 contains 2 additional fields, `openAccessPdf` and `abstract`, that the result for drill 2 does not contain. 

**TODO** need results for drill 3