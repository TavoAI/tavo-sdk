"""
Scan_Schedules API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Scan_SchedulesClient:
    """Client for scan_schedules endpoints."""

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


    async def post_root(self, schedule_in: Any):
        """POST /"""
        url = f"/"
        params = {}
        data = schedule_in
        return await self._request("POST", url, params=params, json=data)


    async def get_repository_repository_id(self, repository_id: str):
        """GET /repository/{repository_id}"""
        url = f"/repository/{repository_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_schedule_id(self, schedule_id: str):
        """GET /{schedule_id}"""
        url = f"/{schedule_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def put_schedule_id(self, schedule_id: str, schedule_update: Any):
        """PUT /{schedule_id}"""
        url = f"/{schedule_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("PUT", url, params=params, json=data)


    async def delete_schedule_id(self, schedule_id: str):
        """DELETE /{schedule_id}"""
        url = f"/{schedule_id}"
        params = {}
        data = schedule_id
        return await self._request("DELETE", url, params=params, json=data)

