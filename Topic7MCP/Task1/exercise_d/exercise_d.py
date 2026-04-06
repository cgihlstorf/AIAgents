import ollama
import requests, os, json
import fire

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

        new_result = get_result(requests.post(url, headers=headers, json=new_payload))
        
        try:
           new_results.append(json.loads(new_result[0]["text"]))

        except:
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

    
    return authors


def main(paper_id:str):

    url = "https://asta-tools.allen.ai/mcp/v1"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "x-api-key": os.environ["ASTA_API_KEY"]
    }

    prompt = "You will be given metadata about a research paper. Please generate a structured markdown report containing: \n\n"
    prompt += "- A one-paragraph summary of the seed paper\n"
    prompt += "A \"Foundational Works\" section with the 5 key references\n"
    prompt += "A \"Recent Developments\" section with 5 citing papers\n"
    prompt += "An \"Author Profiles\" section with each author's most notable other work\n\n"
    prompt += "Here is the metadata:\n\n"


    general_metadata = str(get_metadata(url, headers, paper_id))
    top_5_abstracts = str(get_top_5_refs(url, headers, paper_id))
    recent_citing_papers = str(get_citing_papers_past_3_years(url, headers, paper_id))
    authors_most_cited_other_works = str(get_authors_other_works(url, headers, paper_id))

    prompt += "General Metadata:\n" + general_metadata + "\n\n"
    prompt += "Top 5 Most-Cited Abstracts:\n" + top_5_abstracts + "\n\n"
    prompt += "Papers that cite the research paper:\n" + recent_citing_papers + "\n\n"
    prompt += "Most Cited Work for each Author:" + authors_most_cited_other_works


    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = ollama.chat(
        model="qwen3-next:80b-cloud",
        messages=messages,
    )

    print(response)


    

if __name__ == "__main__":

    #paper_id = "ARXIV:2210.03629"
    fire.Fire(main)