# Changelog

All notable changes to CodeGuard are documented here.

## [0.2.0] — 2026-05-24

### Added
- Plugin system with directory discovery (`~/.codeguard/plugins/`)
- Example plugin for TODO/FIXME detection
- Plugin development documentation
- Interactive HTML dashboard with Chart.js charts
- DashboardWriter output format
- Incremental file scanner for large codebases
- SARIF 2.1.0 output format for GitHub Code Scanning
- Pre-commit hook configuration (`.pre-commit-hooks.yaml`)
- Pre-commit hook shell script
- JSON Schema config validation
- GitHub Action composite action with SARIF upload
- GitHub Actions workflow
- Auto-fix capability for trailing whitespace
- Line ending normalizer (CRLF → LF)
- `fix` CLI command with dry-run mode
- BaseFixer abstract class and FixResult dataclass
- Binary file detection during collection
- LRU eviction policy in cache module
- Memory cache layer with access tracking
- Cache statistics reporting
- IFileReader and ICheckRunner interfaces
- Dependency injection in AnalysisEngine
- 60+ test files across all modules
- Configuration edge case tests

### Changed
- FileCollector now skips binary files automatically
- Config parser handles empty YAML gracefully
- AnalysisEngine uses incremental scanner when cache enabled
- Output module supports dashboard and SARIF formats
- Cache module bounded by max_size with LRU eviction

### Fixed
- Config parser crash with empty YAML values
- UnicodeDecodeError on binary file analysis
- Unbounded memory growth in cache module
- Various edge cases in AST parsing

### Documentation
- Plugin development guide
- Pre-commit integration guide
- GitHub Actions integration guide
- JSON Schema reference

## [0.1.0] — 2026-05-24

### Added
- Initial project structure
- Core analysis engine with parallel execution
- 9 check modules (complexity, style, security, performance, documentation, naming, imports, duplication, typing)
- 4 output formats (terminal, JSON, HTML, Markdown)
- Configuration system with YAML support
- CLI with Click (analyze, check, report, init commands)
- Utility modules (cache, parallel, timer, logger, fs, ast_utils, git_utils)
- 25 test files
- Comprehensive documentation
- Makefile for development tasks
