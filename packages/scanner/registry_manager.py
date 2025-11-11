"""
Registry Manager for Tavo Scanner

Handles browsing, downloading, and managing bundles from the TavoAI Registry.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .bundle_cache import BundleCache


@dataclass
class RegistryBundle:
    """Registry bundle metadata."""
    id: str
    name: str
    description: str
    version: str
    pricing_tier: str
    category: str
    subcategory: str
    tags: List[str]
    download_count: int
    rating: float
    review_count: int
    is_official: bool
    compatible_scanners: List[str]


class RegistryManager:
    """Manages interactions with the TavoAI Registry."""

    def __init__(self, sdk_integration=None, cache_dir: Optional[Path] = None):
        """Initialize registry manager.

        Args:
            sdk_integration: SDK integration instance
            cache_dir: Directory for bundle caching
        """
        self.sdk_integration = sdk_integration
        self.bundle_cache = BundleCache(cache_dir)

    async def browse_bundles(
        self,
        category: Optional[str] = None,
        pricing_tier: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50
    ) -> List[RegistryBundle]:
        """Browse available bundles in the registry.

        Args:
            category: Filter by category (e.g., "security", "compliance")
            pricing_tier: Filter by pricing ("free", "paid", "enterprise")
            search: Search term for bundle names/descriptions
            limit: Maximum number of results

        Returns:
            List of available bundles
        """
        if not self.sdk_integration:
            raise RuntimeError("SDK integration not available")

        try:
            # Build query parameters
            params = {"limit": limit}
            if category:
                params["category"] = category
            if pricing_tier:
                params["pricing_tier"] = pricing_tier
            if search:
                params["search"] = search

            # Query registry
            response = await self.sdk_integration.browse_registry(**params)

            # Convert to RegistryBundle objects
            bundles = []
            for item in response:
                bundle = RegistryBundle(
                    id=item["id"],
                    name=item["name"],
                    description=item["description"],
                    version=item["version"],
                    pricing_tier=item.get("pricing_tier", "free"),
                    category=item.get("category", ""),
                    subcategory=item.get("subcategory", ""),
                    tags=item.get("tags", []),
                    download_count=item.get("download_count", 0),
                    rating=item.get("rating", 0.0),
                    review_count=item.get("review_count", 0),
                    is_official=item.get("is_official", False),
                    compatible_scanners=item.get("compatible_scanners", [])
                )
                bundles.append(bundle)

            return bundles

        except Exception as e:
            raise RuntimeError(f"Failed to browse registry: {e}")

    async def get_bundle_details(self, bundle_id: str) -> RegistryBundle:
        """Get detailed information about a specific bundle.

        Args:
            bundle_id: Bundle identifier

        Returns:
            Bundle details
        """
        if not self.sdk_integration:
            raise RuntimeError("SDK integration not available")

        try:
            response = await self.sdk_integration.download_bundle(bundle_id)

            return RegistryBundle(
                id=response["id"],
                name=response["name"],
                description=response["description"],
                version=response["version"],
                pricing_tier=response.get("pricing_tier", "free"),
                category=response.get("category", ""),
                subcategory=response.get("subcategory", ""),
                tags=response.get("tags", []),
                download_count=response.get("download_count", 0),
                rating=response.get("rating", 0.0),
                review_count=response.get("review_count", 0),
                is_official=response.get("is_official", False),
                compatible_scanners=response.get("compatible_scanners", [])
            )

        except Exception as e:
            raise RuntimeError(f"Failed to get bundle details: {e}")

    async def install_bundle(self, bundle_id: str) -> Path:
        """Install a bundle from the registry.

        Args:
            bundle_id: Bundle identifier

        Returns:
            Path to installed bundle
        """
        if not self.sdk_integration:
            raise RuntimeError("SDK integration not available")

        try:
            # Check if already cached
            cached_path = self.bundle_cache.get_cached_bundle(bundle_id)
            if cached_path and cached_path.exists():
                return cached_path

            # Install from registry
            await self.sdk_integration.install_bundle(bundle_id)

            # Download bundle content
            bundle_data = await self.sdk_integration.download_bundle(bundle_id)

            # Cache the bundle
            cached_path = self.bundle_cache.cache_bundle(bundle_id, bundle_data)

            return cached_path

        except Exception as e:
            raise RuntimeError(f"Failed to install bundle {bundle_id}: {e}")

    async def update_bundle(self, bundle_id: str) -> Optional[Path]:
        """Update a bundle to the latest version.

        Args:
            bundle_id: Bundle identifier

        Returns:
            Path to updated bundle, or None if no update needed
        """
        try:
            # Get current cached bundle info
            cached_info = self.bundle_cache.get_bundle_info(bundle_id)
            if not cached_info:
                # Not installed, install instead
                return await self.install_bundle(bundle_id)

            # Get latest version from registry
            latest_bundle = await self.get_bundle_details(bundle_id)

            if latest_bundle.version == cached_info["version"]:
                return None  # Already up to date

            # Update to latest version
            return await self.install_bundle(bundle_id)

        except Exception as e:
            raise RuntimeError(f"Failed to update bundle {bundle_id}: {e}")

    def list_installed_bundles(self) -> List[Dict[str, Any]]:
        """List locally installed bundles.

        Returns:
            List of installed bundle information
        """
        return self.bundle_cache.list_cached_bundles()

    def get_installed_bundle_path(self, bundle_id: str) -> Optional[Path]:
        """Get path to installed bundle.

        Args:
            bundle_id: Bundle identifier

        Returns:
            Path to bundle, or None if not installed
        """
        return self.bundle_cache.get_cached_bundle(bundle_id)

    def uninstall_bundle(self, bundle_id: str) -> bool:
        """Uninstall a bundle.

        Args:
            bundle_id: Bundle identifier

        Returns:
            True if uninstalled, False if not found
        """
        return self.bundle_cache.remove_bundle(bundle_id)

    def clear_cache(self) -> None:
        """Clear the bundle cache."""
        self.bundle_cache.clear_cache()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics.

        Returns:
            Cache statistics
        """
        return self.bundle_cache.get_stats()

    async def search_bundles(self, query: str, limit: int = 20) -> List[RegistryBundle]:
        """Search bundles by name or description.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            Matching bundles
        """
        return await self.browse_bundles(search=query, limit=limit)

    async def get_bundle_categories(self) -> List[str]:
        """Get available bundle categories.

        Returns:
            List of categories
        """
        if not self.sdk_integration:
            return []

        try:
            # This would need a categories endpoint in the API
            # For now, return common categories
            return ["security", "compliance", "vulnerability", "code-quality"]
        except Exception:
            return []

    def is_bundle_installed(self, bundle_id: str) -> bool:
        """Check if a bundle is installed.

        Args:
            bundle_id: Bundle identifier

        Returns:
            True if installed
        """
        return self.bundle_cache.is_bundle_cached(bundle_id)

    def get_bundle_info(self, bundle_id: str) -> Optional[Dict[str, Any]]:
        """Get information about an installed bundle.

        Args:
            bundle_id: Bundle identifier

        Returns:
            Bundle information, or None if not installed
        """
        return self.bundle_cache.get_bundle_info(bundle_id)


