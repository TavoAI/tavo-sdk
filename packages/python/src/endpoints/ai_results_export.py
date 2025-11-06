"""
Ai_Results_Export API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Ai_Results_ExportClient:
    """Client for ai_results_export endpoints."""

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


    async def get_results(self, skip: Optional[float] = None, limit: Optional[float] = None, scan_id: Optional[str] = None, analysis_type: Optional[str] = None, severity: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """GET /results"""
        url = f"/results"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_results_export(self, format: Optional[str] = None, scan_id: Optional[str] = None, analysis_type: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """GET /results/export"""
        url = f"/results/export"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

