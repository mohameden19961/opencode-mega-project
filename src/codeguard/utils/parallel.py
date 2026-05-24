from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, TypeVar, Iterator

T = TypeVar("T")
R = TypeVar("R")


class ParallelExecutor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def map(self, func: Callable[[T], R], items: List[T]) -> List[R]:
        if len(items) <= 1:
            return [func(item) for item in items]
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(func, item): item for item in items}
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append(None)
        return results

    def map_ordered(self, func: Callable[[T], R], items: List[T]) -> List[R]:
        if len(items) <= 1:
            return [func(item) for item in items]
        results = [None] * len(items)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(func, item): i for i, item in enumerate(items)}
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    results[idx] = future.result()
                except Exception:
                    results[idx] = None
        return results
