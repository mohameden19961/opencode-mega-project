import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional
from dataclasses import dataclass, field
from codeguard.config import Config
from codeguard.core.collector import FileCollector
from codeguard.checks.base import CheckRegistry
from codeguard.checks.complexity import ComplexityCheck
from codeguard.checks.style import StyleCheck
from codeguard.checks.security import SecurityCheck
from codeguard.checks.performance import PerformanceCheck
from codeguard.checks.documentation import DocumentationCheck
from codeguard.checks.naming import NamingCheck
from codeguard.checks.imports import ImportCheck
from codeguard.checks.duplication import DuplicationCheck
from codeguard.checks.typing import TypingCheck
from codeguard.checks.encoding import EncodingCheck
from codeguard.checks.error_handling import ErrorHandlingCheck
from codeguard.checks.logging import LoggingCheck
from codeguard.checks.concurrency import ConcurrencyCheck
from codeguard.checks.api_design import APIDesignCheck
from codeguard.checks.testing import TestingCheck
from codeguard.checks.dependencies import DependencyCheck
from codeguard.checks.best_practices import best_practices
from codeguard.checks.maintainability import maintainability









from codeguard.utils.cache import AnalysisCache
from codeguard.utils.timer import Timer
from codeguard.core.scanner import IncrementalScanner
from codeguard.utils.log import Logger
from codeguard.utils.parallel import ParallelExecutor
from codeguard.exceptions import AnalysisError


@dataclass
class Violation:
    check_name: str
    severity: str
    message: str
    file_path: str
    line_number: int = 0
    column: int = 0
    suggestion: Optional[str] = None


@dataclass
class AnalysisResults:
    violations: List[Violation] = field(default_factory=list)
    files_analyzed: int = 0
    total_lines: int = 0
    duration: float = 0.0
    errors: List[str] = field(default_factory=list)

    def get_violations(self, min_severity: str = "low") -> List[Violation]:
        severity_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        threshold = severity_order.get(min_severity, 0)
        return [
            v for v in self.violations
            if severity_order.get(v.severity, 0) >= threshold
        ]

    def count_by_severity(self) -> dict:
        counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for v in self.violations:
            if v.severity in counts:
                counts[v.severity] += 1
        return counts

    def count_by_check(self) -> dict:
        counts = {}
        for v in self.violations:
            counts[v.check_name] = counts.get(v.check_name, 0) + 1
        return counts


from abc import ABC, abstractmethod

class IFileReader(ABC):
    @abstractmethod
    def read_file(self, path: str) -> str:
        pass

class ICheckRunner(ABC):
    @abstractmethod
    def run_checks(self, file_path: str, content: str, lines: list) -> list:
        pass

class FileReader(IFileReader):
    def read_file(self, path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

class CheckRunner(ICheckRunner):
    def __init__(self, config, checks):
        self.config = config
        self.checks = checks
    def run_checks(self, file_path, content, lines):
        violations = []
        for check in self.checks:
            try:
                inst = check(config=self.config)
                violations.extend(inst.check(file_path, content, lines))
            except Exception:
                pass
        return violations

class AnalysisEngine:
    def __init__(self, config: Config, file_reader: IFileReader = None, check_runner: ICheckRunner = None):
        self.config = config
        self.logger = Logger(verbose=config.verbose)
        self.cache = AnalysisCache(config.cache_dir) if config.use_cache else None
        self.collector = FileCollector(config)
        self.file_reader = file_reader or FileReader()
        self.check_runner = check_runner
        self._register_checks()

    def _register_checks(self):
        CheckRegistry.register(ComplexityCheck)
        CheckRegistry.register(maintainability)
        CheckRegistry.register(best_practices)
        CheckRegistry.register(DependencyCheck)
        CheckRegistry.register(TestingCheck)
        CheckRegistry.register(APIDesignCheck)
        CheckRegistry.register(ConcurrencyCheck)
        CheckRegistry.register(LoggingCheck)
        CheckRegistry.register(ErrorHandlingCheck)
        CheckRegistry.register(EncodingCheck)
        CheckRegistry.register(StyleCheck)
        CheckRegistry.register(SecurityCheck)
        CheckRegistry.register(PerformanceCheck)
        CheckRegistry.register(DocumentationCheck)
        CheckRegistry.register(NamingCheck)
        CheckRegistry.register(ImportCheck)
        CheckRegistry.register(DuplicationCheck)
        CheckRegistry.register(TypingCheck)

    def run(self, paths: List[str]) -> AnalysisResults:
        timer = Timer()
        timer.start()
        results = AnalysisResults()
        if self.config.use_cache:
            scanner = IncrementalScanner(self.config)
            files = scanner.get_changed_files(paths)
        else:
            files = self.collector.collect(paths)
        results.files_analyzed = len(files)
        if not files:
            self.logger.warning("No files found to analyze")
            timer.stop()
            results.duration = timer.elapsed()
            return results

        checks = CheckRegistry.get_enabled(self.config.checks_enabled)
        self.logger.info(f"Running {len(checks)} checks on {len(files)} files")

        executor = ParallelExecutor(max_workers=self.config.max_workers)

        def analyze_file(file_path):
            file_violations = []
            try:
                content = self.file_reader.read_file(file_path)
                lines = content.split("\n")
                results.total_lines += len(lines)
                cached = self.cache and self.cache.get(file_path)
                if cached and cached["hash"] == hash(content):
                    self.logger.debug(f"Cache hit: {file_path}")
                    return cached["violations"]
                for check in checks:
                    try:
                        check_instance = check(config=self.config)
                        violations = check_instance.check(file_path, content, lines)
                        file_violations.extend(violations)
                    except Exception as e:
                        self.logger.error(f"Check {check.__name__} failed on {file_path}: {e}")
                        results.errors.append(f"{check.__name__}:{file_path}: {e}")
                if self.cache:
                    self.cache.set(file_path, hash(content), file_violations)
            except Exception as e:
                self.logger.error(f"Error analyzing {file_path}: {e}")
                results.errors.append(f"Error:{file_path}: {e}")
            return file_violations

        file_results = executor.map(analyze_file, files)
        for file_violations in file_results:
            results.violations.extend(file_violations)

        timer.stop()
        results.duration = timer.elapsed()
        self.logger.info(
            f"Analysis complete: {len(results.violations)} violations "
            f"in {results.files_analyzed} files ({results.duration:.2f}s)"
        )
        return results


def analyze(paths: List[str], config: Optional[Config] = None) -> AnalysisResults:
    if config is None:
        config = Config.default()
    engine = AnalysisEngine(config=config)
    return engine.run(paths)
