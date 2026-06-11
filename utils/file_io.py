import json, os

def save_data(filename, data):
    try:
        json.dump(data, open(filename, "w"), indent=4)
        print(f"  [✔] Saved {filename}")
    except IOError as e:
        print(f"  [✘] Save failed {filename}: {e}")

def load_data(filename):
    if not os.path.exists(filename): return []
    try:
        return json.load(open(filename))
    except (json.JSONDecodeError, IOError) as e:
        print(f"  [✘] Load failed {filename}: {e}"); return []
