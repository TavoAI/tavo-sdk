"""
Repositories API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class RepositoriesClient:
    """Client for repositories endpoints."""

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


    async def post_sync(self, background_tasks: Any):
        """POST /sync"""
        url = f"/sync"
        params = {}
        data = background_tasks
        return await self._request("POST", url, params=params, json=data)


    async def get_root(self, connection_id: Optional[str] = None, language: Optional[str] = None, scan_enabled: Optional[bool] = None, search: Optional[str] = None, page: Optional[float] = None, per_page: Optional[float] = None):
        """GET /"""
        url = f"/"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_repository_id(self, repository_id: str):
        """GET /{repository_id}"""
        url = f"/{repository_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def put_repository_id(self, repository_id: str, repository_update: Any):
        """PUT /{repository_id}"""
        url = f"/{repository_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("PUT", url, params=params, json=data)


    async def delete_repository_id(self, repository_id: str):
        """DELETE /{repository_id}"""
        url = f"/{repository_id}"
        params = {}
        data = repository_id
        return await self._request("DELETE", url, params=params, json=data)


    async def get_repository_id_scans(self, repository_id: str, limit: Optional[float] = None):
        """GET /{repository_id}/scans"""
        url = f"/{repository_id}/scans"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_repository_id_scan(self, repository_id: str, background_tasks: Any):
        """POST /{repository_id}/scan"""
        url = f"/{repository_id}/scan"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_repository_id_branches(self, repository_id: str):
        """GET /{repository_id}/branches"""
        url = f"/{repository_id}/branches"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_repository_id_pause(self, repository_id: str):
        """POST /{repository_id}/pause"""
        url = f"/{repository_id}/pause"
        params = {}
        data = repository_id
        return await self._request("POST", url, params=params, json=data)


    async def post_repository_id_resume(self, repository_id: str):
        """POST /{repository_id}/resume"""
        url = f"/{repository_id}/resume"
        params = {}
        data = repository_id
        return await self._request("POST", url, params=params, json=data)


    async def get_repository_id_analytics(self, repository_id: str, timeframe: Optional[str] = None):
        """GET /{repository_id}/analytics"""
        url = f"/{repository_id}/analytics"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_repository_id_badge(self, repository_id: str, style: Optional[str] = None):
        """GET /{repository_id}/badge"""
        url = f"/{repository_id}/badge"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_repository_id_activity(self, repository_id: str, limit: Optional[float] = None):
        """GET /{repository_id}/activity"""
        url = f"/{repository_id}/activity"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

