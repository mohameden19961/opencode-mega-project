
# VSCode Extension Integration
# Provides language server protocol support

import json
import sys
from codeguard import analyze
from codeguard.config import Config

def handle_lsp_request(request):
    if request["method"] == "textDocument/codeGuard":
        uri = request["params"]["uri"]
        results = analyze([uri], config=Config.default())
        return {"violations": [
            {"line": v.line_number, "message": v.message, "severity": v.severity}
            for v in results.violations
        ]}
    return None
