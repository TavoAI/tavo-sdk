#!/usr/bin/env python3
"""Tavo AI Security Scanner - Standalone binary for local security scanning."""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import tempfile
import subprocess
import yaml


class ScannerError(Exception):
    """Scanner-specific errors."""

    pass


class RuleManager:
    """Manages rule bundles for local scanning."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path.home() / ".tavoai" / "rules"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.bundles: Dict[str, Dict[str, Any]] = {}

    def download_bundle(self, bundle_name: str) -> Dict[str, Any]:
        """Download a rule bundle from the repository."""
        # For now, look locally in the workspace
        bundle_dir = self._find_bundle_locally(bundle_name)
        if bundle_dir:
            return self._load_bundle_from_directory(bundle_dir)

        raise ScannerError(f"Bundle '{bundle_name}' not found")

    def _find_bundle_locally(self, bundle_name: str) -> Optional[Path]:
        """Find bundle in local workspace."""
        current_dir = Path.cwd()
        workspace_root = current_dir

        while workspace_root != workspace_root.parent:
            tavo_rules = workspace_root / "tavo-rules" / "bundles" / bundle_name
            if tavo_rules.exists():
                return tavo_rules
            workspace_root = workspace_root.parent
        return None

    def _load_bundle_from_directory(self, bundle_dir: Path) -> Dict[str, Any]:
        """Load bundle from local directory."""
        index_file = bundle_dir / "index.json"
        if not index_file.exists():
            raise ScannerError(f"Bundle index not found: {index_file}")

        with open(index_file, "r", encoding="utf-8") as f:
            index_data = json.load(f)

        # Load all YAML rule files
        rules = []
        for rule_file in bundle_dir.glob("*.yaml"):
            try:
                with open(rule_file, "r", encoding="utf-8") as f:
                    yaml_data = yaml.safe_load(f)
                    if (
                        yaml_data
                        and isinstance(yaml_data, dict)
                        and "rules" in yaml_data
                    ):
                        rules.extend(yaml_data["rules"])
            except Exception as e:
                print(
                    f"Warning: Failed to load rules from {rule_file}: {e}",
                    file=sys.stderr,
                )

        return {
            "name": index_data["name"],
            "version": index_data["version"],
            "description": index_data["description"],
            "rules": rules,
            "categories": index_data.get("categories", {}),
        }


class OpenGrepEngine:
    """OpenGrep pattern matching engine wrapper."""

    def __init__(self, opengrep_path: Optional[str] = None):
        if opengrep_path is None:
            bundled_path = self._find_bundled_engine()
            self.opengrep_path = bundled_path or "opengrep"
        else:
            self.opengrep_path = opengrep_path
        self._check_opengrep()

    def _find_bundled_engine(self) -> Optional[str]:
        """Find bundled OpenGrep engine."""
        # Look relative to the binary/script location
        script_dir = Path(__file__).parent
        engines_dir = script_dir / "engines"

        candidates = ["opengrep-core", "opengrep-core.exe", "opengrep"]
        for candidate in candidates:
            path = engines_dir / candidate
            if path.is_file():
                return str(path)
        return None

    def _check_opengrep(self):
        """Check if OpenGrep is available."""
        try:
            result = subprocess.run(
                [self.opengrep_path, "-version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                raise ScannerError("OpenGrep not found or not working")
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ScannerError(
                "OpenGrep executable not found. Please install OpenGrep."
            )

    def scan_file(
        self, file_path: Path, rules: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Scan a file using OpenGrep rules."""
        if not file_path.exists():
            return []

        findings = []

        # Create temporary rule file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump({"rules": rules}, f)
            rule_file = f.name

        try:
            # Run OpenGrep with -lang for single file
            cmd = [
                self.opengrep_path,
                "-rules",
                rule_file,
                "-lang",
                "python",
                "-json",
                str(file_path),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode in [0, 1]:  # 0 = no matches, 1 = matches found
                if result.stdout:
                    try:
                        # OpenGrep sometimes outputs extra text before JSON, find the JSON start
                        stdout = result.stdout.strip()
                        json_start = stdout.find("{")
                        if json_start >= 0:
                            json_str = stdout[json_start:]
                            output = json.loads(json_str)
                            raw_results = output.get("results", [])
                            # Transform OpenGrep results to standardized format
                            findings = []
                            for result in raw_results:
                                finding = {
                                    "rule_id": result.get("check_id"),
                                    "message": result.get("extra", {}).get("message"),
                                    "path": result.get("path"),
                                    "start_line": result.get("start", {}).get("line"),
                                    "end_line": result.get("end", {}).get("line"),
                                    "start_col": result.get("start", {}).get("col"),
                                    "end_col": result.get("end", {}).get("col"),
                                    "severity": result.get("extra", {})
                                    .get("metadata", {})
                                    .get("severity", "UNKNOWN"),
                                    "category": result.get("extra", {})
                                    .get("metadata", {})
                                    .get("category"),
                                    "cwe": result.get("extra", {})
                                    .get("metadata", {})
                                    .get("cwe"),
                                    "metadata": result.get("extra", {}).get(
                                        "metadata", {}
                                    ),
                                }
                                findings.append(finding)
                        else:
                            findings = []
                    except json.JSONDecodeError:
                        print(
                            f"Warning: Failed to parse OpenGrep output: {result.stdout}",
                            file=sys.stderr,
                        )

        except subprocess.TimeoutExpired:
            print(f"Warning: OpenGrep scan timed out for {file_path}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: OpenGrep scan failed: {e}", file=sys.stderr)
        finally:
            # Clean up temporary file
            Path(rule_file).unlink(missing_ok=True)

        return findings

    def scan_directory(
        self,
        dir_path: Path,
        rules: List[Dict[str, Any]],
        extensions: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Scan a directory using OpenGrep rules."""
        if not dir_path.exists():
            return []

        all_findings = []

        for file_path in self._find_files(dir_path, extensions):
            findings = self.scan_file(file_path, rules)
            all_findings.extend(findings)

        return all_findings

    def _find_files(
        self, dir_path: Path, extensions: Optional[List[str]] = None
    ) -> List[Path]:
        """Find files to scan."""
        files = []

        def traverse(current_path: Path):
            if not current_path.exists() or not current_path.is_dir():
                return

            try:
                for item in current_path.iterdir():
                    if item.is_file() and self._should_scan_file(item, extensions):
                        files.append(item)
                    elif item.is_dir() and not item.name.startswith("."):
                        traverse(item)
            except PermissionError:
                pass  # Skip directories we can't read

        traverse(dir_path)
        return files

    def _should_scan_file(
        self, file_path: Path, extensions: Optional[List[str]]
    ) -> bool:
        """Check if file should be scanned."""
        if extensions and not any(file_path.name.endswith(ext) for ext in extensions):
            return False
        return not self._is_binary_file(file_path)

    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if file is binary."""
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                if b"\0" in chunk:
                    return True
                # Check for high ratio of non-text characters
                text_chars = bytearray(range(32, 127)) + b"\n\r\t\f\b"
                non_text = sum(1 for byte in chunk if byte not in text_chars)
                return non_text / len(chunk) > 0.3
        except Exception:
            return True
        return False


class SecurityScanner:
    """Unified security scanner using OpenGrep."""

    def __init__(self, rule_manager: RuleManager):
        self.rule_manager = rule_manager
        self.opengrep = OpenGrepEngine()

    def scan_codebase(
        self, path: str, bundle_name: str = "llm-security"
    ) -> Dict[str, Any]:
        """Scan a codebase for security issues."""
        import time

        start_time = time.time()

        path_obj = Path(path)
        bundle = self.rule_manager.download_bundle(bundle_name)

        findings = []

        # Scan with OpenGrep rules
        opengrep_rules = [rule for rule in bundle["rules"] if "pattern" in rule]

        if opengrep_rules:
            if path_obj.is_file():
                findings.extend(self.opengrep.scan_file(path_obj, opengrep_rules))
            else:
                findings.extend(self.opengrep.scan_directory(path_obj, opengrep_rules))

        scan_time = time.time() - start_time

        return {
            "vulnerabilities": findings,
            "passed": len(findings) == 0,
            "scan_time": scan_time,
            "bundle": bundle["name"],
            "rules_used": len(opengrep_rules),
        }


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Tavo AI Security Scanner - Local security scanning with OpenGrep"
    )
    parser.add_argument("path", help="Path to file or directory to scan")
    parser.add_argument(
        "--bundle",
        "-b",
        default="llm-security",
        help="Rule bundle to use (default: llm-security)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    try:
        # Initialize scanner
        rule_manager = RuleManager()
        scanner = SecurityScanner(rule_manager)

        if args.verbose:
            print(
                f"Scanning {args.path} with bundle '{args.bundle}'...", file=sys.stderr
            )

        # Perform scan
        result = scanner.scan_codebase(args.path, args.bundle)

        # Output results
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"Scan Results for {args.path}")
            print(f"Bundle: {result['bundle']}")
            print(f"Rules Used: {result['rules_used']}")
            print(f"Scan Time: {result['scan_time']:.2f}s")
            print(f"Vulnerabilities Found: {len(result['vulnerabilities'])}")
            print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}")

            if result["vulnerabilities"]:
                print("\nVulnerabilities:")
                for vuln in result["vulnerabilities"]:
                    print(
                        f"  - {vuln.get('check_id', 'Unknown')}: {vuln.get('message', 'No message')}"
                    )

        # Exit with appropriate code
        sys.exit(0 if result["passed"] else 1)

    except ScannerError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
