import json
import os

def save_to_json(data, filename):
    """
    Saves data to a JSON file, ensuring the directory structure exists.
    """
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)  

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {filename}")
