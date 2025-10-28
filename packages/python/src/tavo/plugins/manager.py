"""Plugin manager for installation, updates, and lifecycle management"""

import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import subprocess
import sys

from .interfaces import PluginType, PluginMetadata
from .exceptions import (
    PluginLoadError,
    PluginValidationError,
    PluginDependencyError,
)

logger = logging.getLogger(__name__)


class PluginManager:
    """Manages plugin installation, updates, and dependencies"""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize plugin manager

        Args:
            cache_dir: Directory for plugin storage
        """
        self.cache_dir = cache_dir or Path.home() / ".tavoai" / "plugins"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Separate directories for marketplace and local plugins
        self.marketplace_dir = self.cache_dir / "marketplace"
        self.local_dir = self.cache_dir / "local"
        self.marketplace_dir.mkdir(exist_ok=True)
        self.local_dir.mkdir(exist_ok=True)

    def install_from_package(
        self, plugin_data: bytes, plugin_id: str, is_vetted: bool = True
    ) -> bool:
        """Install plugin from package data

        Args:
            plugin_data: Plugin package (zip file)
            plugin_id: Plugin identifier
            is_vetted: Whether plugin is from vetted marketplace

        Returns:
            True if installation successful

        Raises:
            PluginLoadError: If installation fails
        """
        import zipfile
        import io

        # Choose installation directory
        install_dir = self.marketplace_dir if is_vetted else self.local_dir
        plugin_path = install_dir / plugin_id

        # Remove existing installation
        if plugin_path.exists():
            shutil.rmtree(plugin_path)

        plugin_path.mkdir(parents=True)

        try:
            # Extract plugin package
            with zipfile.ZipFile(io.BytesIO(plugin_data)) as zf:
                zf.extractall(plugin_path)

            # Validate plugin structure
            if not self._validate_plugin_structure(plugin_path):
                shutil.rmtree(plugin_path)
                raise PluginValidationError(
                    f"Invalid plugin structure for '{plugin_id}'"
                )

            # Install dependencies
            if not self._install_dependencies(plugin_path):
                logger.warning(
                    f"Failed to install dependencies for '{plugin_id}'. "
                    "Plugin may not work correctly."
                )

            logger.info(
                f"Installed plugin: {plugin_id} "
                f"({'vetted' if is_vetted else 'local'})"
            )
            return True

        except Exception as e:
            # Cleanup on failure
            if plugin_path.exists():
                shutil.rmtree(plugin_path)
            raise PluginLoadError(f"Failed to install plugin '{plugin_id}': {e}") from e

    def install_from_local_path(self, source_path: Path, plugin_id: str) -> bool:
        """Install plugin from local directory

        Args:
            source_path: Path to plugin source directory
            plugin_id: Plugin identifier

        Returns:
            True if installation successful
        """
        if not source_path.exists():
            raise PluginLoadError(f"Source path not found: {source_path}")

        # Validate plugin structure
        if not self._validate_plugin_structure(source_path):
            raise PluginValidationError(
                f"Invalid plugin structure at '{source_path}'. "
                "Missing plugin.yaml or entry point."
            )

        # Copy to local plugins directory
        plugin_path = self.local_dir / plugin_id

        if plugin_path.exists():
            shutil.rmtree(plugin_path)

        shutil.copytree(source_path, plugin_path)

        logger.info(f"Installed local plugin: {plugin_id}")
        return True

    def uninstall(self, plugin_id: str) -> bool:
        """Uninstall a plugin

        Args:
            plugin_id: Plugin identifier

        Returns:
            True if uninstallation successful
        """
        # Try marketplace plugins first
        plugin_path = self.marketplace_dir / plugin_id

        if not plugin_path.exists():
            # Try local plugins
            plugin_path = self.local_dir / plugin_id

        if plugin_path.exists():
            shutil.rmtree(plugin_path)
            logger.info(f"Uninstalled plugin: {plugin_id}")
            return True

        return False

    def list_installed(self) -> List[Dict[str, Any]]:
        """List all installed plugins

        Returns:
            List of plugin info dictionaries
        """
        plugins = []

        # List marketplace plugins
        for plugin_dir in self.marketplace_dir.iterdir():
            if plugin_dir.is_dir():
                plugin_info = self._get_plugin_info(plugin_dir)
                if plugin_info:
                    plugin_info["source"] = "marketplace"
                    plugin_info["is_vetted"] = True
                    plugins.append(plugin_info)

        # List local plugins
        for plugin_dir in self.local_dir.iterdir():
            if plugin_dir.is_dir():
                plugin_info = self._get_plugin_info(plugin_dir)
                if plugin_info:
                    plugin_info["source"] = "local"
                    plugin_info["is_vetted"] = False
                    plugins.append(plugin_info)

        return plugins

    def get_plugin_path(self, plugin_id: str) -> Optional[Path]:
        """Get path to installed plugin

        Args:
            plugin_id: Plugin identifier

        Returns:
            Path to plugin directory or None if not installed
        """
        # Check marketplace plugins
        marketplace_path = self.marketplace_dir / plugin_id
        if marketplace_path.exists():
            return marketplace_path

        # Check local plugins
        local_path = self.local_dir / plugin_id
        if local_path.exists():
            return local_path

        return None

    def is_installed(self, plugin_id: str) -> bool:
        """Check if plugin is installed

        Args:
            plugin_id: Plugin identifier

        Returns:
            True if installed
        """
        return self.get_plugin_path(plugin_id) is not None

    def _validate_plugin_structure(self, plugin_path: Path) -> bool:
        """Validate plugin has required files

        Args:
            plugin_path: Path to plugin directory

        Returns:
            True if valid structure
        """
        # Check for plugin.yaml
        if not (plugin_path / "plugin.yaml").exists():
            logger.error(f"Missing plugin.yaml in {plugin_path}")
            return False

        # Load and validate metadata
        import yaml

        try:
            with open(plugin_path / "plugin.yaml") as f:
                metadata = yaml.safe_load(f)

            # Required fields
            required = ["id", "name", "version", "plugin_type", "entry_point"]
            for field in required:
                if field not in metadata:
                    logger.error(f"Missing required field '{field}' in plugin.yaml")
                    return False

            # Validate entry point exists
            entry_point = metadata["entry_point"]
            module_path, class_name = entry_point.split(":")
            module_file = module_path.replace(".", "/") + ".py"

            # Check if module file exists
            plugin_src = plugin_path / metadata["id"].replace("-", "_")
            if not plugin_src.exists():
                logger.error(f"Plugin source directory not found: {plugin_src}")
                return False

            return True

        except Exception as e:
            logger.error(f"Failed to validate plugin structure: {e}")
            return False

    def _install_dependencies(self, plugin_path: Path) -> bool:
        """Install plugin dependencies

        Args:
            plugin_path: Path to plugin directory

        Returns:
            True if dependencies installed successfully
        """
        # Load plugin metadata
        import yaml

        metadata_file = plugin_path / "plugin.yaml"
        with open(metadata_file) as f:
            metadata = yaml.safe_load(f)

        dependencies = metadata.get("dependencies", {})
        packages = dependencies.get("packages", [])

        if not packages:
            return True  # No dependencies to install

        try:
            # Install packages using pip
            cmd = [sys.executable, "-m", "pip", "install"] + packages

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300  # 5 min timeout
            )

            if result.returncode == 0:
                logger.info(f"Installed dependencies for {plugin_path.name}")
                return True
            else:
                logger.error(f"Failed to install dependencies: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("Dependency installation timed out")
            return False
        except Exception as e:
            logger.error(f"Error installing dependencies: {e}")
            return False

    def _get_plugin_info(self, plugin_dir: Path) -> Optional[Dict[str, Any]]:
        """Get plugin information from directory

        Args:
            plugin_dir: Path to plugin directory

        Returns:
            Plugin info dictionary or None if invalid
        """
        metadata_file = plugin_dir / "plugin.yaml"

        if not metadata_file.exists():
            return None

        import yaml

        try:
            with open(metadata_file) as f:
                metadata = yaml.safe_load(f)

            # Add installation info
            metadata["installed"] = True
            metadata["install_path"] = str(plugin_dir)

            return metadata

        except Exception as e:
            logger.warning(f"Failed to read plugin metadata from {plugin_dir}: {e}")
            return None


class LocalPluginManager(PluginManager):
    """Manager for local (non-marketplace) plugins"""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize local plugin manager

        Args:
            cache_dir: Directory for plugin storage
        """
        super().__init__(cache_dir)

    def install_local_plugin(
        self, source_path: Path, plugin_id: Optional[str] = None
    ) -> str:
        """Install plugin from local directory with user confirmation

        Args:
            source_path: Path to plugin source
            plugin_id: Optional plugin ID (read from metadata if not provided)

        Returns:
            Installed plugin ID

        Raises:
            PluginValidationError: If plugin validation fails
        """
        # Validate plugin structure
        if not self._validate_plugin_structure(source_path):
            raise PluginValidationError(f"Invalid plugin structure at '{source_path}'")

        # Read plugin ID from metadata if not provided
        if not plugin_id:
            import yaml

            with open(source_path / "plugin.yaml") as f:
                metadata = yaml.safe_load(f)
            plugin_id = metadata["id"]

        # Show warning for local plugins
        logger.warning(
            f"Installing local plugin '{plugin_id}' from '{source_path}'. "
            f"Local plugins are not vetted by TavoAI. "
            f"Only install plugins from trusted sources."
        )

        # Install to local directory
        if self.install_from_local_path(source_path, plugin_id):
            return plugin_id

        raise PluginLoadError(f"Failed to install local plugin from '{source_path}'")

    def list_local_plugins(self) -> List[Dict[str, Any]]:
        """List only local (non-marketplace) plugins

        Returns:
            List of local plugin info dictionaries
        """
        plugins = []

        for plugin_dir in self.local_dir.iterdir():
            if plugin_dir.is_dir():
                plugin_info = self._get_plugin_info(plugin_dir)
                if plugin_info:
                    plugin_info["source"] = "local"
                    plugin_info["is_vetted"] = False
                    plugins.append(plugin_info)

        return plugins
