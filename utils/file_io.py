# utils/file_io.py — JSON save & load helpers

import json
import os

def save_data(filename: str, data: list) -> None:
    """Save a list of dictionaries to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"  [✔] Data saved to {filename}")
    except IOError as e:
        print(f"  [✘] Failed to save {filename}: {e}")

def load_data(filename: str) -> list:
    """Load a list of dictionaries from a JSON file. Returns [] if not found."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  [✘] Failed to load {filename}: {e}")
        return []