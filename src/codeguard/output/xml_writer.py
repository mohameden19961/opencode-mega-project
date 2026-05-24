
import xml.etree.ElementTree as ET
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults

class XMLWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        root = ET.Element("codeguard_report")
        summary = ET.SubElement(root, "summary")
        for attr in ["files_analyzed", "total_lines", "total_violations"]:
            el = ET.SubElement(summary, attr)
            el.text = str(getattr(results, attr, 0))
        violations_el = ET.SubElement(root, "violations")
        for v in results.violations:
            v_el = ET.SubElement(violations_el, "violation")
            for field in ["check_name", "severity", "message", "file_path", "line_number", "suggestion"]:
                el = ET.SubElement(v_el, field)
                el.text = str(getattr(v, field, "") or "")
        xml = ET.tostring(root, encoding="unicode")
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(xml)
        else:
            print(xml)
