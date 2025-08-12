



"""
Security Scanner

Comprehensive security scanning tools for the AI BackLog Assistant.
"""

import os
import re
import json
import time
import importlib
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import inspect
import pkgutil
import subprocess
import sys

@dataclass
class SecurityFinding:
    """Security finding/issue"""
    category: str
    severity: str  # 'critical', 'high', 'medium', 'low', 'info'
    description: str
    location: str
    details: Optional[dict] = None
    recommendation: Optional[str] = None

class SecurityScanner:
    """
    Security scanner for analyzing the codebase and dependencies.

    Features:
    - API endpoint analysis
    - Authentication/authorization checks
    - Input validation verification
    - Dependency vulnerability scanning
    - Configuration security checks
    """

    def __init__(self):
        self.findings = []
        self.excluded_paths = ['__pycache__', '.git', 'node_modules']
        self.high_risk_patterns = [
            # SQL injection patterns
            (r"SELECT.*FROM.*WHERE.*\s*=\s*[^']*'[^']*'", "Potential SQL injection"),
            (r"INSERT.*INTO.*VALUES.*\(", "Potential SQL injection"),
            (r"EXEC\(", "Potential SQL execution"),

            # Command injection
            (r"os\.system\(", "Potential command injection"),
            (r"subprocess\.run\(", "Potential command injection"),
            (r"subprocess\.Popen\(", "Potential command injection"),

            # Path traversal
            (r"open\(", "Potential file path traversal"),
            (r"__import__\(", "Potential dynamic import"),

            # Hardcoded secrets
            (r"password\s*=\s*['\"].*['\"]", "Potential hardcoded password"),
            (r"secret\s*=\s*['\"].*['\"]", "Potential hardcoded secret"),
            (r"api_key\s*=\s*['\"].*['\"]", "Potential hardcoded API key"),
        ]

    def _add_finding(self, finding: SecurityFinding):
        """Add a security finding"""
        self.findings.append(finding)

    def scan_api_endpoints(self, api_module_path: str) -> List[SecurityFinding]:
        """Scan API endpoints for security issues"""
        findings = []

        try:
            # Import the API module
            api_module = importlib.import_module(api_module_path)

            # Find all route handlers
            for attr_name in dir(api_module):
                attr = getattr(api_module, attr_name)
                if callable(attr) and hasattr(attr, '__code__'):
                    # Check for common security issues
                    source_code = inspect.getsource(attr)

                    # Check for missing authentication
                    if not re.search(r'@auth_required|@login_required|@jwt_required', source_code):
                        findings.append(SecurityFinding(
                            category="Authentication",
                            severity="medium",
                            description="API endpoint may be missing authentication",
                            location=f"{api_module_path}.{attr_name}",
                            recommendation="Add proper authentication decorator"
                        ))

                    # Check for missing input validation
                    if not re.search(r'validate|sanitize|schema', source_code, re.IGNORECASE):
                        findings.append(SecurityFinding(
                            category="Input Validation",
                            severity="medium",
                            description="API endpoint may be missing input validation",
                            location=f"{api_module_path}.{attr_name}",
                            recommendation="Add input validation and sanitization"
                        ))

                    # Check for sensitive data exposure
                    if re.search(r'password|secret|api_key|token', source_code, re.IGNORECASE):
                        findings.append(SecurityFinding(
                            category="Data Exposure",
                            severity="high",
                            description="API endpoint may expose sensitive data",
                            location=f"{api_module_path}.{attr_name}",
                            recommendation="Review data returned by endpoint"
                        ))

        except Exception as e:
            findings.append(SecurityFinding(
                category="Scanner Error",
                severity="low",
                description=f"Error scanning API module: {str(e)}",
                location=api_module_path
            ))

        return findings

    def scan_auth_implementation(self, auth_module_path: str) -> List[SecurityFinding]:
        """Scan authentication implementation"""
        findings = []

        try:
            auth_module = importlib.import_module(auth_module_path)

            # Check for common authentication issues
            for attr_name in dir(auth_module):
                attr = getattr(auth_module, attr_name)
                if callable(attr) and hasattr(attr, '__code__'):
                    source_code = inspect.getsource(attr)

                    # Check for weak password handling
                    if re.search(r'password', source_code, re.IGNORECASE):
                        if not re.search(r'hash|encrypt|bcrypt', source_code, re.IGNORECASE):
                            findings.append(SecurityFinding(
                                category="Authentication",
                                severity="high",
                                description="Password may be stored or handled insecurely",
                                location=f"{auth_module_path}.{attr_name}",
                                recommendation="Use proper password hashing (bcrypt, etc.)"
                            ))

                    # Check for JWT issues
                    if re.search(r'jwt|token', source_code, re.IGNORECASE):
                        if not re.search(r'expires|expiration', source_code, re.IGNORECASE):
                            findings.append(SecurityFinding(
                                category="Authentication",
                                severity="medium",
                                description="JWT may be missing expiration",
                                location=f"{auth_module_path}.{attr_name}",
                                recommendation="Add token expiration"
                            ))

        except Exception as e:
            findings.append(SecurityFinding(
                category="Scanner Error",
                severity="low",
                description=f"Error scanning auth module: {str(e)}",
                location=auth_module_path
            ))

        return findings

    def scan_codebase_for_patterns(self, base_path: str) -> List[SecurityFinding]:
        """Scan codebase for security patterns"""
        findings = []

        for root, dirs, files in os.walk(base_path):
            # Skip excluded paths
            dirs[:] = [d for d in dirs if d not in self.excluded_paths]

            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Check for high-risk patterns
                        for pattern, description in self.high_risk_patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                findings.append(SecurityFinding(
                                    category="Code Pattern",
                                    severity="high",
                                    description=description,
                                    location=file_path,
                                    details={"pattern": pattern}
                                ))

                        # Check for logging of sensitive data
                        if re.search(r'logging.*password|log.*secret', content, re.IGNORECASE):
                            findings.append(SecurityFinding(
                                category="Logging",
                                severity="medium",
                                description="Potential logging of sensitive data",
                                location=file_path,
                                recommendation="Remove sensitive data from logs"
                            ))

                    except Exception as e:
                        findings.append(SecurityFinding(
                            category="Scanner Error",
                            severity="low",
                            description=f"Error reading file: {str(e)}",
                            location=file_path
                        ))

        return findings

    def scan_dependencies(self) -> List[SecurityFinding]:
        """Scan dependencies for known vulnerabilities"""
        findings = []

        try:
            # Check for requirements files
            requirements_files = ['requirements.txt', 'pyproject.toml']

            for req_file in requirements_files:
                if os.path.exists(req_file):
                    # Use pip-audit if available
                    try:
                        result = subprocess.run(
                            ['pip-audit', '-r', req_file, '--json'],
                            capture_output=True,
                            text=True,
                            timeout=30
                        )

                        if result.returncode == 0:
                            vulnerabilities = json.loads(result.stdout)
                            for vuln in vulnerabilities:
                                findings.append(SecurityFinding(
                                    category="Dependency",
                                    severity="high",
                                    description=f"Vulnerable dependency: {vuln['package_name']} {vuln['package_version']}",
                                    location=req_file,
                                    details={
                                        "vulnerability_id": vuln.get("vulnerability_id", "N/A"),
                                        "fix_versions": vuln.get("fix_versions", []),
                                        "advisory": vuln.get("advisory", "N/A")
                                    },
                                    recommendation="Update to a secure version"
                                ))

                        else:
                            # pip-audit not available or error
                            findings.append(SecurityFinding(
                                category="Scanner Info",
                                severity="info",
                                description="pip-audit not available, consider installing for dependency scanning",
                                location=req_file
                            ))

                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        # Fallback to basic check
                        with open(req_file, 'r') as f:
                            for line in f:
                                if line.strip() and not line.startswith('#'):
                                    package = line.split('=')[0].strip().lower()
                                    # Basic check for known vulnerable packages
                                    if package in ['requests<2.28.1', 'urllib3<1.26.5']:
                                        findings.append(SecurityFinding(
                                            category="Dependency",
                                            severity="medium",
                                            description=f"Potentially vulnerable dependency: {package}",
                                            location=req_file,
                                            recommendation="Check for updates"
                                        ))

        except Exception as e:
            findings.append(SecurityFinding(
                category="Scanner Error",
                severity="low",
                description=f"Error scanning dependencies: {str(e)}",
                location="dependencies"
            ))

        return findings

    def scan_config_files(self, config_files: List[str]) -> List[SecurityFinding]:
        """Scan configuration files for security issues"""
        findings = []

        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check for hardcoded secrets
                    secret_patterns = [
                        r'password\s*=\s*["\'].*["\']',
                        r'secret\s*=\s*["\'].*["\']',
                        r'api_key\s*=\s*["\'].*["\']',
                        r'token\s*=\s*["\'].*["\']'
                    ]

                    for pattern in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            findings.append(SecurityFinding(
                                category="Configuration",
                                severity="critical",
                                description="Potential hardcoded secret in configuration",
                                location=config_file,
                                recommendation="Use environment variables or secret management"
                            ))

                    # Check for debug mode
                    if re.search(r'debug\s*=\s*True', content, re.IGNORECASE):
                        findings.append(SecurityFinding(
                            category="Configuration",
                            severity="medium",
                            description="Debug mode may be enabled",
                            location=config_file,
                            recommendation="Disable debug mode in production"
                        ))

                except Exception as e:
                    findings.append(SecurityFinding(
                        category="Scanner Error",
                        severity="low",
                        description=f"Error reading config file: {str(e)}",
                        location=config_file
                    ))

        return findings

    def run_full_scan(self, base_path: str = '.') -> Dict[str, Any]:
        """Run a comprehensive security scan"""
        print("Starting comprehensive security scan...")
        self.findings = []

        # Scan API endpoints
        print("  - Scanning API endpoints...")
        api_findings = self.scan_api_endpoints('web_server.api_gateway.document_routes')
        self.findings.extend(api_findings)

        # Scan authentication
        print("  - Scanning authentication...")
        auth_findings = self.scan_auth_implementation('web_server.api_gateway.auth_middleware')
        self.findings.extend(auth_findings)

        # Scan codebase
        print("  - Scanning codebase...")
        code_findings = self.scan_codebase_for_patterns(base_path)
        self.findings.extend(code_findings)

        # Scan dependencies
        print("  - Scanning dependencies...")
        dep_findings = self.scan_dependencies()
        self.findings.extend(dep_findings)

        # Scan config files
        print("  - Scanning configuration files...")
        config_findings = self.scan_config_files(['config.py', 'settings.py', 'config.json'])
        self.findings.extend(config_findings)

        # Generate report
        report = self.generate_report()
        print(f"\nSecurity scan completed. Found {len(self.findings)} findings.")

        return report

    def generate_report(self) -> Dict[str, Any]:
        """Generate security report"""
        # Group findings by severity
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0
        }

        for finding in self.findings:
            severity_counts[finding.severity] += 1

        # Generate summary
        summary = {
            'total_findings': len(self.findings),
            'by_severity': severity_counts,
            'categories': {}
        }

        # Group by category
        for finding in self.findings:
            if finding.category not in summary['categories']:
                summary['categories'][finding.category] = 0
            summary['categories'][finding.category] += 1

        return {
            'summary': summary,
            'findings': [vars(f) for f in self.findings],
            'timestamp': time.time()
        }

    def save_report(self, filename: str = 'security_report.json'):
        """Save security report to file"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Security report saved to: {filename}")

    def print_summary(self):
        """Print security findings summary"""
        report = self.generate_report()

        print("\n" + "="*80)
        print("SECURITY SCAN SUMMARY")
        print("="*80)
        print(f"Total Findings: {report['summary']['total_findings']}")
        print("\nBy Severity:")
        for severity, count in report['summary']['by_severity'].items():
            print(f"  {severity.upper()}: {count}")

        print("\nBy Category:")
        for category, count in report['summary']['categories'].items():
            print(f"  {category}: {count}")

        print("\n" + "="*80)
        print("DETAILED FINDINGS:")
        print("="*80)

        for i, finding in enumerate(self.findings, 1):
            print(f"\n{i}. {finding.category} - {finding.severity.upper()}")
            print(f"   Location: {finding.location}")
            print(f"   Description: {finding.description}")
            if finding.recommendation:
                print(f"   Recommendation: {finding.recommendation}")

        print("\n" + "="*80)

# Example usage
if __name__ == "__main__":
    scanner = SecurityScanner()
    report = scanner.run_full_scan()

    # Print summary
    scanner.print_summary()

    # Save report
    scanner.save_report()




