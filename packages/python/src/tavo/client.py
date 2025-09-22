"""Tavo AI API Client"""

import asyncio
from typing import Any, Dict, Optional
import httpx
from pydantic import BaseModel, Field


class TavoConfig(BaseModel):
    """Configuration for Tavo API client"""

    api_key: str = Field(..., description="API key for authentication")
    base_url: str = Field(
        default="https://api.tavo.ai", description="Base URL for API"
    )
    api_version: str = Field(default="v1", description="API version to use")
    timeout: float = Field(
        default=30.0, description="Request timeout in seconds"
    )
    max_retries: int = Field(
        default=3, description="Maximum number of retries"
    )


class TavoClient:
    """Main client for interacting with Tavo AI API"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.tavo.ai",
        api_version: str = "v1",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize Tavo API client

        Args:
            api_key: API key for authentication. If not provided, will look
                for TAVO_API_KEY env var
            base_url: Base URL for the API
            api_version: API version to use
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        if api_key is None:
            import os
            api_key = os.getenv("TAVO_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided or set in TAVO_API_KEY "
                    "environment variable"
                )

        self.config = TavoConfig(
            api_key=api_key,
            base_url=base_url,
            api_version=api_version,
            timeout=timeout,
            max_retries=max_retries,
        )

        self._client = httpx.AsyncClient(
            base_url=f"{base_url}/api/{api_version}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "tavo-python-sdk/0.1.0",
            },
            timeout=timeout,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API"""
        for attempt in range(self.config.max_retries + 1):
            try:
                response = await self._client.request(
                    method=method,
                    url=endpoint,
                    json=data,
                    params=params,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < self.config.max_retries:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
            except httpx.RequestError:
                if attempt < self.config.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise

        raise RuntimeError("Request failed after all retries")

    # Placeholder methods - will be expanded with actual API endpoints
    async def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        return await self._request("GET", "/health")

    def scans(self):
        """Access scan-related operations"""
        return ScanOperations(self)

    def reports(self):
        """Access report-related operations"""
        return ReportOperations(self)


class ScanOperations:
    """Operations for security scans"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def create(self, repository_url: str, **kwargs) -> Dict[str, Any]:
        """Create a new security scan"""
        data = {"repository_url": repository_url, **kwargs}
        return await self._client._request("POST", "/scans", data=data)

    async def get(self, scan_id: str) -> Dict[str, Any]:
        """Get scan details"""
        return await self._client._request("GET", f"/scans/{scan_id}")

    async def list(self, **params) -> Dict[str, Any]:
        """List scans"""
        return await self._client._request("GET", "/scans", params=params)


class ReportOperations:
    """Operations for reports"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def get(self, report_id: str) -> Dict[str, Any]:
        """Get report details"""
        return await self._client._request("GET", f"/reports/{report_id}")

    async def list(self, **params) -> Dict[str, Any]:
        """List reports"""
        return await self._client._request("GET", "/reports", params=params)
