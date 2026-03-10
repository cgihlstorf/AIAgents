import requests, os
import json

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

print("==================== Tools ====================")

for tool in tools:
    name = tool["name"]
    description = tool["description"]

    print("Tool Name:", name)
    print()
    print("Tool Description:", description)
    print()
    print("Required Parameters:")
    
    required_params = tool["inputSchema"]["required"]
    properties = tool["inputSchema"]["properties"]
    for r in required_params:
        r_type = properties[r]["type"]
        print(r + ":", "Type", r_type)

    print("==" * 60)