from langchain_ollama import ChatOllama
import requests, os, json

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
                "fields": "title, abstract, year, authors, fieldsOfStudy",
            }
        }
    }
    
    result = json.loads(get_result(requests.post(url, headers=headers, json=payload))[0]["text"])

    return result


def get_top_5_refs(url:str, headers:dict, paper_id:str):

    #Fetch the paper's references and retrieve abstracts for the 5 most-cited ones.

    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_paper",
            "arguments": {
                "paper_id": paper_id,
                "fields": "references",
                "limit": 5,
            }
        }
    }

    result = json.loads(get_result(requests.post(url, headers=headers, json=payload))[0]["text"])["references"][0:5]

    assert len(result) == 5

    new_results = []

    for paper_dict in result:

        new_paper_id = paper_dict["paperId"]

        new_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_paper",
                "arguments": {
                    "paper_id": new_paper_id,
                    "fields": "abstract",
                    "limit": 5,
                }
            }
        }

        new_result = json.loads(get_result(requests.post(url, headers=headers, json=new_payload))[0]["text"])
        new_results.append(new_result)


    return new_results


def get_citing_papers_past_3_years(url:str, headers:dict, paper_id:str):

    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_citations",
            "arguments": {
                "paper_id": paper_id,
                "publication_date_range": "2023-04:2026:04"
            }
        }
    }
    
    result = json.loads(get_result(requests.post(url, headers=headers, json=payload))[0]["text"])

    return result


def get_authors_other_works(url:str, headers:dict, paper_id:str):

    #First, get the authors

    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_paper",
            "arguments": {
                "paper_id": paper_id,
                "fields": "authors",
            }
        }
    }

    authors = json.loads(get_result(requests.post(url, headers=headers, json=payload))[0]["text"])["authors"]

    for author_dict in authors:

        author_id = author_dict["authorId"]

        payload_2 = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_author_papers",
                "arguments": {
                    "author_id": author_id,
                }
            }
        }

        author_papers = get_result(requests.post(url, headers=headers, json=payload_2))

        paper_with_most_citations = {}
        most_citations = 0

        for author_paper_dict in author_papers:

            author_paper_dict = json.loads(author_paper_dict["text"])

            if author_paper_dict["paperId"] == paper_id:
                continue #don't consider the original paper used to search, only consider other papers

            payload_3 = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "get_citations",
                    "arguments": {
                        "paper_id": author_paper_dict["paperId"],
                    }
                }
            }

            result_citations = get_result(requests.post(url, headers=headers, json=payload_3))

            num_citations = len(result_citations)
            
            if (num_citations > most_citations): #make sure we are searching trough other papers besides this one
                
                most_citations = num_citations
                paper_with_most_citations = author_paper_dict

        author_dict["most_cited_paper"] = paper_with_most_citations

    print(authors)
    
    return authors





if __name__ == "__main__":

    url = "https://asta-tools.allen.ai/mcp/v1"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-api-key": os.environ["ASTA_API_KEY"]
    }

    paper_id = "ARXIV:2210.03629"

    #get_metadata(url, headers, paper_id)
    #get_top_5_refs(url, headers, paper_id)
    #get_citing_papers_past_3_years(url, headers, paper_id)
    get_authors_other_works(url, headers, paper_id)