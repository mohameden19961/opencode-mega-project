# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.2.x   | ✅ Active |
| 0.1.x   | ❌ No longer supported |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in CodeGuard, please follow these steps:

1. **Do not** open a public issue
2. Send details to **24068@supnum.mr**
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Possible impact
   - Suggested fix (if any)

## What to Expect

- Acknowledgment within 48 hours
- Regular updates on progress
- Credit for the discovery (if desired)

## Scope

Security issues include:
- Code injection via config files
- Path traversal in file collection
- Unsafe deserialization
- Exposure of sensitive information in reports

## Non-Qualifying Issues

- Missing docstrings (covered by documentation checks)
- Code style preferences
- Performance issues not related to security
