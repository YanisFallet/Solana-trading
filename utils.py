import json

def load_addresses():
    with open("input/addresses.json", "r") as f:
        return json.load(f)