from codeguard.utils.parallel import ParallelExecutor


class TestParallelExecutor:
    def test_map(self):
        executor = ParallelExecutor(max_workers=2)
        results = executor.map(lambda x: x * 2, [1, 2, 3])
        assert results == [2, 4, 6]

    def test_map_ordered(self):
        executor = ParallelExecutor(max_workers=2)
        results = executor.map_ordered(lambda x: x * 2, [3, 1, 2])
        assert results == [6, 2, 4]

    def test_empty(self):
        executor = ParallelExecutor(max_workers=2)
        results = executor.map(lambda x: x, [])
        assert results == []
