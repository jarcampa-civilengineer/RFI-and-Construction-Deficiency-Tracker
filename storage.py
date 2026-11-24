import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "tracker_items.json"

def load_items():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_items(items):
    DATA_DIR.mkdir(exist_ok=True)
    temp_file = DATA_FILE.with_suffix(".tmp")
    with temp_file.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)
    temp_file.replace(DATA_FILE)
