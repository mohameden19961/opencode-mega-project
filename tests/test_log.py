from codeguard.utils.log import Logger


class TestLogger:
    def test_info(self, capsys):
        logger = Logger(verbose=False)
        logger.info("test message")
        captured = capsys.readouterr()
        assert "INFO" in captured.err
        assert "test message" in captured.err

    def test_debug_verbose(self, capsys):
        logger = Logger(verbose=True)
        logger.debug("debug message")
        captured = capsys.readouterr()
        assert "DEBUG" in captured.err

    def test_debug_not_verbose(self, capsys):
        logger = Logger(verbose=False)
        logger.debug("debug message")
        captured = capsys.readouterr()
        assert captured.err == ""
