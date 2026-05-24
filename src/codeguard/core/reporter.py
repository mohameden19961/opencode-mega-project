import os
import json
from datetime import datetime
from typing import Optional
from codeguard.config import Config
from codeguard.output.json_writer import JSONWriter
from codeguard.output.html_writer import HTMLWriter
from codeguard.output.markdown_writer import MarkdownWriter


class ReportGenerator:
    def __init__(self, config: Config):
        self.config = config

    def generate(self, output_format: str = "html", output_dir: str = "codeguard_report"):
        os.makedirs(output_dir, exist_ok=True)
        writers = {
            "html": HTMLWriter,
            "markdown": MarkdownWriter,
            "json": JSONWriter,
        }
        writer_cls = writers.get(output_format)
        if writer_cls is None:
            raise ValueError(f"Unsupported format: {output_format}")
        writer = writer_cls(output_path=os.path.join(output_dir, f"report.{output_format}"), config=self.config)
        return writer
