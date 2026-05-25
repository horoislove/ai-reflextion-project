import json

FILE = "data/conversations.json"

def load_memory():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

