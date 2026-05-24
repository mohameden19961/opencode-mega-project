import sys
from datetime import datetime
from typing import Optional


class Logger:
    def __init__(self, verbose: bool = False, output: Optional[str] = None):
        self.verbose = verbose
        self.output = output

    def info(self, message: str):
        self._log("INFO", message)

    def debug(self, message: str):
        if self.verbose:
            self._log("DEBUG", message)

    def warning(self, message: str):
        self._log("WARN", message)

    def error(self, message: str):
        self._log("ERROR", message)

    def _log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] [{level}] {message}"
        if self.output:
            with open(self.output, "a") as f:
                f.write(formatted + "\n")
        else:
            print(formatted, file=sys.stderr)
