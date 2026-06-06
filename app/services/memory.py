import json
import os
import tempfile

FILE = "data/conversations.json"


def load_memory():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_memory(data):
    """Атомарная запись: пишем во временный файл и заменяем им основной,
    чтобы при сбое не потерять историю и не оставить битый JSON."""
    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    dir_name = os.path.dirname(FILE) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, FILE)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise