"""
Scan_Bulk_Operations API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Scan_Bulk_OperationsClient:
    """Client for scan_bulk_operations endpoints."""

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


    async def post_bulk_initiate(self, scan_requests: List[Any]):
        """POST /bulk/initiate"""
        url = f"/bulk/initiate"
        params = {}
        data = scan_requests
        return await self._request("POST", url, params=params, json=data)


    async def post_bulk_cancel(self, scan_ids: List[str]):
        """POST /bulk/cancel"""
        url = f"/bulk/cancel"
        params = {}
        data = scan_ids
        return await self._request("POST", url, params=params, json=data)


    async def delete_bulk_delete(self, scan_ids: List[str]):
        """DELETE /bulk/delete"""
        url = f"/bulk/delete"
        params = {}
        data = scan_ids
        return await self._request("DELETE", url, params=params, json=data)


    async def get_bulk_status(self, scan_ids: Optional[List[str]] = None, organization_id: Optional[str] = None, status_filter: Optional[str] = None, limit: Optional[float] = None):
        """GET /bulk/status"""
        url = f"/bulk/status"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

