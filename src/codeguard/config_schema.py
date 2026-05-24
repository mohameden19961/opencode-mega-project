"""JSON Schema validation for CodeGuard configuration."""

CODEGUARD_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "CodeGuard Configuration", "type": "object",
    "properties": {
        "verbose": {"type": "boolean", "default": False},
        "use_cache": {"type": "boolean", "default": True},
        "cache_dir": {"type": "string", "default": ".codeguard_cache"},
        "severity_threshold": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "low"},
        "max_workers": {"type": "integer", "minimum": 1, "maximum": 64, "default": 4},
        "timeout": {"type": "integer", "minimum": 1, "default": 60},
        "checks_enabled": {"type": "array", "items": {"type": "string"}},
        "exclude_patterns": {"type": "array", "items": {"type": "string"}},
        "complexity": {"type": "object", "properties": {
            "max_cyclomatic": {"type": "integer", "minimum": 1, "default": 10},
            "max_cognitive": {"type": "integer", "minimum": 1, "default": 15},
            "max_nesting": {"type": "integer", "minimum": 0, "default": 4},
            "max_lines_per_function": {"type": "integer", "minimum": 1, "default": 50},
            "max_parameters": {"type": "integer", "minimum": 1, "default": 6},
        }},
        "style": {"type": "object", "properties": {
            "max_line_length": {"type": "integer", "minimum": 40, "default": 100},
            "indent": {"type": "integer", "enum": [2, 4], "default": 4},
            "trailing_whitespace": {"type": "boolean", "default": False},
        }},
        "security": {"type": "object", "properties": {
            "level": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "high"},
            "check_sql_injection": {"type": "boolean", "default": True},
            "check_path_traversal": {"type": "boolean", "default": True},
            "check_command_injection": {"type": "boolean", "default": True},
        }},
    },
}

def validate_config(data: dict) -> list:
    errors = []
    for key in data:
        if key not in CODEGUARD_SCHEMA["properties"]:
            errors.append(f"Unknown key: '{key}'"); continue
        prop = CODEGUARD_SCHEMA["properties"][key]
        if "type" in prop:
            t = prop["type"]
            if t == "integer" and not isinstance(data[key], int):
                errors.append(f"'{key}' must be integer")
            elif t == "boolean" and not isinstance(data[key], bool):
                errors.append(f"'{key}' must be boolean")
            elif t == "string" and not isinstance(data[key], str):
                errors.append(f"'{key}' must be string")
            elif t == "string" and "enum" in prop and data[key] not in prop["enum"]:
                errors.append(f"'{key}' must be one of {prop['enum']}")
        if isinstance(data[key], (int, float)):
            if "minimum" in prop and data[key] < prop["minimum"]:
                errors.append(f"'{key}' min is {prop['minimum']}")
            if "maximum" in prop and data[key] > prop["maximum"]:
                errors.append(f"'{key}' max is {prop['maximum']}")
    return errors
