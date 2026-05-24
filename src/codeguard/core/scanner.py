"""Incremental file scanner for large codebases."""
import os, hashlib, json
from typing import List
from codeguard.config import Config

class IncrementalScanner:
    def __init__(self, config: Config):
        self.config = config
        self.state_file = os.path.join(config.cache_dir, "scanner_state.json")

    def get_changed_files(self, paths: List[str]) -> List[str]:
        state = self._load_state()
        files = self._collect_files(paths)
        changed = []
        for f in files:
            h = self._file_hash(f)
            if f not in state or state[f] != h:
                changed.append(f)
                state[f] = h
        self._save_state(state)
        return changed

    def _collect_files(self, paths):
        from codeguard.core.collector import FileCollector
        return FileCollector(self.config).collect(paths)

    def _file_hash(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file) as f:
                return json.load(f)
        return {}

    def _save_state(self, state):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(state, f)
