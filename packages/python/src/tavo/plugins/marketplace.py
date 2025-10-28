"""Plugin marketplace client for browsing and downloading plugins"""

import httpx
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

from .interfaces import PluginType
from .exceptions import PluginNotFoundError, PluginLoadError

logger = logging.getLogger(__name__)


class MarketplacePlugin:
    """Represents a plugin in the marketplace"""

    def __init__(self, data: Dict[str, Any]):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.version: str = data["version"]
        self.description: str = data.get("description", "")
        self.plugin_type: str = data.get("plugin_type", "unknown")
        self.pricing_tier: str = data.get("pricing_tier", "free")
        self.author: str = data.get("author", "Unknown")
        self.rating: float = data.get("rating", 0.0)
        self.downloads: int = data.get("downloads", 0)
        self.tags: List[str] = data.get("tags", [])
        self.is_official: bool = data.get("is_official", False)
        self.is_vetted: bool = data.get("is_vetted", False)
        self._raw_data = data

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self._raw_data


class PluginMarketplace:
    """Client for TavoAI plugin marketplace"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.tavoai.net",
        api_version: str = "v1",
    ):
        """Initialize marketplace client

        Args:
            api_key: API key for authentication
            base_url: Base URL for API
            api_version: API version to use
        """
        self.api_key = api_key or self._get_api_key_from_env()
        self.base_url = base_url
        self.api_version = api_version
        self._client = httpx.Client(
            base_url=f"{base_url}/api/{api_version}",
            headers=self._get_auth_headers(),
            timeout=30.0,
        )
        self._cache: Dict[str, Any] = {}

    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment"""
        import os

        return os.getenv("TAVOAI_API_KEY") or os.getenv("TAVO_API_KEY")

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "tavoai-sdk/1.0.0",
        }

        if self.api_key:
            headers["X-API-Key"] = self.api_key

        return headers

    def browse(
        self,
        plugin_type: Optional[PluginType] = None,
        category: Optional[str] = None,
        pricing_tier: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> List[Dict[str, Any]]:
        """Browse marketplace plugins

        Args:
            plugin_type: Filter by plugin type
            category: Filter by category
            pricing_tier: Filter by pricing tier
            search: Search query
            page: Page number
            per_page: Results per page

        Returns:
            List of plugin dictionaries
        """
        params = {"page": page, "per_page": per_page}

        if plugin_type:
            params["plugin_type"] = plugin_type.value
        if category:
            params["category"] = category
        if pricing_tier:
            params["pricing_tier"] = pricing_tier
        if search:
            params["search"] = search

        try:
            response = self._client.get("/plugins/marketplace", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])

        except httpx.HTTPError as e:
            logger.error(f"Failed to browse marketplace: {e}")
            return []

    def get_plugin(self, plugin_id: str) -> Dict[str, Any]:
        """Get detailed plugin information

        Args:
            plugin_id: Plugin identifier

        Returns:
            Plugin details dictionary

        Raises:
            PluginNotFoundError: If plugin not found
        """
        # Check cache first
        cache_key = f"plugin:{plugin_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            response = self._client.get(f"/plugins/{plugin_id}")
            response.raise_for_status()
            plugin_data = response.json()

            # Cache the result
            self._cache[cache_key] = plugin_data

            return plugin_data

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise PluginNotFoundError(
                    f"Plugin '{plugin_id}' not found in marketplace"
                )
            raise

    def download_plugin(
        self, plugin_id: str, output_path: Optional[Path] = None
    ) -> bytes:
        """Download plugin package

        Args:
            plugin_id: Plugin identifier
            output_path: Optional path to save plugin (if None, returns bytes)

        Returns:
            Plugin package data as bytes

        Raises:
            PluginNotFoundError: If plugin not found
            PluginLoadError: If download fails
        """
        try:
            response = self._client.get(f"/plugins/{plugin_id}/download")
            response.raise_for_status()

            plugin_data = response.content

            if output_path:
                output_path.write_bytes(plugin_data)
                logger.info(f"Downloaded plugin to: {output_path}")

            return plugin_data

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise PluginNotFoundError(f"Plugin '{plugin_id}' not found")
            elif e.response.status_code == 403:
                raise PluginLoadError(
                    f"Access denied for plugin '{plugin_id}'. "
                    "Check your API key and subscription."
                )
            raise PluginLoadError(f"Failed to download plugin: {e}")

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for plugins

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            List of matching plugins
        """
        return self.browse(search=query, per_page=limit)

    def refresh(self) -> None:
        """Refresh marketplace cache"""
        self._cache.clear()
        logger.info("Marketplace cache cleared")

    def get_installed_plugins(self, cache_dir: Optional[Path] = None) -> List[str]:
        """Get list of installed plugin IDs

        Args:
            cache_dir: Plugin cache directory

        Returns:
            List of installed plugin IDs
        """
        cache_dir = cache_dir or Path.home() / ".tavoai" / "plugins"

        if not cache_dir.exists():
            return []

        installed = []
        for plugin_dir in cache_dir.iterdir():
            if plugin_dir.is_dir() and (plugin_dir / "plugin.yaml").exists():
                installed.append(plugin_dir.name)

        return installed

    def check_updates(self, plugin_ids: List[str]) -> Dict[str, Dict[str, str]]:
        """Check for plugin updates

        Args:
            plugin_ids: List of plugin IDs to check

        Returns:
            Dictionary of plugin_id -> {current_version, latest_version}
        """
        updates = {}

        for plugin_id in plugin_ids:
            try:
                latest = self.get_plugin(plugin_id)
                latest_version = latest.get("version", "unknown")

                # Get current version from installed plugin
                cache_dir = Path.home() / ".tavoai" / "plugins"
                metadata_file = cache_dir / plugin_id / "plugin.yaml"

                if metadata_file.exists():
                    import yaml

                    with open(metadata_file) as f:
                        current_metadata = yaml.safe_load(f)
                    current_version = current_metadata.get("version", "unknown")

                    if current_version != latest_version:
                        updates[plugin_id] = {
                            "current_version": current_version,
                            "latest_version": latest_version,
                        }

            except Exception as e:
                logger.warning(f"Failed to check updates for {plugin_id}: {e}")

        return updates

    def __del__(self):
        """Cleanup on destruction"""
        if hasattr(self, "_client"):
            self._client.close()
