import os
import yaml
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Any
from codeguard.exceptions import ConfigurationError
from codeguard.config_schema import validate_config


@dataclass
class ComplexityConfig:
    max_cyclomatic: int = 10
    max_cognitive: int = 15
    max_nesting: int = 4
    max_lines_per_function: int = 50
    max_parameters: int = 6
    max_returns: int = 4


@dataclass
class StyleConfig:
    max_line_length: int = 100
    indent: int = 4
    quotes: str = "double"
    trailing_whitespace: bool = False
    blank_lines: bool = True
    max_blank_lines: int = 2


@dataclass
class SecurityConfig:
    level: str = "high"
    exclude_patterns: List[str] = field(default_factory=list)
    dangerous_functions: List[str] = field(default_factory=lambda: [
        "eval", "exec", "compile", "__import__",
        "pickle.loads", "yaml.load", "os.system",
        "subprocess.Popen", "subprocess.call",
    ])
    check_sql_injection: bool = True
    check_path_traversal: bool = True
    check_command_injection: bool = True


@dataclass
class PerformanceConfig:
    max_complexity: int = 10
    check_nested_loops: bool = True
    check_large_allocations: bool = True
    check_slow_imports: bool = True
    max_iterations_warning: int = 10000


@dataclass
class DocumentationConfig:
    require_docstrings: bool = True
    require_type_hints: bool = False
    min_docstring_length: int = 10
    check_public_api: bool = True
    exclude_patterns: List[str] = field(default_factory=lambda: ["__.*__"])


@dataclass
class Config:
    verbose: bool = False
    use_cache: bool = True
    cache_dir: str = ".codeguard_cache"
    severity_threshold: str = "low"
    checks_enabled: List[str] = field(default_factory=lambda: [
        "complexity", "style", "security", "performance",
        "documentation", "naming", "imports", "duplication", "typing",
        "ssh_config", "ssh_keys", "ssh_port",
    ])
    exclude_patterns: List[str] = field(default_factory=lambda: [
        "*.pyc", "__pycache__", ".git", "venv", ".venv",
        "build", "dist", "*.egg-info",
    ])
    complexity: ComplexityConfig = field(default_factory=ComplexityConfig)
    style: StyleConfig = field(default_factory=StyleConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    documentation: DocumentationConfig = field(default_factory=DocumentationConfig)
    max_workers: int = 4
    timeout: int = 60

    @classmethod
    def default(cls):
        return cls()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        config = cls()
        if "verbose" in data:
            config.verbose = data["verbose"]
        if "use_cache" in data:
            config.use_cache = data["use_cache"]
        if "cache_dir" in data:
            config.cache_dir = data["cache_dir"]
        if "severity_threshold" in data:
            config.severity_threshold = data["severity_threshold"]
        if "checks_enabled" in data:
            config.checks_enabled = data["checks_enabled"]
        if "exclude_patterns" in data:
            config.exclude_patterns = data["exclude_patterns"]
        if "complexity" in data:
            for k, v in data["complexity"].items():
                setattr(config.complexity, k, v)
        if "style" in data:
            for k, v in data["style"].items():
                setattr(config.style, k, v)
        if "security" in data:
            for k, v in data["security"].items():
                setattr(config.security, k, v)
        if "performance" in data:
            for k, v in data["performance"].items():
                setattr(config.performance, k, v)
        if "documentation" in data:
            for k, v in data["documentation"].items():
                setattr(config.documentation, k, v)
        if "max_workers" in data:
            config.max_workers = data["max_workers"]
        if "timeout" in data:
            config.timeout = data["timeout"]
        return config

    def save(self, path: str):
        data = asdict(self)
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)


def load_config(path: Optional[str] = None) -> Config:
    if path is None:
        for candidate in [".codeguard.yml", ".codeguard.yaml",
                          "~/.codeguard.yml", "~/.codeguard/config.yml"]:
            expanded = os.path.expanduser(candidate)
            if os.path.exists(expanded):
                path = expanded
                break
    if path and os.path.exists(path):
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
        except (yaml.YAMLError, IOError):
            return Config.default()
        if data is None:
            return Config.default()
        if not isinstance(data, dict):
            return Config.default()
        return Config.from_dict(data)
    default = Config.default()
    return default
