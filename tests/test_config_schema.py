from codeguard.config_schema import validate_config

class TestConfigSchema:
    def test_valid(self):
        assert len(validate_config({"verbose": True})) == 0
    def test_invalid_type(self):
        assert len(validate_config({"verbose": "bad"})) > 0
    def test_unknown_key(self):
        assert len(validate_config({"unknown": "x"})) > 0
    def test_enum(self):
        assert len(validate_config({"severity_threshold": "bad"})) > 0
    def test_minimum(self):
        assert len(validate_config({"max_workers": 0})) > 0
