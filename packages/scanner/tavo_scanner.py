#!/usr/bin/env python3
"""Tavo AI Security Scanner - Standalone binary for local security scanning."""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import tempfile
import subprocess
import yaml
import asyncio

# Plugin system imports (optional - graceful degradation if not available)
try:
    from tavo.plugins import (
        PluginRegistry,
        PluginType,
        PluginExecutionContext,
        PluginExecutionResult,
    )
    from tavo.scanner import (
        PluginExecutor,
        ResultAggregator,
        ScannerConfig,
        ScanOptions,
    )

    PLUGIN_SYSTEM_AVAILABLE = True
except ImportError:
    PLUGIN_SYSTEM_AVAILABLE = False

# SDK Integration imports (optional - graceful degradation if not available)
try:
    from .auth_manager import AuthManager
    from .sdk_integration import SDKIntegration, SDKConfig
    from .registry_manager import RegistryManager
    from .code_submitter import CodeSubmitter
    from .remote_scanner import RemoteScanner
    from .websocket_handler import WebSocketHandler
    from .usage_tracker import UsageTracker
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False


class ScannerError(Exception):
    """Scanner-specific errors."""

    pass


# Import new rule system
try:
    from .rules_loader import RulesLoader
    from .hybrid_rule_executor import HybridRuleExecutor
    RULE_SYSTEM_AVAILABLE = True
except ImportError:
    RULE_SYSTEM_AVAILABLE = False


