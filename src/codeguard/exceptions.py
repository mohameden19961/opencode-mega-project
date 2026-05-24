class CodeGuardError(Exception):
    pass


class ConfigurationError(CodeGuardError):
    pass


class AnalysisError(CodeGuardError):
    pass


class CheckError(CodeGuardError):
    pass


class ReportError(CodeGuardError):
    pass


class CollectorError(CodeGuardError):
    pass


class CacheError(CodeGuardError):
    pass
