"""
Scan_Management API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Scan_ManagementClient:
    """Client for scan_management endpoints."""

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


    async def post_root(self, scan_in: Any):
        """POST /"""
        url = f"/"
        params = {}
        data = scan_in
        return await self._request("POST", url, params=params, json=data)


    async def get_root(self, skip: Optional[float] = None, limit: Optional[float] = None, status_filter: Optional[str] = None, organization_id: Optional[str] = None):
        """GET /"""
        url = f"/"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_scan_id(self, scan_id: str):
        """GET /{scan_id:uuid}"""
        url = f"/{scan_id:uuid}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_scan_id_results(self, scan_id: str, severity_filter: Optional[str] = None, rule_type_filter: Optional[str] = None, limit: Optional[float] = None):
        """GET /{scan_id:uuid}/results"""
        url = f"/{scan_id:uuid}/results"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_scan_id_cancel(self, scan_id: str):
        """POST /{scan_id:uuid}/cancel"""
        url = f"/{scan_id:uuid}/cancel"
        params = {}
        data = scan_id
        return await self._request("POST", url, params=params, json=data)

