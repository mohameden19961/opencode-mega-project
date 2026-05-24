
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
        for v in results.violations:
            check_counts[v.check_name] = check_counts.get(v.check_name, 0) + 1
        return {
            "total": len(results.violations),
            "severities": severities,
            "by_check": check_counts,
            "avg_per_file": len(results.violations) / max(results.files_analyzed, 1),
        }
