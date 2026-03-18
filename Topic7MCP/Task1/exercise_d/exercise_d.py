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


#TODO get tools
#TODO bind tools to model



if __name__ == "__main__":

    url = "https://asta-tools.allen.ai/mcp/v1"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-api-key": os.environ["ASTA_API_KEY"]
    }

    paper_id = "ARXIV:2210.03629"

    get_metadata(url, headers, paper_id)