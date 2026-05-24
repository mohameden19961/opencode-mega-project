import statistics
from typing import List, Dict, Any
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults

class StatsUtils:
    @staticmethod
    def compute_stats(results: AnalysisResults) -> Dict[str, Any]:
        severities = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for v in results.violations:
            severities[v.severity] = severities.get(v.severity, 0) + 1
        check_counts = {}

    @staticmethod
    def get_summary(results: AnalysisResults) -> str:
        total = len(results.violations)
        sev = results.count_by_severity()
        return f"Found {total} violations ({sev.get('critical',0)} critical, {sev.get('high',0)} high, {sev.get('medium',0)} medium, {sev.get('low',0)} low)"
