"""TavoAI Plugin System

This module provides the plugin architecture for extending TavoAI's security scanning
capabilities with third-party tools and custom analyzers.
"""

from .interfaces import (
    PluginType,
    BasePlugin,
    StaticAnalysisPlugin,
    DynamicTestingPlugin,
    ProxyFilteringPlugin,
    LogAnalysisPlugin,
    PluginMetadata,
    PluginExecutionContext,
    PluginExecutionResult,
)
from .registry import PluginRegistry, DynamicPluginRegistry
from .marketplace import PluginMarketplace, MarketplacePlugin
from .manager import PluginManager, LocalPluginManager
from .exceptions import (
    PluginError,
    PluginNotFoundError,
    PluginLoadError,
    PluginExecutionError,
    PluginValidationError,
)

__all__ = [
    # Types
    "PluginType",
    # Base classes
    "BasePlugin",
    "StaticAnalysisPlugin",
    "DynamicTestingPlugin",
    "ProxyFilteringPlugin",
    "LogAnalysisPlugin",
    # Data models
    "PluginMetadata",
    "PluginExecutionContext",
    "PluginExecutionResult",
    # Registry
    "PluginRegistry",
    "DynamicPluginRegistry",
    # Marketplace
    "PluginMarketplace",
    "MarketplacePlugin",
    # Manager
    "PluginManager",
    "LocalPluginManager",
    # Exceptions
    "PluginError",
    "PluginNotFoundError",
    "PluginLoadError",
    "PluginExecutionError",
    "PluginValidationError",
]
