"""
SDK Integration Layer for Tavo Scanner

Provides unified interface to all TavoAI SDK endpoints with error handling and retry logic.
"""

import asyncio
import time
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass
from contextlib import asynccontextmanager

import httpx

from ..python.src.tavo.client import TavoClient
from ..python.src.tavo.scans import ScansClient
from ..python.src.tavo.ai_analysis import Ai_AnalysisClient
from ..python.src.tavo.registry import RegistryClient
from ..python.src.tavo.plugin_marketplace import Plugin_MarketplaceClient
from ..python.src.tavo.repositories import RepositoriesClient
from ..python.src.tavo.jobs import JobsClient
from ..python.src.tavo.health import HealthClient
from ..python.src.tavo.websockets import WebsocketsClient
from ..python.src.tavo.code_submission import Code_SubmissionClient
from ..python.src.tavo.ai_bulk_operations import Ai_Bulk_OperationsClient
from ..python.src.tavo.ai_results_export import Ai_Results_ExportClient

from .auth_manager import AuthManager, AuthCredentials


@dataclass
class SDKConfig:
    """Configuration for SDK integration."""
    base_url: str = "https://api.tavo.ai"
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    enable_websockets: bool = True


class SDKError(Exception):
    """SDK operation error."""
    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}


class SDKIntegration:
    """Unified SDK integration layer for Tavo Scanner."""

    def __init__(self, auth_manager: AuthManager, config: Optional[SDKConfig] = None):
        """Initialize SDK integration.

        Args:
            auth_manager: Authentication manager instance
            config: SDK configuration
        """
        self.auth_manager = auth_manager
        self.config = config or SDKConfig()

        # Initialize HTTP client with auth
        self.http_client = httpx.AsyncClient(
            base_url=self.config.base_url + "/api/v1",
            headers=self.auth_manager.get_auth_headers(),
            timeout=self.config.timeout
        )

        # Initialize SDK clients
        self._init_sdk_clients()

        # WebSocket client (optional)
        self.websocket_client = None
        if self.config.enable_websockets:
            try:
                self.websocket_client = WebsocketsClient(
                    self.config.base_url,
                    self.http_client
                )
            except Exception:
                # Graceful degradation if WebSocket not available
                pass

    def _init_sdk_clients(self) -> None:
        """Initialize all SDK client instances."""
        self.scans = ScansClient(self.config.base_url, self.http_client)
        self.ai_analysis = Ai_AnalysisClient(self.config.base_url, self.http_client)
        self.registry = RegistryClient(self.config.base_url, self.http_client)
        self.plugin_marketplace = Plugin_MarketplaceClient(self.config.base_url, self.http_client)
        self.repositories = RepositoriesClient(self.config.base_url, self.http_client)
        self.jobs = JobsClient(self.config.base_url, self.http_client)
        self.health = HealthClient(self.config.base_url, self.http_client)
        self.code_submission = Code_SubmissionClient(self.config.base_url, self.http_client)
        self.ai_bulk_operations = Ai_Bulk_OperationsClient(self.config.base_url, self.http_client)
        self.ai_results_export = Ai_Results_ExportClient(self.config.base_url, self.http_client)

    async def _retry_request(self, operation, *args, **kwargs):
        """Execute operation with retry logic."""
        last_error = None

        for attempt in range(self.config.max_retries):
            try:
                return await operation(*args, **kwargs)
            except (httpx.TimeoutException, httpx.ConnectError) as e:
                last_error = e
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
            except httpx.HTTPStatusError as e:
                # Don't retry on client errors (4xx)
                if 400 <= e.response.status_code < 500:
                    raise SDKError(
                        f"Request failed: {e.response.status_code} {e.response.reason_phrase}",
                        status_code=e.response.status_code,
                        details={"response": e.response.text}
                    )
                # Retry on server errors (5xx)
                last_error = e
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
                    continue

        raise SDKError(f"Request failed after {self.config.max_retries} attempts: {last_error}")

    async def check_auth(self) -> bool:
        """Check if current authentication is valid."""
        try:
            await self.health.get_health()
            return True
        except Exception:
            return False

    async def get_health_status(self) -> Dict[str, Any]:
        """Get API server health status."""
        try:
            health = await self._retry_request(self.health.get_health)
            return {
                "status": "healthy",
                "details": health,
                "timestamp": time.time()
            }
        except SDKError as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "status_code": e.status_code,
                "timestamp": time.time()
            }

    async def create_scan(self, repository_url: str, **kwargs) -> Dict[str, Any]:
        """Create a new scan."""
        return await self._retry_request(
            self.scans.create,
            repository_url=repository_url,
            **kwargs
        )

    async def get_scan_results(self, scan_id: str) -> Dict[str, Any]:
        """Get scan results."""
        return await self._retry_request(
            self.scans.get_results,
            scan_id=scan_id
        )

    async def submit_ai_analysis(self, code_snippet: str, **kwargs) -> Dict[str, Any]:
        """Submit code for AI analysis."""
        return await self._retry_request(
            self.ai_analysis.analyze_code,
            code=code_snippet,
            **kwargs
        )

    async def browse_registry(self, **kwargs) -> List[Dict[str, Any]]:
        """Browse registry bundles."""
        return await self._retry_request(
            self.registry.get_marketplace,
            **kwargs
        )

    async def install_bundle(self, bundle_id: str) -> Dict[str, Any]:
        """Install a registry bundle."""
        return await self._retry_request(
            self.registry.post_bundles_bundle_id_install,
            bundle_id=bundle_id
        )

    async def download_bundle(self, bundle_id: str) -> Dict[str, Any]:
        """Download bundle details."""
        return await self._retry_request(
            self.registry.get_bundles_bundle_id_download,
            bundle_id=bundle_id
        )

    async def browse_plugins(self, **kwargs) -> List[Dict[str, Any]]:
        """Browse plugin marketplace."""
        return await self._retry_request(
            self.plugin_marketplace.get_marketplace,
            **kwargs
        )

    async def install_plugin(self, plugin_id: str) -> Dict[str, Any]:
        """Install a plugin."""
        return await self._retry_request(
            self.plugin_marketplace.post_plugins_plugin_id_install,
            plugin_id=plugin_id
        )

    async def list_repositories(self) -> List[Dict[str, Any]]:
        """List connected repositories."""
        return await self._retry_request(
            self.repositories.get_repositories
        )

    async def scan_repository(self, repo_id: str, **kwargs) -> Dict[str, Any]:
        """Trigger scan on repository."""
        return await self._retry_request(
            self.repositories.post_repositories_repo_id_scan,
            repo_id=repo_id,
            **kwargs
        )

    async def list_jobs(self, **kwargs) -> List[Dict[str, Any]]:
        """List background jobs."""
        return await self._retry_request(
            self.jobs.get_jobs,
            **kwargs
        )

    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status."""
        return await self._retry_request(
            self.jobs.get_jobs_job_id,
            job_id=job_id
        )

    async def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a job."""
        return await self._retry_request(
            self.jobs.delete_jobs_job_id,
            job_id=job_id
        )

    async def submit_code(self, code: str, **kwargs) -> Dict[str, Any]:
        """Submit code for analysis."""
        return await self._retry_request(
            self.code_submission.post_code,
            code=code,
            **kwargs
        )

    async def bulk_analyze(self, items: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """Submit bulk analysis request."""
        return await self._retry_request(
            self.ai_bulk_operations.post_bulk_analysis,
            items=items,
            **kwargs
        )

    async def export_results(self, scan_id: str, format: str = "json", **kwargs) -> Dict[str, Any]:
        """Export scan results."""
        return await self._retry_request(
            self.ai_results_export.post_export,
            scan_id=scan_id,
            format=format,
            **kwargs
        )

    @asynccontextmanager
    async def websocket_connection(self, scan_id: Optional[str] = None):
        """Context manager for WebSocket connections."""
        if not self.websocket_client:
            raise SDKError("WebSocket client not available")

        try:
            await self.websocket_client.connect()
            if scan_id:
                await self.websocket_client.subscribe_to_scan(scan_id)
            yield self.websocket_client
        finally:
            await self.websocket_client.disconnect()

    async def listen_for_scan_updates(self, scan_id: str, callback):
        """Listen for real-time scan updates."""
        if not self.websocket_client:
            raise SDKError("WebSocket client not available")

        async with self.websocket_connection(scan_id) as ws:
            async for message in ws.listen():
                if message.get('type') == 'scan_update':
                    await callback(message)

    async def close(self) -> None:
        """Close all connections."""
        if self.http_client:
            await self.http_client.aclose()
        if self.websocket_client:
            await self.websocket_client.disconnect()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


