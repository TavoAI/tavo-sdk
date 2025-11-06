"""
Jobs API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class JobsClient:
    """Client for jobs endpoints."""

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


    async def get_status_job_id(self, job_id: str):
        """GET /status/{job_id}"""
        url = f"/status/{job_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_dashboard(self, limit: Optional[float] = None, authorization: Optional[str] = None, x_api_key: Optional[str] = None):
        """GET /dashboard"""
        url = f"/dashboard"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

