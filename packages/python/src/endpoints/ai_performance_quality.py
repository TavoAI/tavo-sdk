"""
Ai_Performance_Quality API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Ai_Performance_QualityClient:
    """Client for ai_performance_quality endpoints."""

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


    async def get_performance_metrics(self, start_date: Optional[str] = None, end_date: Optional[str] = None, analysis_type: Optional[str] = None):
        """GET /performance-metrics"""
        url = f"/performance-metrics"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_quality_review_scan_id(self, scan_id: str):
        """GET /quality-review/{scan_id}"""
        url = f"/quality-review/{scan_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

