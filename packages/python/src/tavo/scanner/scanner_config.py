"""Scanner configuration and options"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class ScanOptions:
    """Options for scanner execution"""

    # Static analysis options
    static_analysis: bool = True
    static_plugins: List[str] = field(default_factory=list)
    static_rules: Optional[Path] = None

    # Dynamic testing options
    dynamic_testing: bool = False
    dynamic_plugins: List[str] = field(default_factory=list)

    # Output options
    output_format: str = "sarif"  # sarif, json, text
    output_file: Optional[Path] = None

    # Execution options
    timeout: int = 300  # 5 minutes
    max_file_size: int = 10 * 1024 * 1024  # 10 MB
    exclude_patterns: List[str] = field(default_factory=list)
    include_patterns: List[str] = field(default_factory=list)

    # Plugin options
    plugin_config: Dict[str, Any] = field(default_factory=dict)

    # AI analysis options
    enable_ai_analysis: bool = False
    ai_analysis_threshold: float = 0.7


@dataclass
class ScannerConfig:
    """Configuration for TavoAI scanner"""

    api_key: Optional[str] = None
    base_url: str = "https://api.tavoai.net"
    api_version: str = "v1"

    # Plugin configuration
    plugin_cache_dir: Path = field(
        default_factory=lambda: Path.home() / ".tavoai" / "plugins"
    )
    auto_update_plugins: bool = False

    # Scanner paths
    opengrep_path: Optional[Path] = None
    semgrep_path: Optional[Path] = None
    opa_path: Optional[Path] = None

    # Logging
    log_level: str = "INFO"
    log_file: Optional[Path] = None

    def __post_init__(self):
        """Post-initialization validation"""
        # Ensure plugin cache directory exists
        self.plugin_cache_dir.mkdir(parents=True, exist_ok=True)
