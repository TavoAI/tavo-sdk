"""
Dual Distribution Manager for Tavo Scanner

Manages the dual distribution system where:
- Free bundles: Direct access from GitHub (no API key required)
- Paid bundles: Access through TavoAI Registry (API key required)

Handles fallback logic, API key detection, and bundle source selection.
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from urllib.parse import urlparse

try:
    from .bundle_cache import BundleCache
except ImportError:
    # Fallback for direct execution
    from bundle_cache import BundleCache

logger = logging.getLogger(__name__)


@dataclass
class BundleSource:
    """Represents a bundle source location."""

    source_type: str  # "registry", "github", "local"
    location: str  # URL, path, or bundle ID
    version: Optional[str] = None
    requires_api_key: bool = False
    fallback_available: bool = True


@dataclass
class BundleMetadata:
    """Bundle metadata with distribution info."""

    id: str
    name: str
    description: str
    version: str
    pricing_tier: str  # "free", "paid", "enterprise"
    category: str
    tags: List[str]
    source: BundleSource
    github_url: Optional[str] = None  # For free bundles


class DualDistributionManager:
    """
    Manages dual distribution of rule bundles.

    Strategy:
    1. Check if API key is available
    2. For free bundles: Try GitHub first, fallback to registry if available
    3. For paid bundles: Require registry access (API key mandatory)
    4. Cache downloaded bundles locally
    """

    def __init__(
        self,
        registry_manager=None,
        bundle_cache: Optional[BundleCache] = None,
        api_key: Optional[str] = None,
        github_token: Optional[str] = None,
    ):
        """
        Initialize dual distribution manager.

        Args:
            registry_manager: Registry manager instance
            bundle_cache: Bundle cache instance
            api_key: TavoAI API key for registry access
            github_token: GitHub token for higher rate limits (optional)
        """
        self.registry_manager = registry_manager
        self.bundle_cache = bundle_cache or BundleCache()
        self.api_key = api_key or os.getenv("TAVOAI_API_KEY")
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")

        # Known bundle mappings (could be loaded from config)
        self.bundle_mappings = self._load_bundle_mappings()

    def _load_bundle_mappings(self) -> Dict[str, BundleMetadata]:
        """Load bundle mappings from configuration."""
        # This could be loaded from a JSON file or API
        # For now, hardcoded examples
        return {
            # Free bundles available on GitHub
            "owasp-llm-basic": BundleMetadata(
                id="owasp-llm-basic",
                name="OWASP LLM Top 10 Basic",
                description="Heuristic-only OWASP LLM Top 10 rules",
                version="1.0.0",
                pricing_tier="free",
                category="security",
                tags=["owasp", "llm", "ai-security"],
                source=BundleSource(
                    source_type="github",
                    location="TavoAI/tavo-rules/bundles/free/owasp-llm-basic",
                    requires_api_key=False,
                    fallback_available=True,
                ),
                github_url="https://github.com/TavoAI/tavo-rules/tree/main/bundles/free/owasp-llm-basic",
            ),
            "iso-42001-compliance": BundleMetadata(
                id="iso-42001-compliance",
                name="ISO 42001 AI Governance",
                description="Comprehensive AI governance compliance rules",
                version="1.0.0",
                pricing_tier="paid",
                category="compliance",
                tags=["iso-42001", "ai-governance", "compliance"],
                source=BundleSource(
                    source_type="registry",
                    location="iso-42001-compliance",
                    requires_api_key=True,
                    fallback_available=False,
                ),
            ),
            # AI-enhanced bundles (paid)
            "owasp-llm-pro": BundleMetadata(
                id="owasp-llm-pro",
                name="OWASP LLM Top 10 Pro",
                description="AI-enhanced OWASP LLM Top 10 analysis",
                version="1.0.0",
                pricing_tier="paid",
                category="security",
                tags=["owasp", "llm", "ai-enhanced"],
                source=BundleSource(
                    source_type="registry",
                    location="owasp-llm-pro",
                    requires_api_key=True,
                    fallback_available=False,
                ),
            ),
        }

    def has_api_key(self) -> bool:
        """Check if API key is available."""
        return self.api_key is not None and len(self.api_key.strip()) > 0

    def can_access_registry(self) -> bool:
        """Check if registry access is available."""
        return self.has_api_key() and self.registry_manager is not None

    async def load_bundle(
        self, bundle_id: str, version: Optional[str] = None, force_refresh: bool = False
    ) -> Dict[str, Any]:
        """
        Load a bundle using dual distribution strategy.

        Args:
            bundle_id: Bundle identifier
            version: Specific version (optional)
            force_refresh: Force re-download even if cached

        Returns:
            Bundle data

        Raises:
            ValueError: If bundle cannot be loaded
        """
        logger.info(f"Loading bundle: {bundle_id}")

        # Get bundle metadata
        if bundle_id not in self.bundle_mappings:
            raise ValueError(f"Unknown bundle: {bundle_id}")

        bundle_meta = self.bundle_mappings[bundle_id]

        # Check cache first (unless force refresh)
        if not force_refresh:
            cached_bundle = self.bundle_cache.get_cached_bundle(bundle_id, version)
            if cached_bundle:
                logger.info(f"Loaded bundle from cache: {bundle_id}")
                return cached_bundle

        # Determine access strategy based on pricing tier and API key availability
        if bundle_meta.pricing_tier == "free":
            return await self._load_free_bundle(bundle_meta, version)
        else:
            return await self._load_paid_bundle(bundle_meta, version)

    async def _load_free_bundle(
        self, bundle_meta: BundleMetadata, version: Optional[str]
    ) -> Dict[str, Any]:
        """
        Load a free bundle.

        Strategy:
        1. Try GitHub direct access first
        2. Fallback to registry if available and API key present
        """
        logger.info(f"Loading free bundle: {bundle_meta.id}")

        # Try GitHub first
        try:
            bundle_data = await self._load_from_github(bundle_meta, version)
            logger.info(f"Successfully loaded bundle from GitHub: {bundle_meta.id}")
            return bundle_data
        except Exception as e:
            logger.warning(f"Failed to load from GitHub: {e}")

            # Fallback to registry if available
            if self.can_access_registry():
                try:
                    bundle_data = await self._load_from_registry(bundle_meta, version)
                    logger.info(
                        f"Successfully loaded bundle from registry fallback: {bundle_meta.id}"
                    )
                    return bundle_data
                except Exception as e2:
                    logger.error(f"Registry fallback also failed: {e2}")

            # Show helpful message for free bundles
            raise ValueError(
                f"Unable to load free bundle '{bundle_meta.id}' from GitHub. "
                f"Please check your internet connection or try again later. "
                f"GitHub URL: {bundle_meta.github_url}"
            )

    async def _load_paid_bundle(
        self, bundle_meta: BundleMetadata, version: Optional[str]
    ) -> Dict[str, Any]:
        """
        Load a paid bundle.

        Strategy:
        1. Require registry access and API key
        2. No fallback to GitHub for paid bundles
        """
        logger.info(f"Loading paid bundle: {bundle_meta.id}")

        if not self.can_access_registry():
            raise ValueError(
                f"Bundle '{bundle_meta.id}' requires a TavoAI API key for access. "
                f"This is a {bundle_meta.pricing_tier} bundle. "
                f"Please set your TAVOAI_API_KEY environment variable or "
                f"contact sales@tavoai.net for access."
            )

        try:
            bundle_data = await self._load_from_registry(bundle_meta, version)
            logger.info(
                f"Successfully loaded paid bundle from registry: {bundle_meta.id}"
            )
            return bundle_data
        except Exception as e:
            logger.error(f"Failed to load paid bundle from registry: {e}")
            raise ValueError(
                f"Unable to load paid bundle '{bundle_meta.id}' from registry. "
                f"Please check your API key and internet connection."
            )

    async def _load_from_github(
        self, bundle_meta: BundleMetadata, version: Optional[str]
    ) -> Dict[str, Any]:
        """
        Load bundle directly from GitHub.

        Uses GitHub's raw content API to fetch bundle files.
        """
        if not bundle_meta.github_url:
            raise ValueError(f"No GitHub URL configured for bundle: {bundle_meta.id}")

        # Parse GitHub URL to construct raw API URLs
        # Example: https://github.com/TavoAI/tavo-rules/tree/main/bundles/free/owasp-llm-basic
        # Raw URL: https://raw.githubusercontent.com/TavoAI/tavo-rules/main/bundles/free/owasp-llm-basic/

        parsed = urlparse(bundle_meta.github_url)
        if "github.com" not in parsed.netloc:
            raise ValueError(f"Invalid GitHub URL: {bundle_meta.github_url}")

        # Extract owner/repo/path from URL
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 5:  # owner/repo/tree/branch/path...
            raise ValueError(f"Invalid GitHub URL format: {bundle_meta.github_url}")

        owner = path_parts[0]
        repo = path_parts[1]
        branch = path_parts[3]  # Assuming 'main' or 'master'
        bundle_path = "/".join(path_parts[4:])

        # Construct raw GitHub URL
        raw_base_url = (
            f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{bundle_path}"
        )

        # Try to load bundle manifest first
        manifest_url = f"{raw_base_url}/index.json"
        headers = {}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(manifest_url, headers=headers) as response:
                    if response.status == 200:
                        manifest_data = await response.json()
                        # Load all rule files referenced in manifest
                        bundle_data = await self._load_bundle_files_from_github(
                            raw_base_url, manifest_data, headers
                        )
                        return bundle_data
                    elif response.status == 404:
                        # No manifest, try to load as single file
                        return await self._load_single_file_from_github(
                            raw_base_url, bundle_meta, headers
                        )
                    else:
                        raise Exception(f"GitHub API error: {response.status}")

        except ImportError:
            # Fallback to synchronous requests if aiohttp not available
            return self._load_from_github_sync(raw_base_url, bundle_meta, headers)

    async def _load_bundle_files_from_github(
        self, base_url: str, manifest: Dict[str, Any], headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """Load bundle files from GitHub based on manifest."""
        import aiohttp

        bundle_data = {
            "id": manifest.get("id"),
            "name": manifest.get("name"),
            "version": manifest.get("version", "1.0.0"),
            "description": manifest.get("description"),
            "rules": [],
        }

        async with aiohttp.ClientSession() as session:
            for rule_file in manifest.get("rules", []):
                rule_url = f"{base_url}/rules/{rule_file}"
                try:
                    async with session.get(rule_url, headers=headers) as response:
                        if response.status == 200:
                            rule_content = await response.text()
                            # Parse YAML/JSON rule content
                            if rule_file.endswith(".yaml") or rule_file.endswith(
                                ".yml"
                            ):
                                import yaml

                                rule_data = yaml.safe_load(rule_content)
                            elif rule_file.endswith(".json"):
                                rule_data = json.loads(rule_content)
                            else:
                                continue

                            bundle_data["rules"].append(rule_data)
                        else:
                            logger.warning(f"Failed to load rule file: {rule_file}")
                except Exception as e:
                    logger.warning(f"Error loading rule {rule_file}: {e}")

        return bundle_data

    async def _load_single_file_from_github(
        self, base_url: str, bundle_meta: BundleMetadata, headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """Load single bundle file from GitHub."""
        import aiohttp

        # Try common file names
        file_names = ["rules.yaml", "bundle.yaml", "index.yaml", "rules.yml"]

        async with aiohttp.ClientSession() as session:
            for file_name in file_names:
                file_url = f"{base_url}/{file_name}"
                try:
                    async with session.get(file_url, headers=headers) as response:
                        if response.status == 200:
                            content = await response.text()
                            if file_name.endswith(".yaml") or file_name.endswith(
                                ".yml"
                            ):
                                import yaml

                                bundle_data = yaml.safe_load(content)
                            else:
                                bundle_data = json.loads(content)

                            # Add metadata
                            bundle_data.update(
                                {
                                    "id": bundle_meta.id,
                                    "name": bundle_meta.name,
                                    "version": bundle_meta.version,
                                    "source": "github",
                                }
                            )

                            return bundle_data
                except Exception as e:
                    logger.debug(f"Failed to load {file_name}: {e}")
                    continue

        raise Exception("No valid bundle file found on GitHub")

    def _load_from_github_sync(
        self, base_url: str, bundle_meta: BundleMetadata, headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """Synchronous fallback for GitHub loading."""
        import requests

        # Try to load manifest
        manifest_url = f"{base_url}/index.json"
        response = requests.get(manifest_url, headers=headers, timeout=30)

        if response.status_code == 200:
            manifest = response.json()
            # Load synchronously (simplified version)
            bundle_data = {
                "id": manifest.get("id"),
                "name": manifest.get("name"),
                "version": manifest.get("version", "1.0.0"),
                "rules": [],
            }
            return bundle_data
        else:
            raise Exception(f"Failed to load from GitHub: {response.status_code}")

    async def _load_from_registry(
        self, bundle_meta: BundleMetadata, version: Optional[str]
    ) -> Dict[str, Any]:
        """Load bundle from TavoAI Registry."""
        if not self.registry_manager:
            raise Exception("Registry manager not available")

        try:
            # Use registry manager to download bundle
            bundle_data = await self.registry_manager.download_bundle(
                bundle_meta.id, version=version
            )

            # Cache the bundle
            self.bundle_cache.cache_bundle(bundle_meta.id, bundle_data)

            return bundle_data

        except Exception as e:
            logger.error(f"Registry download failed: {e}")
            raise

    def list_available_bundles(self) -> List[BundleMetadata]:
        """List all available bundles (both free and paid)."""
        # Return all bundles - access control is handled during loading
        return list(self.bundle_mappings.values())

    def get_bundle_info(self, bundle_id: str) -> Optional[BundleMetadata]:
        """Get information about a specific bundle."""
        return self.bundle_mappings.get(bundle_id)

    def show_access_message(self, bundle_id: str) -> str:
        """Generate appropriate access message for a bundle."""
        bundle_meta = self.get_bundle_info(bundle_id)
        if not bundle_meta:
            return f"Bundle '{bundle_id}' not found."

        if bundle_meta.pricing_tier == "free":
            if bundle_meta.github_url:
                return f"Free bundle available at: {bundle_meta.github_url}"
            else:
                return "Free bundle available for download."
        else:
            if self.has_api_key():
                return "Paid bundle available with your API key."
            else:
                return (
                    f"This is a {bundle_meta.pricing_tier} bundle. "
                    "Please set your TAVOAI_API_KEY environment variable or "
                    "contact sales@tavoai.net for access."
                )
