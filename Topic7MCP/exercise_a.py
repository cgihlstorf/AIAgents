import requests, os
import json

########## Answers to Discussion Questions ##########

# 1. Which tool would you use to find all papers about "transformer attention mechanisms"? 
# I would use the 'search_papers_by_relevance' tool, as it searches for papers based on the keywords in the input.

# 2. Which would you use to find who else published in the same area as a specific author?
# There are two approaches I could use: First, I could use is choosing a few papers by the authors that are representative of their research area
# and, for each paper, using the 'get_citations' tool to get the papers that cite the paper (assuming these papers will
# be in a similar research area). I could then use the 'get_paper' tool to get the authors from each paper (if author 
# information is provided by the tool and if the paper id is available). 
# Second, I could first use the 'get_author_papers' tool to get the papers written by the author to get a sense of 
# what the author's research area is. Then I would use the 'search_papers_by_relevance' tool to do a keyword search 
# for similar papers in that area and for each paper found, I could either manually inspect who the authors are or I 
# could use the 'get_paper' tool if the paper id is provided to get the names of the authors of that paper, if that 
# information is available via this tool call.


headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "x-api-key": os.environ["ASTA_API_KEY"]
}
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
}
resp = requests.post(
    "https://asta-tools.allen.ai/mcp/v1",
    headers=headers,
    json=payload,
    stream=True,
)
# Your printing logic here
resp_items = []
for l in resp.iter_lines():
    resp_items.append(l)

resp_str = resp_items[1].decode("utf-8").replace("data:", "").strip()
resp_dict = json.loads(resp_str)

tools = resp_dict["result"]["tools"]

for tool in tools:
    name = tool["name"]
    description = tool["description"].split("Args:")[0].strip()


    print("Tool:", name)
    print("  Description:", description)

    properties = tool["inputSchema"]["properties"]
    required_params = tool["inputSchema"]["required"]
    required_str = ""

    for r in required_params:

        r_type = properties[r]["type"]

        required_str += r + f" ({r_type})"
        
        if required_params.index(r) != len(required_params) - 1: #don't include a comma for the last item in the list
            required_str += ", "

    all_params = list(properties.keys())

    print("  Required:", required_str)

    optional_str = ""

    for o in all_params:

        if o not in required_params: #skip required params

            o_type = properties[o]["type"]

            optional_str += o + f" ({o_type})"

            if all_params.index(o) != len(all_params) - 1:
                optional_str += ", "

    print("  Optional:", optional_str)

    print("\n")