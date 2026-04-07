import requests, os
import json

#export ASTA_API_KEY=O9erX9VmDRaCr3nbeP0rv9vXjrIabigS96m4Hg4g

def get_result(result):

    result_items = []

    for l in result.iter_lines():
        result_items.append(l)

    result_str = result_items[1].decode("utf-8").replace("data:", "").strip()
    
    try:
        result_dict = json.loads(result_str)
        result_final = result_dict["result"]["content"]
    except:
        result_final = {}
    

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

    print("====================Drill 2 Results====================\n")

    print("Results Count:", results_count)

    print("\n")

    print("Top 5 Papers:\n")
    
    for i in range(len(result[0:5])): #only go through the first 5 papers

        paper = json.loads(result[i]["text"])["citingPaper"]

        print(str(i + 1) + ")", paper["title"])

        print("\n")


def drill_3():

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
            "name": "get_paper",
            "arguments": {
                    "paper_id": "ARXIV:2210.03629",
                    "fields": "references, year",
                    "limit": 10,
                    "publication_date_range": "2023-01-01:"
                }
            }
        }
    
    references = json.loads(get_result(requests.post(url, headers=headers, json=payload))[0]["text"])["references"]
    references_info = {}

    for ref_dict in references:
        
        ref_id = ref_dict["paperId"]

        payload_r = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_paper",
                "arguments": {
                        "paper_id": ref_id,
                        "fields": "year",
                        "limit": 1,
                    }
                }
            }
        
        year_result = get_result(requests.post(url, headers=headers, json=payload_r))
        
        try:
            ref_year = json.loads(year_result[0]["text"])["year"]
        except:
            continue #if there is no year, do not count this paper
        
        references_info[ref_dict["title"]] = ref_year


    references_info = {key: value for key, value in sorted(references_info.items(), key=lambda item: item[1], reverse=True)}


    for ref_title in references_info.keys():
        print(ref_title, references_info[ref_title])




if __name__ == "__main__":
    #drill_1()
    #drill_2()
    drill_3()