class RuleManager:
    """Legacy rule manager for backward compatibility."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path.home() / ".tavoai" / "rules"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.bundles: Dict[str, Dict[str, Any]] = {}

        # Use new rules loader if available
        self.rules_loader = RulesLoader() if RULE_SYSTEM_AVAILABLE else None

    def download_bundle(self, bundle_name: str) -> Dict[str, Any]:
        """Download a rule bundle from the repository."""
        # For now, look locally in the workspace
        bundle_dir = self._find_bundle_locally(bundle_name)
        if bundle_dir:
            if self.rules_loader:
                return self.rules_loader.load_bundle(bundle_dir)
            else:
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
        """Load bundle from local directory (legacy method)."""
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
    """Unified security scanner using OpenGrep with plugin support."""

    def __init__(self, rule_manager: RuleManager, api_key: Optional[str] = None, sdk_integration: Optional[Any] = None):
        self.rule_manager = rule_manager
        self.opengrep = OpenGrepEngine()
        self.api_key = api_key
        self.sdk_integration = sdk_integration

        # Initialize hybrid rule executor if available
        self.hybrid_executor = None
        if RULE_SYSTEM_AVAILABLE and sdk_integration:
            try:
                self.hybrid_executor = HybridRuleExecutor(sdk_integration)
            except Exception as e:
                print(
                    f"Warning: Failed to initialize hybrid rule executor: {e}", file=sys.stderr
                )
                RULE_SYSTEM_AVAILABLE = False

        # Initialize plugin system if available
        self.plugin_executor = None
        if PLUGIN_SYSTEM_AVAILABLE and api_key:
            try:
                config = ScannerConfig(api_key=api_key)
                self.plugin_executor = PluginExecutor(config)
                self.result_aggregator = ResultAggregator()
            except Exception as e:
                print(
                    f"Warning: Failed to initialize plugin system: {e}", file=sys.stderr
                )
                PLUGIN_SYSTEM_AVAILABLE = False

    def scan_codebase(
        self,
        path: str,
        bundle_name: str = "llm-security",
        static_plugins: Optional[List[str]] = None,
        dynamic_plugins: Optional[List[str]] = None,
        plugin_config: Optional[Dict[str, Any]] = None,
        mode: str = "local"
    ) -> Dict[str, Any]:
        """Scan a codebase for security issues.

        Args:
            path: Path to scan
            bundle_name: Rule bundle to use
            static_plugins: List of static analysis plugin IDs
            dynamic_plugins: List of dynamic testing plugin IDs
            plugin_config: Configuration for plugins
            mode: Scan mode ("local", "remote", "hybrid")
        """
        import time

        start_time = time.time()

        path_obj = Path(path)
        bundle = self.rule_manager.download_bundle(bundle_name)

        findings = []
        plugin_results = []
        hybrid_results = []

        # Use hybrid rule executor if available and in hybrid mode
        if RULE_SYSTEM_AVAILABLE and self.hybrid_executor and mode == "hybrid":
            # Execute hybrid rules
            try:
                # Create code context for scanning
                base_context = {
                    "file_path": str(path_obj),
                    "language": self._detect_language(path_obj.name if path_obj.is_file() else ""),
                    "code_snippet": "",  # Will be filled per file
                    "line_number": 1,
                    "metadata": {
                        "bundle_name": bundle_name,
                        "scan_mode": mode
                    }
                }

                if path_obj.is_file():
                    # Scan single file
                    with open(path_obj, 'r', encoding='utf-8', errors='ignore') as f:
                        code_content = f.read()
                        base_context["code_snippet"] = code_content
                        base_context["file_path"] = str(path_obj)

                    hybrid_results = asyncio.run(
                        self.hybrid_executor.execute_bundle_rules(bundle, base_context)
                    )
                else:
                    # Scan directory - process each file
                    for file_path in self._find_files_to_scan(path_obj):
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                code_content = f.read()

                            file_context = base_context.copy()
                            file_context["file_path"] = str(file_path)
                            file_context["code_snippet"] = code_content
                            file_context["language"] = self._detect_language(file_path.name)

                            file_results = asyncio.run(
                                self.hybrid_executor.execute_bundle_rules(bundle, file_context)
                            )
                            hybrid_results.extend(file_results)
                        except Exception as e:
                            print(f"Warning: Failed to scan {file_path}: {e}", file=sys.stderr)

                # Extract findings from hybrid results
                for result in hybrid_results:
                    if result.heuristics and result.heuristics.findings:
                        # Add rule metadata to each finding
                        for finding in result.heuristics.findings:
                            finding["rule_id"] = finding.get("rule_id", f"hybrid-{id(result)}")
                            finding["severity"] = finding.get("severity", "medium")
                            finding["category"] = finding.get("category", "security")
                        findings.extend(result.heuristics.findings)

                    if result.ai_analysis:
                        # Convert AI analysis to finding format
                        ai_finding = {
                            "rule_id": f"ai-analysis-{id(result)}",
                            "message": result.ai_analysis.description,
                            "path": path,
                            "start_line": result.ai_analysis.vulnerable_lines[0] if result.ai_analysis.vulnerable_lines else 1,
                            "end_line": result.ai_analysis.vulnerable_lines[-1] if result.ai_analysis.vulnerable_lines else 1,
                            "severity": result.ai_analysis.severity,
                            "category": "ai-analysis",
                            "metadata": {
                                "remediation": result.ai_analysis.remediation,
                                "owasp_mapping": result.ai_analysis.owasp_mapping,
                                "confidence": result.ai_analysis.confidence,
                                "tokens_used": result.ai_analysis.tokens_used,
                                "cost_usd": result.ai_analysis.cost_usd
                            }
                        }
                        findings.append(ai_finding)

            except Exception as e:
                print(f"Warning: Hybrid rule execution failed, falling back to legacy: {e}", file=sys.stderr)
                # Fall back to legacy OpenGrep scanning
                mode = "local"

        # Legacy OpenGrep scanning (fallback or when mode != "hybrid")
        if mode != "hybrid" or not RULE_SYSTEM_AVAILABLE:
            opengrep_rules = [rule for rule in bundle["rules"] if "pattern" in rule]

            if opengrep_rules:
                if path_obj.is_file():
                    findings.extend(self.opengrep.scan_file(path_obj, opengrep_rules))
                else:
                    findings.extend(self.opengrep.scan_directory(path_obj, opengrep_rules))

        # Execute plugins if available and requested
        if (
            PLUGIN_SYSTEM_AVAILABLE
            and self.plugin_executor
            and (static_plugins or dynamic_plugins)
        ):
            try:
                options = ScanOptions(
                    static_plugins=static_plugins or [],
                    dynamic_plugins=dynamic_plugins or [],
                    plugin_config=plugin_config or {},
                    static_analysis=bool(static_plugins),
                    dynamic_testing=bool(dynamic_plugins),
                )

                plugin_results = self.plugin_executor.execute_plugins(
                    target_path=path_obj,
                    options=options,
                )

                # Aggregate plugin findings
                for result in plugin_results:
                    if result.success:
                        findings.extend(result.findings)

            except Exception as e:
                print(f"Warning: Plugin execution failed: {e}", file=sys.stderr)

        scan_time = time.time() - start_time

        # Calculate hybrid execution stats
        hybrid_stats = {}
        if hybrid_results and self.hybrid_executor:
            hybrid_stats = self.hybrid_executor.get_execution_stats(hybrid_results)

        return {
            "vulnerabilities": findings,
            "passed": len(findings) == 0,
            "scan_time": scan_time,
            "bundle": bundle["name"],
            "rules_used": len(bundle.get("rules", [])),
            "mode": mode,
            "hybrid_stats": hybrid_stats,
            "plugin_results": (
                [
                    {
                        "plugin_id": r.plugin_id,
                        "plugin_name": r.plugin_name,
                        "success": r.success,
                        "findings_count": len(r.findings),
                        "execution_time_ms": r.execution_time_ms,
                    }
                    for r in plugin_results
                ]
                if plugin_results
                else []
            ),
        }

    def _find_files_to_scan(self, path_obj: Path) -> List[Path]:
        """Find files to scan in directory."""
        files = []
        extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.php', '.yaml', '.yml', '.rego']

        def traverse(current_path: Path):
            if not current_path.exists() or not current_path.is_dir():
                return

            try:
                for item in current_path.iterdir():
                    if item.is_file() and any(item.name.endswith(ext) for ext in extensions):
                        files.append(item)
                    elif item.is_dir() and not item.name.startswith(".") and item.name not in ["node_modules", "__pycache__", ".git"]:
                        traverse(item)
            except PermissionError:
                pass  # Skip directories we can't read

        traverse(path_obj)
        return files

    def _detect_language(self, filename: str) -> str:
        """Detect programming language from filename."""
        if not filename:
            return "unknown"

        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.clj': 'clojure',
            '.hs': 'haskell',
            '.ml': 'ocaml',
            '.fs': 'fsharp',
            '.vb': 'vb',
            '.lua': 'lua',
            '.pl': 'perl',
            '.pm': 'perl',
            '.r': 'r',
            '.m': 'matlab',
            '.sh': 'bash',
            '.bash': 'bash',
            '.zsh': 'zsh',
            '.fish': 'fish',
            '.ps1': 'powershell',
            '.sql': 'sql',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.toml': 'toml',
            '.ini': 'ini',
            '.cfg': 'ini',
            '.rego': 'rego'
        }

        for ext, lang in extension_map.items():
            if filename.endswith(ext):
                return lang

        return "unknown"


def create_scan_parser(subparsers):
    """Create scan command parser."""
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan code for security vulnerabilities"
    )
    scan_parser.add_argument("path", help="Path to file or directory to scan")
    scan_parser.add_argument(
        "--bundle",
        "-b",
        default="llm-security",
        help="Rule bundle to use (default: llm-security)",
    )
    scan_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text", "sarif"],
        default="json",
        help="Output format (default: json)",
    )
    scan_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    # Plugin options
    scan_parser.add_argument(
        "--static-plugins",
        help="Comma-separated list of static analysis plugin IDs",
    )
    scan_parser.add_argument(
        "--dynamic-plugins",
        help="Comma-separated list of dynamic testing plugin IDs",
    )
    scan_parser.add_argument(
        "--plugin-config",
        type=str,
        help="Path to plugin configuration JSON file",
    )
    scan_parser.add_argument(
        "--api-key",
        help="TavoAI API key for plugin marketplace access (or set TAVOAI_API_KEY env var)",
    )
    scan_parser.add_argument(
        "--mode",
        choices=["local", "remote", "hybrid"],
        default="local",
        help="Execution mode (default: local)",
    )


def create_auth_parser(subparsers):
    """Create auth command parser."""
    auth_parser = subparsers.add_parser(
        "auth",
        help="Manage authentication"
    )
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", help="Auth commands")

    # Login command
    login_parser = auth_subparsers.add_parser(
        "login",
        help="Authenticate with device code flow"
    )
    login_parser.add_argument(
        "--name",
        default="Tavo Scanner",
        help="Client name for authentication (default: Tavo Scanner)"
    )

    # Status command
    auth_subparsers.add_parser(
        "status",
        help="Check authentication status"
    )

    # Logout command
    auth_subparsers.add_parser(
        "logout",
        help="Clear authentication credentials"
    )


def create_health_parser(subparsers):
    """Create health command parser."""
    health_parser = subparsers.add_parser(
        "health",
        help="Check API server health"
    )
    health_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed health information"
    )


def create_registry_parser(subparsers):
    """Create registry command parser."""
    registry_parser = subparsers.add_parser(
        "registry",
        help="Manage registry bundles"
    )
    registry_subparsers = registry_parser.add_subparsers(dest="registry_command", help="Registry commands")

    # List command
    list_parser = registry_subparsers.add_parser(
        "list",
        help="List available bundles"
    )
    list_parser.add_argument(
        "--category",
        help="Filter by category"
    )
    list_parser.add_argument(
        "--pricing",
        choices=["free", "paid", "enterprise"],
        help="Filter by pricing tier"
    )
    list_parser.add_argument(
        "--search",
        help="Search bundles by name/description"
    )
    list_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of results (default: 20)"
    )

    # Install command
    install_parser = registry_subparsers.add_parser(
        "install",
        help="Install a bundle from registry"
    )
    install_parser.add_argument(
        "bundle_id",
        help="Bundle ID to install"
    )

    # Update command
    update_parser = registry_subparsers.add_parser(
        "update",
        help="Update bundles to latest versions"
    )
    update_parser.add_argument(
        "bundle_id",
        nargs="?",
        help="Bundle ID to update (updates all if not specified)"
    )

    # Info command
    info_parser = registry_subparsers.add_parser(
        "info",
        help="Show bundle information"
    )
    info_parser.add_argument(
        "bundle_id",
        help="Bundle ID to show info for"
    )

    # Installed command
    registry_subparsers.add_parser(
        "installed",
        help="List installed bundles"
    )


def create_submit_parser(subparsers):
    """Create submit command parser."""
    submit_parser = subparsers.add_parser(
        "submit",
        help="Submit code for remote analysis"
    )
    submit_parser.add_argument(
        "target",
        help="File, directory, or repository URL to submit"
    )
    submit_parser.add_argument(
        "--wait",
        action="store_true",
        help="Wait for analysis to complete"
    )
    submit_parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout for waiting (seconds, default: 300)"
    )


def create_request_scan_parser(subparsers):
    """Create request-scan command parser."""
    scan_parser = subparsers.add_parser(
        "request-scan",
        help="Request remote scan of repository"
    )
    scan_parser.add_argument(
        "repository_url",
        help="Repository URL to scan"
    )
    scan_parser.add_argument(
        "--type",
        default="security",
        choices=["security", "compliance", "vulnerability"],
        help="Scan type (default: security)"
    )
    scan_parser.add_argument(
        "--wait",
        action="store_true",
        help="Wait for scan to complete"
    )
    scan_parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout for waiting (seconds, default: 300)"
    )


def create_jobs_parser(subparsers):
    """Create jobs command parser."""
    jobs_parser = subparsers.add_parser(
        "jobs",
        help="Manage background jobs"
    )
    jobs_subparsers = jobs_parser.add_subparsers(dest="jobs_command", help="Job commands")

    # List command
    jobs_subparsers.add_parser(
        "list",
        help="List background jobs"
    )

    # Status command
    status_parser = jobs_subparsers.add_parser(
        "status",
        help="Get job status"
    )
    status_parser.add_argument(
        "job_id",
        help="Job ID to check"
    )

    # Cancel command
    cancel_parser = jobs_subparsers.add_parser(
        "cancel",
        help="Cancel a job"
    )
    cancel_parser.add_argument(
        "job_id",
        help="Job ID to cancel"
    )


def create_usage_parser(subparsers):
    """Create usage command parser."""
    usage_parser = subparsers.add_parser(
        "usage",
        help="Check token usage and budget"
    )
    usage_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed usage information"
    )


async def handle_scan(args, auth_manager, sdk_integration):
    """Handle scan command."""
    try:
        # Get API key from args or auth manager
        api_key = args.api_key
        if not api_key and auth_manager:
            creds = auth_manager.get_credentials()
            api_key = creds.api_key

        # Parse plugin lists
        static_plugins = (
            [p.strip() for p in args.static_plugins.split(",") if p.strip()]
            if args.static_plugins
            else None
        )
        dynamic_plugins = (
            [p.strip() for p in args.dynamic_plugins.split(",") if p.strip()]
            if args.dynamic_plugins
            else None
        )

        # Load plugin configuration
        plugin_config = {}
        if args.plugin_config:
            with open(args.plugin_config) as f:
                plugin_config = json.load(f)

        # Show system status
        if args.verbose:
            if RULE_SYSTEM_AVAILABLE and sdk_integration and args.mode == "hybrid":
                print("Rule system: ✓ Hybrid mode (OpenGrep + OPA + AI)", file=sys.stderr)
            elif RULE_SYSTEM_AVAILABLE:
                print("Rule system: ✓ Hybrid rules available", file=sys.stderr)
            else:
                print("Rule system: Legacy mode", file=sys.stderr)

            # Show available engines
            engines = []
            engines.append("OpenGrep/Semgrep")

            # Check for OPA support (binary or client)
            opa_available = False
            try:
                import subprocess
                subprocess.run(['opa', '--version'], capture_output=True, check=True, timeout=5)
                opa_available = True
            except:
                pass

            if not opa_available:
                try:
                    from opa_client import create_opa_client
                    # Test if OPA server is available
                    import asyncio
                    async def test_opa_server():
                        client = create_opa_client(async_mode=True, host='localhost', port=8181)
                        connected = await client.check_connection()
                        await client.close_connection()
                        return connected
                    opa_available = asyncio.run(test_opa_server())
                except:
                    pass

            if opa_available:
                engines.append("OPA/Rego")

            if sdk_integration:
                engines.append("AI Analysis")

            print(f"Available engines: {', '.join(engines)}", file=sys.stderr)

            if PLUGIN_SYSTEM_AVAILABLE:
                print("Plugin system: ✓ Available", file=sys.stderr)
                if static_plugins:
                    print(
                        f"Static plugins: {', '.join(static_plugins)}", file=sys.stderr
                    )
                if dynamic_plugins:
                    print(
                        f"Dynamic plugins: {', '.join(dynamic_plugins)}",
                        file=sys.stderr,
                    )
            else:
                print(
                    "Plugin system: ✗ Not available (install tavoai-sdk for plugin support)",
                    file=sys.stderr,
                )

        # Initialize scanner
        rule_manager = RuleManager()
        scanner = SecurityScanner(
            rule_manager,
            api_key=api_key,
            sdk_integration=sdk_integration
        )

        if args.verbose:
            print(
                f"Scanning {args.path} with bundle '{args.bundle}' in {args.mode} mode...",
                file=sys.stderr
            )

        # Perform scan
        result = scanner.scan_codebase(
            args.path,
            args.bundle,
            static_plugins=static_plugins,
            dynamic_plugins=dynamic_plugins,
            plugin_config=plugin_config,
            mode=args.mode,
        )

        # Output results
        if args.format == "json":
            print(json.dumps(result, indent=2))
        elif args.format == "sarif":
            # Convert to SARIF if plugin system available
            if PLUGIN_SYSTEM_AVAILABLE and scanner.result_aggregator:
                # Create PluginExecutionResult from findings
                findings_result = PluginExecutionResult(
                    plugin_id="opengrep",
                    plugin_name="OpenGrep",
                    plugin_version="latest",
                    success=True,
                    findings=result["vulnerabilities"],
                )
                plugin_results = result.get("plugin_results", [])
                # TODO: Convert plugin_results dict to PluginExecutionResult objects
                sarif = scanner.result_aggregator.to_sarif([findings_result])
                print(json.dumps(sarif, indent=2))
            else:
                # Fallback to JSON
                print(json.dumps(result, indent=2))
        else:  # text
            print(f"Scan Results for {args.path}")
            print(f"Bundle: {result['bundle']}")
            print(f"Rules Used: {result['rules_used']}")
            print(f"Scan Time: {result['scan_time']:.2f}s")
            print(f"Vulnerabilities Found: {len(result['vulnerabilities'])}")

            if result.get("plugin_results"):
                print(f"Plugins Executed: {len(result['plugin_results'])}")
                for pr in result["plugin_results"]:
                    status = "✓" if pr["success"] else "✗"
                    print(
                        f"  {status} {pr['plugin_name']}: {pr['findings_count']} findings"
                    )

            print(f"Status: {'PASSED' if result['passed'] else 'FAILED'}")

            if result["vulnerabilities"]:
                print("\nVulnerabilities:")
                for vuln in result["vulnerabilities"]:
                    print(
                        f"  - {vuln.get('rule_id', 'Unknown')}: {vuln.get('message', 'No message')}"
                    )

        # Exit with appropriate code
        sys.exit(0 if result["passed"] else 1)

    except ScannerError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


async def handle_auth(args, auth_manager):
    """Handle auth commands."""
    if not auth_manager:
        print("Authentication not available (SDK not installed)")
        sys.exit(1)

    if args.auth_command == "login":
        print("Starting device code authentication...")
        success = await auth_manager.device_code_login(args.name)
        if success:
            print("✅ Authentication successful!")
            sys.exit(0)
        else:
            print("❌ Authentication failed!")
            sys.exit(1)

    elif args.auth_command == "status":
        creds = auth_manager.get_credentials()
        if creds.api_key or creds.device_token:
            print("✅ Authenticated")
            user_info = creds.user_info
            if user_info:
                email = user_info.get('email', 'Unknown')
                print(f"User: {email}")
            else:
                print("User: Unknown")
        else:
            print("❌ Not authenticated")
            print("Run 'tavo auth login' to authenticate")
        sys.exit(0)

    elif args.auth_command == "logout":
        auth_manager.clear_credentials()
        print("✅ Logged out successfully")
        sys.exit(0)


async def handle_health(args, auth_manager, sdk_integration):
    """Handle health command."""
    if not sdk_integration:
        print("Health check not available (SDK not installed)")
        sys.exit(1)

    print("Checking API server health...", file=sys.stderr)

    try:
        health_status = await sdk_integration.get_health_status()

        if health_status["status"] == "healthy":
            print("✅ API Server: Healthy")
            if args.verbose:
                details = health_status.get("details", {})
                print(f"  Version: {details.get('version', 'Unknown')}")
                print(f"  Uptime: {details.get('uptime', 'Unknown')}")
                print(f"  Status: {details.get('status', 'Unknown')}")
        else:
            print("❌ API Server: Unhealthy")
            if args.verbose:
                error = health_status.get("error", "Unknown error")
                status_code = health_status.get("status_code", "Unknown")
                print(f"  Error: {error}")
                print(f"  Status Code: {status_code}")

        sys.exit(0 if health_status["status"] == "healthy" else 1)

    except Exception as e:
        print(f"❌ Health check failed: {e}", file=sys.stderr)
        sys.exit(1)


async def handle_registry(args, auth_manager, sdk_integration):
    """Handle registry commands."""
    if not sdk_integration:
        print("Registry not available (SDK not installed)")
        sys.exit(1)

    registry_manager = RegistryManager(sdk_integration)

    try:
        if args.registry_command == "list":
            bundles = await registry_manager.browse_bundles(
                category=args.category,
                pricing_tier=args.pricing,
                search=args.search,
                limit=args.limit
            )

            if not bundles:
                print("No bundles found")
                return

            print(f"Available bundles (showing {min(len(bundles), args.limit)}):")
            print()

            for bundle in bundles:
                official = " 🏷️ " if bundle.is_official else ""
                pricing = f"[{bundle.pricing_tier.upper()}]"
                rating = f"⭐ {bundle.rating:.1f}" if bundle.rating > 0 else ""
                downloads = f"⬇️ {bundle.download_count}" if bundle.download_count > 0 else ""

                print(f"{bundle.id} {official} {pricing}")
                print(f"  {bundle.name}")
                print(f"  {bundle.description}")
                if bundle.tags:
                    print(f"  Tags: {', '.join(bundle.tags)}")
                if rating or downloads:
                    stats = []
                    if rating:
                        stats.append(rating)
                    if downloads:
                        stats.append(downloads)
                    print(f"  {' | '.join(stats)}")
                print()

        elif args.registry_command == "install":
            print(f"Installing bundle: {args.bundle_id}")
            bundle_path = await registry_manager.install_bundle(args.bundle_id)
            print(f"✅ Installed to: {bundle_path}")

        elif args.registry_command == "update":
            if args.bundle_id:
                print(f"Updating bundle: {args.bundle_id}")
                updated_path = await registry_manager.update_bundle(args.bundle_id)
                if updated_path:
                    print(f"✅ Updated to: {updated_path}")
                else:
                    print("Bundle already up to date")
            else:
                print("Updating all bundles...")
                installed = registry_manager.list_installed_bundles()
                updated_count = 0

                for bundle_info in installed:
                    bundle_id = bundle_info["id"]
                    try:
                        updated_path = await registry_manager.update_bundle(bundle_id)
                        if updated_path:
                            print(f"✅ Updated {bundle_id}")
                            updated_count += 1
                        else:
                            print(f"⏭️  Skipped {bundle_id} (already up to date)")
                    except Exception as e:
                        print(f"❌ Failed to update {bundle_id}: {e}")

                print(f"\nUpdated {updated_count} bundles")

        elif args.registry_command == "info":
            if registry_manager.is_bundle_installed(args.bundle_id):
                # Show installed bundle info
                bundle_info = registry_manager.get_bundle_info(args.bundle_id)
                bundle_path = bundle_info["path"]

                print(f"Bundle: {args.bundle_id}")
                print(f"Version: {bundle_info['version']}")
                print(f"Path: {bundle_path}")
                print(f"Size: {bundle_info['size_bytes']} bytes")
                print(f"Downloaded: {time.ctime(bundle_info['downloaded_at'])}")
            else:
                # Show registry bundle info
                bundle_details = await registry_manager.get_bundle_details(args.bundle_id)

                print(f"Bundle: {bundle_details.id}")
                print(f"Name: {bundle_details.name}")
                print(f"Description: {bundle_details.description}")
                print(f"Version: {bundle_details.version}")
                print(f"Category: {bundle_details.category}")
                if bundle_details.subcategory:
                    print(f"Subcategory: {bundle_details.subcategory}")
                print(f"Pricing: {bundle_details.pricing_tier}")
                if bundle_details.tags:
                    print(f"Tags: {', '.join(bundle_details.tags)}")
                print(f"Official: {'Yes' if bundle_details.is_official else 'No'}")
                print(f"Rating: {bundle_details.rating:.1f} ({bundle_details.review_count} reviews)")
                print(f"Downloads: {bundle_details.download_count}")

        elif args.registry_command == "installed":
            installed = registry_manager.list_installed_bundles()

            if not installed:
                print("No bundles installed")
                return

            print("Installed bundles:")
            print()

            for bundle_info in installed:
                bundle_id = bundle_info["id"]
                version = bundle_info["version"]
                age_days = bundle_info["age_days"]
                size_kb = bundle_info["size_bytes"] // 1024

                print(f"{bundle_id} (v{version})")
                print(f"  Age: {age_days:.1f} days")
                print(f"  Size: {size_kb} KB")
                print()

    except Exception as e:
        print(f"Registry command failed: {e}", file=sys.stderr)
        sys.exit(1)


async def handle_submit(args, auth_manager, sdk_integration, usage_tracker):
    """Handle submit command."""
    if not sdk_integration:
        print("Code submission not available (SDK not installed)")
        sys.exit(1)

    code_submitter = CodeSubmitter(sdk_integration)

    try:
        print(f"Submitting {args.target} for remote analysis...")

        # Determine submission type
        if args.target.startswith(('http://', 'https://', 'git@', 'ssh://')):
            result = await code_submitter.submit_url(args.target)
        else:
            # Check if it's a file or directory
            from pathlib import Path
            target_path = Path(args.target)
            if target_path.is_file():
                result = await code_submitter.submit_file(args.target)
            elif target_path.is_dir():
                result = await code_submitter.submit_directory(args.target)
            else:
                raise FileNotFoundError(f"Target not found: {args.target}")

        submission_id = result.get('id', result.get('submission_id', 'unknown'))
        print(f"✅ Submitted successfully (ID: {submission_id})")

        # Track usage
        if usage_tracker and 'cost' in result:
            usage_tracker.record_usage(
                operation='code_submission',
                tokens_used=result.get('tokens_used', 0),
                cost_usd=result.get('cost', 0.0)
            )

        # Wait for completion if requested
        if args.wait:
            print("Waiting for analysis to complete...")
            try:
                final_result = await code_submitter.get_submission_status(submission_id)

                # Poll until complete
                import time
                start_time = time.time()
                while time.time() - start_time < args.timeout:
                    status = final_result.get('status', '').lower()
                    if status in ['completed', 'failed', 'error']:
                        break

                    print(f"Status: {status}...")
                    await asyncio.sleep(5)
                    final_result = await code_submitter.get_submission_status(submission_id)

                if final_result.get('status', '').lower() == 'completed':
                    print("✅ Analysis completed")
                    # Could print summary here
                else:
                    print(f"⚠️  Analysis ended with status: {final_result.get('status', 'unknown')}")

            except Exception as e:
                print(f"Warning: Failed to wait for completion: {e}")

        print(f"Submission ID: {submission_id}")

    except Exception as e:
        print(f"Submit command failed: {e}", file=sys.stderr)
        sys.exit(1)


async def handle_request_scan(args, auth_manager, sdk_integration, usage_tracker):
    """Handle request-scan command."""
    if not sdk_integration:
        print("Remote scanning not available (SDK not installed)")
        sys.exit(1)

    remote_scanner = RemoteScanner(sdk_integration, usage_tracker)

    try:
        # Check budget before proceeding
        budget_status = remote_scanner.check_budget_before_scan()
        if budget_status.get('blocked'):
            print("❌ Cannot proceed: Monthly budget exceeded")
            for warning in budget_status.get('warnings', []):
                if warning.get('level') == 'block':
                    print(f"   {warning['message']}")
                    print(f"   {warning['action']}")
            sys.exit(1)

        print(f"Requesting remote scan of {args.repository_url}...")
        result = await remote_scanner.request_scan(
            target=args.repository_url,
            scan_type=args.type
        )

        scan_id = result.get('id', result.get('scan_id', 'unknown'))
        print(f"✅ Scan requested successfully (ID: {scan_id})")

        # Wait for completion if requested
        if args.wait:
            print("Waiting for scan to complete...")
            try:
                final_result = await remote_scanner.wait_for_scan_completion(
                    scan_id=scan_id,
                    timeout_seconds=args.timeout
                )

                status = final_result.get('status', '').lower()
                if status == 'completed':
                    vulnerabilities = final_result.get('vulnerabilities', [])
                    print(f"✅ Scan completed - found {len(vulnerabilities)} vulnerabilities")
                else:
                    print(f"⚠️  Scan ended with status: {status}")

            except Exception as e:
                print(f"Warning: Failed to wait for scan completion: {e}")

        print(f"Scan ID: {scan_id}")

    except Exception as e:
        print(f"Request-scan command failed: {e}", file=sys.stderr)
        sys.exit(1)


async def handle_jobs(args, auth_manager, sdk_integration):
    """Handle jobs commands."""
    if not sdk_integration:
        print("Job management not available (SDK not installed)")
        sys.exit(1)

    try:
        if args.jobs_command == "list":
            jobs = await sdk_integration.list_jobs()

            if not jobs:
                print("No background jobs found")
                return

            print("Background jobs:")
            print()

            for job in jobs:
                job_id = job.get('id', 'unknown')
                status = job.get('status', 'unknown')
                job_type = job.get('type', 'unknown')
                created_at = job.get('created_at', 'unknown')

                status_icon = {
                    'running': '🔄',
                    'completed': '✅',
                    'failed': '❌',
                    'pending': '⏳',
                    'cancelled': '🚫'
                }.get(status.lower(), '❓')

                print(f"{status_icon} {job_id}")
                print(f"   Type: {job_type}")
                print(f"   Status: {status}")
                print(f"   Created: {created_at}")
                print()

        elif args.jobs_command == "status":
            status_result = await sdk_integration.get_job_status(args.job_id)

            job_id = status_result.get('id', args.job_id)
            job_status = status_result.get('status', 'unknown')
            progress = status_result.get('progress', {})

            print(f"Job: {job_id}")
            print(f"Status: {job_status}")

            if progress:
                files_processed = progress.get('files_processed', 0)
                total_files = progress.get('total_files', 0)
                findings = progress.get('findings', 0)

                if total_files > 0:
                    percent = (files_processed / total_files) * 100
                    print(f"Progress: {files_processed}/{total_files} files ({percent:.1f}%)")
                print(f"Findings: {findings}")

        elif args.jobs_command == "cancel":
            success = await sdk_integration.cancel_job(args.job_id)
            if success:
                print(f"✅ Job {args.job_id} cancelled successfully")
            else:
                print(f"❌ Failed to cancel job {args.job_id}")

    except Exception as e:
        print(f"Jobs command failed: {e}", file=sys.stderr)
        sys.exit(1)


def handle_usage(args, usage_tracker):
    """Handle usage command."""
    if not usage_tracker:
        print("Usage tracking not available")
        sys.exit(1)

    try:
        # Get current month usage
        monthly_usage = usage_tracker.get_current_month_usage()
        budget_status = usage_tracker.check_budget_status()

        print("Token Usage (Current Month):")
        print(f"  Used: {monthly_usage['total_tokens']:,} tokens (${monthly_usage['total_cost_usd']:.2f})")
        print(f"  Remaining: {monthly_usage['remaining_tokens']:,} tokens")
        print(f"  Usage: {monthly_usage['usage_percent']:.1f}% of monthly limit")

        # Show warnings
        warnings = budget_status.get('warnings', [])
        if warnings:
            print("\n⚠️  Budget Warnings:")
            for warning in warnings:
                level_icon = {
                    'warning': '⚠️ ',
                    'critical': '🚨',
                    'block': '🚫'
                }.get(warning.get('level'), '⚠️ ')
                print(f"  {level_icon} {warning['message']}")
                if 'action' in warning:
                    print(f"     → {warning['action']}")

        if args.verbose:
            print("\nDetailed Usage Summary:")
            summary = usage_tracker.get_usage_summary(days=30)
            print(f"  Total tokens: {summary['total_tokens']:,}")
            print(f"  Total cost: ${summary['total_cost_usd']:.2f}")
            print(f"  Daily average: {summary['average_daily_tokens']:.0f} tokens (${summary['average_daily_cost']:.2f})")

            operations = summary.get('operations', {})
            if operations:
                print("\n  By operation:")
                for op_name, op_stats in operations.items():
                    print(f"    {op_name}: {op_stats['tokens']:,} tokens (${op_stats['cost']:.2f})")

    except Exception as e:
        print(f"Usage command failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Tavo AI Security Scanner - Local security scanning with OpenGrep and plugins"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create subcommand parsers
    create_scan_parser(subparsers)
    create_auth_parser(subparsers)
    create_health_parser(subparsers)
    create_registry_parser(subparsers)
    create_submit_parser(subparsers)
    create_request_scan_parser(subparsers)
    create_jobs_parser(subparsers)
    create_usage_parser(subparsers)

    # Legacy support: if no subcommand provided, assume scan command
    args = parser.parse_args()

    # Initialize SDK components if available
    auth_manager = None
    sdk_integration = None
    usage_tracker = None

    if SDK_AVAILABLE:
        try:
            auth_manager = AuthManager()
            # Auto-authenticate if possible
            auth_manager.auto_authenticate()

            sdk_config = SDKConfig()
            sdk_integration = SDKIntegration(auth_manager, sdk_config)

            # Initialize usage tracker
            usage_tracker = UsageTracker()
        except Exception as e:
            if args.verbose:
                print(f"Warning: SDK initialization failed: {e}", file=sys.stderr)

    # Handle commands
    try:
        if args.command == "scan" or not args.command:
            # Default to scan command for backward compatibility
            asyncio.run(handle_scan(args, auth_manager, sdk_integration))
        elif args.command == "auth":
            asyncio.run(handle_auth(args, auth_manager))
        elif args.command == "health":
            asyncio.run(handle_health(args, auth_manager, sdk_integration))
        elif args.command == "registry":
            asyncio.run(handle_registry(args, auth_manager, sdk_integration))
        elif args.command == "submit":
            asyncio.run(handle_submit(args, auth_manager, sdk_integration, usage_tracker))
        elif args.command == "request-scan":
            asyncio.run(handle_request_scan(args, auth_manager, sdk_integration, usage_tracker))
        elif args.command == "jobs":
            asyncio.run(handle_jobs(args, auth_manager, sdk_integration))
        elif args.command == "usage":
            handle_usage(args, usage_tracker)
        else:
            parser.print_help()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
