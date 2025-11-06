"""
Ai_Analysis_Core API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Ai_Analysis_CoreClient:
    """Client for ai_analysis_core endpoints."""

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


    async def get_analyses(self, skip: Optional[float] = None, limit: Optional[float] = None, scan_id: Optional[str] = None, analysis_type: Optional[str] = None, status: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """GET /analyses"""
        url = f"/analyses"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_analyses_analysis_id(self, analysis_id: str):
        """GET /analyses/{analysis_id}"""
        url = f"/analyses/{analysis_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

