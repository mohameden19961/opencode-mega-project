import time
from codeguard.utils.timer import Timer


class TestTimer:
    def test_start_stop(self):
        timer = Timer()
        timer.start()
        time.sleep(0.01)
        timer.stop()
        elapsed = timer.elapsed()
        assert elapsed >= 0.01

    def test_context_manager(self):
        with Timer() as timer:
            time.sleep(0.01)
        assert timer.elapsed() >= 0.01
