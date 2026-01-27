import requests
import json

def call_ollama(prompt, model="llama3.2:1b"):
    response = requests.post('http://localhost:11434/api/generate',
                            json={
                                "model": model,
                                "prompt": prompt,
                                "stream": False
                            })
    return response.json()['response']


if __name__ == "__main__":
    # Use it
    result = call_ollama("Explain transformers in one sentence")
    print("Response:", result)