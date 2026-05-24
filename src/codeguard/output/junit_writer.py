
import xml.etree.ElementTree as ET
from typing import Optional
from codeguard.config import Config
from codeguard.core.engine import AnalysisResults

class JUnitWriter:
    def __init__(self, output_path: Optional[str] = None, config: Optional[Config] = None):
        self.output_path = output_path
        self.config = config or Config.default()

    def write(self, results: AnalysisResults):
        root = ET.Element("testsuites")
        suite = ET.SubElement(root, "testsuite", name="codeguard")
        for v in results.violations:
            case = ET.SubElement(suite, "testcase",
                name=v.check_name,
                classname=v.file_path,
                line=str(v.line_number))
            error = ET.SubElement(case, "error", message=v.message)
            if v.suggestion:
                error.text = v.suggestion
        xml = ET.tostring(root, encoding="unicode")
        if self.output_path:
            with open(self.output_path, "w") as f:
                f.write(xml)
        else:
            print(xml)
