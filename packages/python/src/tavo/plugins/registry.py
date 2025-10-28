"""Plugin registry for discovering and loading plugins"""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Type
import logging

from .interfaces import (
    BasePlugin,
    PluginType,
    PluginMetadata,
    PluginExecutionContext,
    PluginExecutionResult,
)
from .exceptions import (
    PluginNotFoundError,
    PluginLoadError,
    PluginExecutionError,
    PluginValidationError,
)
from .marketplace import PluginMarketplace

logger = logging.getLogger(__name__)


class PluginRegistry:
    """Registry for plugin discovery and loading"""

    def __init__(self, api_key: Optional[str] = None, cache_dir: Optional[Path] = None):
        """Initialize plugin registry

        Args:
            api_key: API key for marketplace access
            cache_dir: Directory for caching plugin data
        """
        self.api_key = api_key
        self.cache_dir = cache_dir or Path.home() / ".tavoai" / "plugins"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self._loaded_plugins: Dict[str, BasePlugin] = {}
        self._plugin_metadata: Dict[str, PluginMetadata] = {}

    def load_plugin(
        self, plugin_id: str, plugin_type: Optional[PluginType] = None
    ) -> BasePlugin:
        """Load a plugin by ID

        Args:
            plugin_id: Plugin identifier
            plugin_type: Expected plugin type (optional, for validation)

        Returns:
            Loaded plugin instance

        Raises:
            PluginNotFoundError: If plugin not found
            PluginLoadError: If plugin fails to load
        """
        # Check if already loaded
        if plugin_id in self._loaded_plugins:
            return self._loaded_plugins[plugin_id]

        # Try to load from installed plugins
        plugin_path = self.cache_dir / plugin_id

        if not plugin_path.exists():
            raise PluginNotFoundError(
                f"Plugin '{plugin_id}' not found. "
                f"Install with: tavo plugins install {plugin_id}"
            )

        try:
            # Load plugin metadata
            metadata_file = plugin_path / "plugin.yaml"
            if not metadata_file.exists():
                raise PluginLoadError(f"Plugin metadata not found: {metadata_file}")

            import yaml

            with open(metadata_file) as f:
                metadata_dict = yaml.safe_load(f)

            metadata = self._parse_metadata(metadata_dict)

            # Validate plugin type if specified
            if plugin_type and metadata.plugin_type != plugin_type:
                raise PluginLoadError(
                    f"Plugin '{plugin_id}' is type {metadata.plugin_type.value}, "
                    f"expected {plugin_type.value}"
                )

            # Load plugin module
            entry_point = metadata.entry_point  # e.g., "module.plugin:PluginClass"
            module_path, class_name = entry_point.split(":")

            # Add plugin directory to sys.path
            plugin_src = plugin_path / plugin_id.replace("-", "_")
            if plugin_src.exists() and str(plugin_src.parent) not in sys.path:
                sys.path.insert(0, str(plugin_src.parent))

            # Import module
            module = importlib.import_module(module_path)

            # Get plugin class
            plugin_class: Type[BasePlugin] = getattr(module, class_name)

            # Instantiate plugin
            plugin = plugin_class()

            # Store metadata and plugin
            self._plugin_metadata[plugin_id] = metadata
            self._loaded_plugins[plugin_id] = plugin

            logger.info(f"Loaded plugin: {plugin_id} v{metadata.version}")

            return plugin

        except Exception as e:
            raise PluginLoadError(f"Failed to load plugin '{plugin_id}': {e}") from e

    def unload_plugin(self, plugin_id: str) -> None:
        """Unload a plugin from memory

        Args:
            plugin_id: Plugin identifier
        """
        if plugin_id in self._loaded_plugins:
            plugin = self._loaded_plugins[plugin_id]
            plugin.cleanup()
            del self._loaded_plugins[plugin_id]

        if plugin_id in self._plugin_metadata:
            del self._plugin_metadata[plugin_id]

    def list_loaded_plugins(self) -> List[str]:
        """Get list of currently loaded plugin IDs

        Returns:
            List of plugin IDs
        """
        return list(self._loaded_plugins.keys())

    def get_plugin_metadata(self, plugin_id: str) -> Optional[PluginMetadata]:
        """Get metadata for a plugin

        Args:
            plugin_id: Plugin identifier

        Returns:
            Plugin metadata if loaded, None otherwise
        """
        return self._plugin_metadata.get(plugin_id)

    def _parse_metadata(self, metadata_dict: Dict[str, Any]) -> PluginMetadata:
        """Parse metadata dictionary into PluginMetadata object

        Args:
            metadata_dict: Raw metadata dictionary from YAML

        Returns:
            PluginMetadata object
        """
        return PluginMetadata(
            id=metadata_dict["id"],
            name=metadata_dict["name"],
            version=metadata_dict["version"],
            description=metadata_dict.get("description", ""),
            plugin_type=PluginType(metadata_dict["plugin_type"]),
            pricing_tier=metadata_dict.get("pricing_tier", "free"),
            author=metadata_dict.get("author", "Unknown"),
            license=metadata_dict.get("license", "Unknown"),
            entry_point=metadata_dict["entry_point"],
            compatible_scanner_version=metadata_dict.get(
                "compatible_scanner_version", ">=1.0.0"
            ),
            dependencies=metadata_dict.get("dependencies", {}),
            tags=metadata_dict.get("tags", []),
            homepage=metadata_dict.get("homepage"),
            repository=metadata_dict.get("repository"),
            documentation=metadata_dict.get("documentation"),
            is_official=metadata_dict.get("is_official", False),
            is_vetted=metadata_dict.get("is_vetted", False),
        )


