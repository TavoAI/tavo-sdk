"""
Bundle Cache for Tavo Scanner

Manages local caching of downloaded bundles with versioning and cleanup.
"""

import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """Cache entry metadata."""
    bundle_id: str
    version: str
    path: Path
    downloaded_at: float
    size_bytes: int
    checksum: str


class BundleCache:
    """Local cache for registry bundles."""

    def __init__(self, cache_dir: Optional[Path] = None, max_size_mb: int = 500, ttl_days: int = 7):
        """Initialize bundle cache.

        Args:
            cache_dir: Cache directory (default: ~/.tavoai/bundles)
            max_size_mb: Maximum cache size in MB
            ttl_days: Time-to-live for cached bundles in days
        """
        self.cache_dir = cache_dir or Path.home() / ".tavoai" / "bundles"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.ttl_seconds = ttl_days * 24 * 60 * 60

        self.metadata_file = self.cache_dir / "cache_metadata.json"
        self._load_metadata()

    def _load_metadata(self) -> None:
        """Load cache metadata."""
        if not self.metadata_file.exists():
            self.metadata = {}
            return

        try:
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.metadata = {}

    def _save_metadata(self) -> None:
        """Save cache metadata."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate checksum for bundle data."""
        # Create a stable string representation for checksum
        content = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _get_bundle_path(self, bundle_id: str, version: str) -> Path:
        """Get path for cached bundle."""
        return self.cache_dir / f"{bundle_id}-{version}.json"

    def cache_bundle(self, bundle_id: str, bundle_data: Dict[str, Any]) -> Path:
        """Cache a bundle locally.

        Args:
            bundle_id: Bundle identifier
            bundle_data: Bundle data

        Returns:
            Path to cached bundle
        """
        version = bundle_data.get("version", "latest")
        checksum = self._calculate_checksum(bundle_data)

        # Check if already cached with same checksum
        if bundle_id in self.metadata:
            existing = self.metadata[bundle_id]
            if existing["checksum"] == checksum:
                return Path(existing["path"])

        # Save bundle to file
        bundle_path = self._get_bundle_path(bundle_id, version)
        with open(bundle_path, 'w') as f:
            json.dump(bundle_data, f, indent=2)

        # Update metadata
        size_bytes = bundle_path.stat().st_size
        self.metadata[bundle_id] = {
            "version": version,
            "path": str(bundle_path),
            "downloaded_at": time.time(),
            "size_bytes": size_bytes,
            "checksum": checksum
        }
        self._save_metadata()

        # Cleanup old entries
        self._cleanup_expired()
        self._enforce_size_limit()

        return bundle_path

    def get_cached_bundle(self, bundle_id: str) -> Optional[Path]:
        """Get path to cached bundle.

        Args:
            bundle_id: Bundle identifier

        Returns:
            Path to cached bundle, or None if not cached
        """
        if bundle_id not in self.metadata:
            return None

        bundle_path = Path(self.metadata[bundle_id]["path"])
        if bundle_path.exists():
            return bundle_path

        # Remove stale metadata entry
        del self.metadata[bundle_id]
        self._save_metadata()
        return None

    def is_bundle_cached(self, bundle_id: str) -> bool:
        """Check if bundle is cached.

        Args:
            bundle_id: Bundle identifier

        Returns:
            True if cached
        """
        return self.get_cached_bundle(bundle_id) is not None

    def get_bundle_info(self, bundle_id: str) -> Optional[Dict[str, Any]]:
        """Get information about cached bundle.

        Args:
            bundle_id: Bundle identifier

        Returns:
            Bundle information, or None if not cached
        """
        if bundle_id not in self.metadata:
            return None

        info = self.metadata[bundle_id].copy()
        info["path"] = Path(info["path"])
        return info

    def list_cached_bundles(self) -> List[Dict[str, Any]]:
        """List all cached bundles.

        Returns:
            List of bundle information
        """
        bundles = []
        for bundle_id, info in self.metadata.items():
            bundle_info = info.copy()
            bundle_info["id"] = bundle_id
            bundle_info["path"] = Path(bundle_info["path"])
            bundle_info["age_days"] = (time.time() - bundle_info["downloaded_at"]) / (24 * 60 * 60)
            bundles.append(bundle_info)

        return sorted(bundles, key=lambda x: x["downloaded_at"], reverse=True)

    def remove_bundle(self, bundle_id: str) -> bool:
        """Remove a bundle from cache.

        Args:
            bundle_id: Bundle identifier

        Returns:
            True if removed, False if not found
        """
        if bundle_id not in self.metadata:
            return False

        # Remove file
        bundle_path = Path(self.metadata[bundle_id]["path"])
        if bundle_path.exists():
            bundle_path.unlink()

        # Remove metadata
        del self.metadata[bundle_id]
        self._save_metadata()

        return True

    def _cleanup_expired(self) -> None:
        """Remove expired cache entries."""
        current_time = time.time()
        expired = []

        for bundle_id, info in self.metadata.items():
            if current_time - info["downloaded_at"] > self.ttl_seconds:
                expired.append(bundle_id)

        for bundle_id in expired:
            self.remove_bundle(bundle_id)

    def _enforce_size_limit(self) -> None:
        """Enforce cache size limit by removing oldest entries."""
        # Calculate current size
        total_size = sum(info["size_bytes"] for info in self.metadata.values())

        if total_size <= self.max_size_bytes:
            return

        # Sort by access time (oldest first)
        sorted_entries = sorted(
            self.metadata.items(),
            key=lambda x: x[1]["downloaded_at"]
        )

        # Remove oldest entries until under limit
        for bundle_id, info in sorted_entries:
            if total_size <= self.max_size_bytes:
                break

            total_size -= info["size_bytes"]
            self.remove_bundle(bundle_id)

    def clear_cache(self) -> None:
        """Clear entire cache."""
        for bundle_id in list(self.metadata.keys()):
            self.remove_bundle(bundle_id)

        # Remove metadata file
        if self.metadata_file.exists():
            self.metadata_file.unlink()

        self.metadata = {}

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.

        Returns:
            Cache statistics
        """
        total_size = sum(info["size_bytes"] for info in self.metadata.values())
        bundle_count = len(self.metadata)

        # Calculate size distribution
        size_mb = total_size / (1024 * 1024)
        max_size_mb = self.max_size_bytes / (1024 * 1024)

        return {
            "bundle_count": bundle_count,
            "total_size_mb": round(size_mb, 2),
            "max_size_mb": max_size_mb,
            "usage_percent": round((size_mb / max_size_mb) * 100, 1) if max_size_mb > 0 else 0,
            "cache_dir": str(self.cache_dir),
            "ttl_days": self.ttl_seconds / (24 * 60 * 60)
        }

    def refresh_bundle(self, bundle_id: str) -> bool:
        """Refresh bundle cache entry timestamp.

        Args:
            bundle_id: Bundle identifier

        Returns:
            True if refreshed, False if not cached
        """
        if bundle_id not in self.metadata:
            return False

        self.metadata[bundle_id]["downloaded_at"] = time.time()
        self._save_metadata()
        return True


