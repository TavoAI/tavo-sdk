"""
Health API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class HealthClient:
    """Client for health endpoints."""

    def __init__(self, base_url: str, client: Optional[httpx.AsyncClient] = None):
        self.base_url = base_url.rstrip('/')
        self.client = client

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """Make HTTP request."""
        url = self.base_url + path
        if self.client:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        else:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()


    async def get_health(self):
        """GET /health"""
        url = f"/health"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_health_ready(self):
        """GET /health/ready"""
        url = f"/health/ready"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_health_live(self):
        """GET /health/live"""
        url = f"/health/live"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)