class DynamicPluginRegistry(PluginRegistry):
    """Extended plugin registry with marketplace integration"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        cache_dir: Optional[Path] = None,
        marketplace: Optional[PluginMarketplace] = None,
    ):
        """Initialize dynamic plugin registry

        Args:
            api_key: API key for marketplace access
            cache_dir: Directory for caching plugin data
            marketplace: PluginMarketplace instance (created if not provided)
        """
        super().__init__(api_key, cache_dir)
        self.marketplace = marketplace or PluginMarketplace(api_key=api_key)

    def list_available_plugins(
        self, plugin_type: Optional[PluginType] = None
    ) -> Dict[str, Dict[str, Any]]:
        """List all available plugins from marketplace

        Args:
            plugin_type: Filter by plugin type

        Returns:
            Dictionary of plugin_id -> plugin info
        """
        try:
            plugins = self.marketplace.browse(plugin_type=plugin_type)
            return {p["id"]: p for p in plugins}
        except Exception as e:
            logger.error(f"Failed to list plugins from marketplace: {e}")
            return {}

    def install_plugin(self, plugin_id: str) -> bool:
        """Install a plugin from marketplace

        Args:
            plugin_id: Plugin identifier

        Returns:
            True if installation successful

        Raises:
            PluginNotFoundError: If plugin not in marketplace
            PluginLoadError: If installation fails
        """
        try:
            # Download plugin from marketplace
            plugin_data = self.marketplace.download_plugin(plugin_id)

            # Extract to cache directory
            plugin_path = self.cache_dir / plugin_id
            plugin_path.mkdir(parents=True, exist_ok=True)

            # Save plugin files
            import zipfile
            import io

            with zipfile.ZipFile(io.BytesIO(plugin_data)) as zf:
                zf.extractall(plugin_path)

            logger.info(f"Installed plugin: {plugin_id}")
            return True

        except Exception as e:
            raise PluginLoadError(f"Failed to install plugin '{plugin_id}': {e}") from e

    def uninstall_plugin(self, plugin_id: str) -> bool:
        """Uninstall a plugin

        Args:
            plugin_id: Plugin identifier

        Returns:
            True if uninstallation successful
        """
        # Unload from memory first
        self.unload_plugin(plugin_id)

        # Remove from disk
        plugin_path = self.cache_dir / plugin_id
        if plugin_path.exists():
            import shutil

            shutil.rmtree(plugin_path)
            logger.info(f"Uninstalled plugin: {plugin_id}")
            return True

        return False

    def refresh_marketplace(self) -> bool:
        """Refresh plugin list from marketplace

        Returns:
            True if refresh successful
        """
        try:
            self.marketplace.refresh()
            return True
        except Exception as e:
            logger.error(f"Failed to refresh marketplace: {e}")
            return False

    def get_plugin_info(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed plugin information

        Args:
            plugin_id: Plugin identifier

        Returns:
            Plugin information dictionary or None
        """
        try:
            return self.marketplace.get_plugin(plugin_id)
        except Exception as e:
            logger.error(f"Failed to get plugin info: {e}")
            return None

    def list_installed_plugins(
        self, plugin_type: Optional[PluginType] = None
    ) -> List[str]:
        """List installed plugins

        Args:
            plugin_type: Filter by plugin type

        Returns:
            List of installed plugin IDs
        """
        installed = []

        if not self.cache_dir.exists():
            return installed

        for plugin_dir in self.cache_dir.iterdir():
            if not plugin_dir.is_dir():
                continue

            metadata_file = plugin_dir / "plugin.yaml"
            if not metadata_file.exists():
                continue

            # Check if plugin type matches filter
            if plugin_type:
                import yaml

                try:
                    with open(metadata_file) as f:
                        metadata = yaml.safe_load(f)
                    if PluginType(metadata["plugin_type"]) != plugin_type:
                        continue
                except Exception:
                    continue

            installed.append(plugin_dir.name)

        return installed
