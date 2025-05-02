import json
from pathlib import Path
from app.models.library import Library
from typing import Dict
from datetime import datetime

DB_FILE = Path("db_state.json")

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def save_state(libraries: Dict[str, Library]):
    tmp_file = DB_FILE.with_suffix('.json.tmp')
    with open(tmp_file, "w") as f:
        json.dump([lib.model_dump() for lib in libraries.values()], f, cls=CustomEncoder)
    tmp_file.replace(DB_FILE)

def load_state():
    if not DB_FILE.exists():
        return {}
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            for lib in data:
                lib["created_at"] = datetime.fromisoformat(lib["created_at"])
                for doc in lib.get("documents", []):
                    doc["created_at"] = datetime.fromisoformat(doc["created_at"])
                    for chunk in doc.get("chunks", []):
                        chunk["created_at"] = datetime.fromisoformat(chunk["created_at"])
            return {lib["id"]: Library(**lib) for lib in data}
    except json.JSONDecodeError as e:
        print("Failed to decode JSON from %s: %s", DB_FILE, e, exc_info=True)
        return {}
