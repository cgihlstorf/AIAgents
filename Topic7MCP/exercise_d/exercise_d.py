from langchain_ollama import ChatOllama
import requests, os, json

def get_result(result):

    result_items = []

    for l in result.iter_lines():
        result_items.append(l)

    result_str = result_items[1].decode("utf-8").replace("data:", "").strip()
    result_dict = json.loads(result_str)
    
    result_final = result_dict["result"]["content"]

    return result_final


def get_metadata(url:str, headers:dict, paper_id:str):

    #Retrieve full metadata for the seed paper (title, abstract, year, authors, fields of study).
    
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_paper",
            "arguments": {
                "paper_id": paper_id,
                "fields": "title, abstract, year, authors",
            }
        }
    }
    
    result = json.loads(get_result(requests.post(url, headers=headers, json=payload))[0]["text"])

    return result


def get_top_5_refs(url:str, headers:dict):

    #Fetch the paper's references and retrieve abstracts for the 5 most-cited ones.

    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_citations",
            "arguments": {
                "paper_id": paper_id,
                "fields": "title, abstract, year, authors",
                "limit": 5,
            }
        }
    }

    result = json.loads(get_result(requests.post(url, headers=headers, json=payload))[0]["text"])
    
    assert len(result) == 5

    print(5)

    return result


if __name__ == "__main__":

    url = "https://asta-tools.allen.ai/mcp/v1"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-api-key": os.environ["ASTA_API_KEY"]
    }

    paper_id = "ARXIV:2210.03629"

    get_metadata(url, headers, paper_id)