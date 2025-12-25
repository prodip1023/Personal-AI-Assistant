import json
import os
from typing import List, Dict


class Memory:
    def __init__(self, file_path: str = "data/memory.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if not os.path.exists(self.file_path):
            self._write([])

    def _write(self, data: List[Dict]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_history(self) -> List[Dict]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def add(self, role: str, message: str):
        history = self.get_history()
        history.append({"role": role, "message": message})
        self._write(history)

    def clear(self):
        self._write([])