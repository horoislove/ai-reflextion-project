import requests

def generate_response(messages):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma4:31b-cloud",
            "messages": messages,
            "stream": False
        }
    )

    return response.json()["message"]["content"]