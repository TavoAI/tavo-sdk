"""
Ai_Bulk_Operations API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Ai_Bulk_OperationsClient:
    """Client for ai_bulk_operations endpoints."""

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


    async def delete_bulk_delete(self, analysis_ids: Optional[List[str]] = None):
        """DELETE /bulk/delete"""
        url = f"/bulk/delete"
        params = {}
        data = analysis_ids
        return await self._request("DELETE", url, params=params, json=data)


    async def put_bulk_update_status(self, analysis_updates: Optional[List[Any]] = None):
        """PUT /bulk/update-status"""
        url = f"/bulk/update-status"
        params = {}
        data = analysis_updates
        return await self._request("PUT", url, params=params, json=data)


    async def get_bulk_export(self, analysis_ids: Optional[List[str]] = None, export_format: Optional[str] = None):
        """GET /bulk/export"""
        url = f"/bulk/export"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

