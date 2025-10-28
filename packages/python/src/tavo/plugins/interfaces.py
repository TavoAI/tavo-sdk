"""Plugin interfaces and base classes for TavoAI plugin system"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


class PluginType(Enum):
    """Type of plugin"""

    STATIC_ANALYSIS = "static_analysis"
    DYNAMIC_TESTING = "dynamic_testing"
    PROXY_FILTERING = "proxy_filtering"
    LOG_ANALYSIS = "log_analysis"


class PricingTier(Enum):
    """Plugin pricing tier"""

    FREE = "free"
    PAID = "paid"
    ENTERPRISE = "enterprise"


@dataclass
class PluginMetadata:
    """Plugin metadata and configuration"""

    id: str
    name: str
    version: str
    description: str
    plugin_type: PluginType
    pricing_tier: PricingTier
    author: str
    license: str
    entry_point: str
    compatible_scanner_version: str = ">=1.0.0"
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    homepage: Optional[str] = None
    repository: Optional[str] = None
    documentation: Optional[str] = None
    is_official: bool = False
    is_vetted: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class PluginExecutionContext:
    """Context for plugin execution"""

    plugin_id: str
    plugin_type: PluginType
    target_path: str
    config: Dict[str, Any] = field(default_factory=dict)
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    api_key: Optional[str] = None
    timeout: int = 300  # 5 minutes default
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PluginExecutionResult:
    """Result from plugin execution"""

    plugin_id: str
    plugin_name: str
    plugin_version: str
    success: bool
    findings: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    execution_time_ms: Optional[int] = None
    tokens_used: Optional[int] = None
    cost_usd: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BasePlugin(ABC):
    """Base class for all TavoAI plugins"""

    def __init__(self):
        self._metadata: Optional[PluginMetadata] = None
        self._config: Dict[str, Any] = {}
        self._initialized: bool = False

    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata

        Returns:
            PluginMetadata: Plugin metadata including id, name, version, etc.
        """
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin with configuration

        Args:
            config: Plugin configuration dictionary

        Raises:
            PluginValidationError: If configuration is invalid
        """
        pass

    @abstractmethod
    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        """Execute plugin logic

        Args:
            context: Execution context with target path, config, etc.

        Returns:
            PluginExecutionResult: Execution result with findings

        Raises:
            PluginExecutionError: If execution fails
        """
        pass

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate plugin configuration

        Args:
            config: Configuration to validate

        Returns:
            bool: True if valid

        Raises:
            PluginValidationError: If configuration is invalid
        """
        # Override in subclass for custom validation
        return True

    def cleanup(self) -> None:
        """Cleanup resources after execution

        Override in subclass if cleanup is needed
        """
        pass


class StaticAnalysisPlugin(BasePlugin):
    """Plugin for static code analysis (SAST)

    Static analysis plugins analyze source code without executing it,
    looking for security vulnerabilities, code quality issues, and compliance violations.
    """

    @abstractmethod
    def analyze_file(
        self, file_path: str, content: str, language: str
    ) -> List[Dict[str, Any]]:
        """Analyze a single file

        Args:
            file_path: Path to the file being analyzed
            content: File content as string
            language: Programming language detected

        Returns:
            List of findings (dict with keys: severity, message, line, column, etc.)
        """
        pass

    @abstractmethod
    def analyze_repository(self, repo_path: str) -> List[Dict[str, Any]]:
        """Analyze entire repository

        Args:
            repo_path: Path to repository root

        Returns:
            List of findings across all files
        """
        pass

    def supports_language(self, language: str) -> bool:
        """Check if plugin supports a specific language

        Args:
            language: Programming language (python, javascript, java, etc.)

        Returns:
            bool: True if supported
        """
        metadata = self.get_metadata()
        supported = metadata.metadata.get("supported_languages", [])
        return language.lower() in [lang.lower() for lang in supported]


class DynamicTestingPlugin(BasePlugin):
    """Plugin for adversarial and dynamic testing

    Dynamic testing plugins perform runtime testing including adversarial attacks,
    fuzzing, and behavior analysis of AI systems.
    """

    @abstractmethod
    def run_attack(self, attack_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run adversarial attack

        Args:
            attack_config: Attack configuration including target, parameters, etc.

        Returns:
            Attack results with vulnerabilities, success rate, etc.
        """
        pass

    def get_attack_types(self) -> List[str]:
        """Get list of supported attack types

        Returns:
            List of attack type identifiers
        """
        metadata = self.get_metadata()
        return metadata.metadata.get("attack_types", [])

    def configure_attack(
        self, attack_type: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Configure specific attack type

        Args:
            attack_type: Type of attack to configure
            parameters: Attack parameters

        Returns:
            Validated attack configuration
        """
        return {"attack_type": attack_type, "parameters": parameters}


class ProxyFilteringPlugin(BasePlugin):
    """Plugin for real-time proxy filtering

    Proxy filtering plugins analyze and filter network traffic in real-time,
    typically for AI API calls, looking for malicious prompts, data exfiltration, etc.
    """

    @abstractmethod
    def filter_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Filter/analyze an outgoing request

        Args:
            request: Request data including headers, body, url, etc.

        Returns:
            Filter result with action (allow/block/alert) and reason
        """
        pass

    @abstractmethod
    def filter_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Filter/analyze an incoming response

        Args:
            response: Response data including headers, body, status, etc.

        Returns:
            Filter result with action and any modifications
        """
        pass

    def supports_provider(self, provider: str) -> bool:
        """Check if plugin supports a specific AI provider

        Args:
            provider: AI provider (openai, anthropic, google, etc.)

        Returns:
            bool: True if supported
        """
        metadata = self.get_metadata()
        supported = metadata.metadata.get("supported_providers", [])
        return provider.lower() in [p.lower() for p in supported] or "all" in supported


class LogAnalysisPlugin(BasePlugin):
    """Plugin for log analysis

    Log analysis plugins perform post-hoc analysis of logs to detect
    AI/bot traffic, security incidents, and usage patterns.
    """

    @abstractmethod
    def analyze_logs(self, log_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze log entries

        Args:
            log_entries: List of log entry dictionaries

        Returns:
            Analysis results with detected patterns, anomalies, etc.
        """
        pass

    def detect_ai_traffic(self, log_entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect if log entry represents AI traffic

        Args:
            log_entry: Single log entry

        Returns:
            Detection result if AI traffic detected, None otherwise
        """
        # Override in subclass for custom detection
        return None

    def extract_patterns(
        self, log_entries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract traffic patterns from logs

        Args:
            log_entries: List of log entries

        Returns:
            List of detected patterns
        """
        # Override in subclass for custom pattern extraction
        return []


class AdversarialTestingPlugin(DynamicTestingPlugin):
    """Specialized plugin for adversarial testing (alias for compatibility)

    This is an alias for DynamicTestingPlugin to maintain compatibility with
    existing code that references AdversarialTestingPlugin.
    """

    pass
