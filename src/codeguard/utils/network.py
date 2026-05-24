
import urllib.request
import json
from typing import Optional, Dict, Any
from codeguard.exceptions import CodeGuardError

class NetworkUtils:
    @staticmethod
    def fetch_json(url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            return None

    @staticmethod
    def check_url(url: str, timeout: int = 5) -> bool:
        try:
            with urllib.request.urlopen(url, timeout=timeout):
                return True
        except Exception:
            return False
