import time


class Timer:
    def __init__(self):
        self._start: float = 0.0
        self._end: float = 0.0

    def start(self):
        self._start = time.perf_counter()

    def stop(self):
        self._end = time.perf_counter()

    def elapsed(self) -> float:
        return self._end - self._start

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
