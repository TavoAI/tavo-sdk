"""
Tavo Scanner Wrapper

Executes tavo-scanner as a subprocess with plugin/rule configuration.
"""

import asyncio
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field

from .scanner.scanner_config import ScanOptions


@dataclass
class ScannerConfig:
    """Configuration for tavo-scanner execution"""

    # Scanner binary path
    scanner_path: Optional[Path] = None

    # Plugin configuration
    plugins: List[str] = field(default_factory=list)
    plugin_config: Dict[str, Any] = field(default_factory=dict)

    # Rule configuration
    rules_path: Optional[Path] = None
    custom_rules: Dict[str, Any] = field(default_factory=dict)

    # Execution options
    timeout: int = 300  # 5 minutes
    working_directory: Optional[Path] = None

    # Output options
    output_format: str = "json"
    output_file: Optional[Path] = None

    def __post_init__(self):
        if self.scanner_path is None:
            # Try to find tavo-scanner in common locations
            self.scanner_path = self._find_scanner_binary()

    def _find_scanner_binary(self) -> Optional[Path]:
        """Find the tavo-scanner binary in common locations"""
        # Check relative to this package
        package_dir = Path(__file__).parent.parent.parent.parent.parent
        scanner_path = package_dir / "tavo-cli" / "bin" / "tavo-scanner"
        if scanner_path.exists():
            return scanner_path

        # Check in PATH
        import shutil
        scanner_in_path = shutil.which("tavo-scanner")
        if scanner_in_path:
            return Path(scanner_in_path)

        return None


class TavoScanner:
    """Wrapper for executing tavo-scanner as a subprocess"""

    def __init__(self, config: Optional[ScannerConfig] = None):
        self.config = config or ScannerConfig()

    async def scan_directory(
        self,
        target_path: Union[str, Path],
        scan_options: Optional[ScanOptions] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Scan a directory with tavo-scanner

        Args:
            target_path: Path to directory or file to scan
            scan_options: Scan configuration options
            **kwargs: Additional scanner arguments

        Returns:
            Scan results as dictionary
        """
        if not self.config.scanner_path:
            raise FileNotFoundError("tavo-scanner binary not found. Please install tavo-cli or set scanner_path.")

        # Merge scan options with config
        merged_config = ScannerConfig()
        if scan_options:
            # Convert ScanOptions to ScannerConfig
            merged_config.plugins = scan_options.static_plugins
            merged_config.rules_path = scan_options.static_rules
            merged_config.timeout = scan_options.timeout
            merged_config.output_format = scan_options.output_format
            merged_config.output_file = scan_options.output_file

        # Override with instance config
        for key, value in self.config.__dict__.items():
            if value is not None:
                setattr(merged_config, key, value)

        # Override with kwargs
        for key, value in kwargs.items():
            if hasattr(merged_config, key):
                setattr(merged_config, key, value)

        # Prepare scanner command
        cmd = [str(merged_config.scanner_path)]

        # Add target path
        cmd.append(str(target_path))

        # Add plugins
        if merged_config.plugins:
            for plugin in merged_config.plugins:
                cmd.extend(["--plugin", plugin])

        # Add rules
        if merged_config.rules_path:
            cmd.extend(["--rules", str(merged_config.rules_path)])

        # Add output options
        if merged_config.output_format:
            cmd.extend(["--format", merged_config.output_format])

        if merged_config.output_file:
            cmd.extend(["--output", str(merged_config.output_file)])

        # Add timeout
        if merged_config.timeout:
            cmd.extend(["--timeout", str(merged_config.timeout)])

        # Execute scanner
        return await self._execute_scanner(cmd, merged_config.working_directory)

    async def scan_with_plugins(
        self,
        target_path: Union[str, Path],
        plugins: List[str],
        **kwargs
    ) -> Dict[str, Any]:
        """Scan with specific plugins"""
        config = ScannerConfig(plugins=plugins)
        scanner = TavoScanner(config)
        return await scanner.scan_directory(target_path, **kwargs)

    async def scan_with_rules(
        self,
        target_path: Union[str, Path],
        rules_path: Union[str, Path],
        **kwargs
    ) -> Dict[str, Any]:
        """Scan with custom rules"""
        config = ScannerConfig(rules_path=Path(rules_path))
        scanner = TavoScanner(config)
        return await scanner.scan_directory(target_path, **kwargs)

    async def _execute_scanner(
        self,
        cmd: List[str],
        working_directory: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Execute the scanner subprocess"""
        try:
            # Run scanner as subprocess
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=working_directory,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Wait for completion
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                raise RuntimeError(f"Scanner failed with exit code {process.returncode}: {error_msg}")

            # Parse output
            output = stdout.decode().strip()
            if not output:
                return {"status": "success", "results": []}

            try:
                return json.loads(output)
            except json.JSONDecodeError:
                # If not JSON, return as text
                return {"status": "success", "output": output}

        except FileNotFoundError:
            raise FileNotFoundError(f"tavo-scanner binary not found at {self.config.scanner_path}")
        except asyncio.TimeoutError:
            raise TimeoutError(f"Scanner timed out after {self.config.timeout} seconds")

    def create_plugin_config(self, plugin_name: str, config: Dict[str, Any]) -> Path:
        """Create a temporary plugin configuration file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f, indent=2)
            return Path(f.name)

    def create_rules_file(self, rules: Dict[str, Any]) -> Path:
        """Create a temporary rules file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(rules, f, indent=2)
            return Path(f.name)
