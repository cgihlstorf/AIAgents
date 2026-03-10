import requests, os
import json

def get_result(result):

    result_items = []

    for l in result.iter_lines():
        result_items.append(l)

    result_str = result_items[1].decode("utf-8").replace("data:", "").strip()
    result_dict = json.loads(result_str)
    
    result_final = result_dict["result"]["content"]

    return result_final

def drill_1():

    url = "https://asta-tools.allen.ai/mcp/v1"
    limit = 5

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-api-key": os.environ["ASTA_API_KEY"]
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "search_papers_by_relevance",
            "arguments": {
                "keyword": "large language model agents",
                "fields": "title,abstract,year,authors",
                "limit": limit
            }
        }
    }
    
    result = get_result(requests.post(url, headers=headers, json=payload))

    assert len(result) == limit

    print("====================Drill 1 Results====================\n")

    for i in range(len(result)):

        paper = json.loads(result[i]["text"])

        paper_title = paper["title"]
        paper_year = paper["year"]

        print("Title:", paper_title)
        print("Year:", paper_year)
        print("\n")



def drill_2():

    url = "https://asta-tools.allen.ai/mcp/v1"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-api-key": os.environ["ASTA_API_KEY"]
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_citations",
            "arguments": {
                    "paper_id": "ARXIV:1810.04805",
                    "fields": "title,year,authors",
                    "limit": 10,
                    "publication_date_range": "2023-01-01:"
                }
            }
        }
    
    result = get_result(requests.post(url, headers=headers, json=payload))

    results_count = len(result)

    print("====================Drill 1 Results====================\n")

    print("Results Count:", results_count)

    print("\n")

    print("Top 5 Papers:\n")
    
    for i in range(len(result[0:5])): #only go through the first 5 papers

        paper = json.loads(result[i]["text"])["citingPaper"]

        print(str(i + 1) + ")", paper["title"])

        print("\n")







    

    


if __name__ == "__main__":
    #drill_1()
    drill_2()