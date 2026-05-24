from codeguard.checks.base import BaseCheck
from codeguard.core.types import Violation
import re
import os
from typing import List


class SSHConfigCheck(BaseCheck):
    name = "ssh_config"
    description = "Check SSH configuration for security issues"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        if not file_path.endswith("/ssh_config") and not file_path.endswith("sshd_config") and not file_path.endswith(".ssh/config"):
            return violations

        vulnerable_settings = {
            "PermitRootLogin yes": ("PermitRootLogin is enabled", "high"),
            "PasswordAuthentication yes": ("Password authentication is enabled, use key-based auth", "high"),
            "PermitEmptyPasswords yes": ("Empty passwords allowed", "critical"),
            "Protocol 1": ("SSH Protocol 1 is insecure", "critical"),
            "UsePAM no": ("PAM disabled, may weaken security", "medium"),
            "X11Forwarding yes": ("X11 forwarding enabled", "medium"),
            "AllowTcpForwarding yes": ("TCP forwarding enabled without restriction", "low"),
            "Compression yes": ("SSH compression may leak data", "low"),
            "LogLevel INFO": ("SSH log level should be VERBOSE", "low"),
        }

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for setting, (msg, sev) in vulnerable_settings.items():
                key, val = setting.split(" ", 1)
                if stripped.startswith(key) and val in stripped:
                    violations.append(Violation(
                        check_name=self.name,
                        severity=sev,
                        message=f"SSH: {msg}",
                        file_path=file_path,
                        line_number=i,
                        suggestion=f"Set '{key} no' in your SSH config"
                    ))

        return violations


class SSHKeyCheck(BaseCheck):
    name = "ssh_keys"
    description = "Check SSH keys for weak algorithms"

    weak_keys = {
        r"-----BEGIN RSA PRIVATE KEY-----": ("RSA key found, consider Ed25519", "medium"),
        r"ssh-rsa AAAA": ("RSA public key, consider Ed25519", "low"),
        r"ssh-dss AAAA": ("DSS (DSA) key is insecure", "critical"),
        r"ecdsa-sha2-nistp256": ("ECDSA with NIST P-256, consider Ed25519", "low"),
    }

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        if not file_path.endswith("id_rsa") and not file_path.endswith("id_ed25519") and not file_path.endswith("authorized_keys"):
            return violations

        for i, line in enumerate(lines, 1):
            for pattern, (msg, sev) in self.weak_keys.items():
                if pattern in line:
                    violations.append(Violation(
                        check_name=self.name,
                        severity=sev,
                        message=f"Key: {msg}",
                        file_path=file_path,
                        line_number=i,
                        suggestion="Generate an Ed25519 key: ssh-keygen -t ed25519"
                    ))
                    break

        return violations


class SSHPortCheck(BaseCheck):
    name = "ssh_port"
    description = "Check for non-standard SSH ports in config"

    def check(self, file_path: str, content: str, lines: List[str]) -> List[Violation]:
        violations = []
        if "ssh" not in file_path and "ssh" not in content.lower():
            return violations

        for i, line in enumerate(lines, 1):
            m = re.match(r"\s*Port\s+(\d+)", line)
            if m and m.group(1) == "22":
                violations.append(Violation(
                    check_name=self.name,
                    severity="low",
                    message="SSH running on default port 22",
                    file_path=file_path,
                    line_number=i,
                    suggestion="Consider using a non-standard port to reduce automated attacks"
                ))
            m2 = re.match(r"\s*HostName\s+\S+", line)
            if m2:
                violations.append(Violation(
                    check_name=self.name,
                    severity="info",
                    message=f"SSH host configured: {line.strip()}",
                    file_path=file_path,
                    line_number=i,
                ))

        return violations
