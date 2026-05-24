import os
import sys
import json
from typing import List, Dict, Optional


class DataProcessor:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.data: List[Dict] = []

    def load_from_file(self, path: str) -> bool:
        if not os.path.exists(path):
            return False
        try:
            with open(path) as f:
                self.data = json.load(f)
            return True
        except (json.JSONDecodeError, IOError):
            return False

    def process_all(self):
        results = []
        for item in self.data:
            if item.get("active"):
                if item.get("type") == "a":
                    for sub in item.get("sub_items", []):
                        if sub.get("valid"):
                            result = self._process_type_a(sub)
                            results.append(result)
                elif item.get("type") == "b":
                    result = self._process_type_b(item)
                    results.append(result)
        return results

    def _process_type_a(self, item: Dict) -> Dict:
        return {
            "id": item.get("id"),
            "value": item.get("value", 0) * 2,
            "category": "a_processed",
        }

    def _process_type_b(self, item: Dict) -> Dict:
        return {
            "id": item.get("id"),
            "value": sum(item.get("values", [])),
            "category": "b_processed",
        }


def main():
    processor = DataProcessor()
    processor.load_from_file("data.json")
    results = processor.process_all()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
