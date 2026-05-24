import sys
import click
from codeguard.config import load_config, Config
from codeguard.core.engine import AnalysisEngine
from codeguard.core.reporter import ReportGenerator
from codeguard.output.terminal_writer import TerminalWriter
from codeguard.output.json_writer import JSONWriter
from codeguard.output.html_writer import HTMLWriter
from codeguard.output.markdown_writer import MarkdownWriter
from codeguard.exceptions import CodeGuardError
from codeguard.version import VERSION


@click.group()
@click.version_option(VERSION, "--version", "-V")
@click.option("--config", "-c", default=None, help="Path to configuration file")
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    try:
        ctx.obj["config"] = load_config(config)
    except Exception as e:
        click.echo(f"Error loading config: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("paths", nargs=-1, required=True)
@click.option("--format", "-f", "output_format", default="terminal",
              type=click.Choice(["terminal", "json", "html", "markdown"]))
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--checks", "-C", default=None, help="Comma-separated checks to run")
@click.option("--severity", "-s", default=None,
              type=click.Choice(["low", "medium", "high", "critical"]))
@click.option("--verbose", "-v", is_flag=True, default=False)
@click.option("--no-cache", is_flag=True, default=False)
@click.pass_context
def analyze(ctx, paths, output_format, output, checks, severity, verbose, no_cache):
    config = ctx.obj["config"]
    if checks:
        config.checks_enabled = checks.split(",")
    if severity:
        config.severity_threshold = severity
    config.verbose = verbose
    config.use_cache = not no_cache
    engine = AnalysisEngine(config=config)
    try:
        results = engine.run(list(paths))
        writer = _get_writer(output_format, output, config)
        writer.write(results)
    except CodeGuardError as e:
        click.echo(f"Analysis failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("paths", nargs=-1, required=True)
@click.option("--checks", "-C", default=None)
@click.option("--severity", "-s", default=None)
@click.pass_context
def check(ctx, paths, checks, severity):
    config = ctx.obj["config"]
    if checks:
        config.checks_enabled = checks.split(",")
    if severity:
        config.severity_threshold = severity
    engine = AnalysisEngine(config=config)
    results = engine.run(list(paths))
    violations = results.get_violations(config.severity_threshold or "low")
    writer = TerminalWriter(config=config)
    writer.write_violations(violations)
    if violations:
        sys.exit(1)


@cli.command()
@click.option("--format", "-f", "output_format", default="html",
              type=click.Choice(["html", "markdown", "json"]))
@click.option("--output", "-o", default="codeguard_report")
@click.pass_context
def report(ctx, output_format, output):
    config = ctx.obj["config"]
    generator = ReportGenerator(config=config)
    generator.generate(output_format=output_format, output_dir=output)


@cli.command()
@click.option("--output", "-o", default=".codeguard.yml")
@click.pass_context
def init(ctx, output):
    config = Config.default()
    config.save(output)
    click.echo(f"Created default configuration at {output}")


def _get_writer(output_format, output, config):
    writers = {
        "terminal": TerminalWriter,
        "json": JSONWriter,
        "html": HTMLWriter,
        "markdown": MarkdownWriter,
    }
    writer_cls = writers.get(output_format, TerminalWriter)
    return writer_cls(output_path=output, config=config)




@cli.command()
@click.argument("paths", nargs=-1, required=True)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--fixers", "-F", default=None)
@click.pass_context
def fix(ctx, paths, dry_run, fixers):
    """Auto-fix common issues in code."""
    from codeguard.fixers.whitespace import TrailingWhitespaceFixer
    from codeguard.fixers.lines import LineEndingFixer
    config = ctx.obj["config"]
    available = {"trailing_whitespace": TrailingWhitespaceFixer(config), "line_endings": LineEndingFixer(config)}
    active = {k: v for k, v in available.items() if not fixers or k in fixers.split(",")}
    from codeguard.core.collector import FileCollector
    files = FileCollector(config).collect(list(paths))
    total = 0
    for fp in files:
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        lines = content.split("\n")
        for name, fixer in active.items():
            result = fixer.fix(fp, content, lines)
            if result.fixed:
                label = "[DRY-RUN]" if dry_run else "[FIXED]"
                click.echo(f"{label} {fp}: {result.description}")
                total += result.changes_made
    click.echo(f"{'Would fix' if dry_run else 'Fixed'} {total} issues")

def main():
    cli()
