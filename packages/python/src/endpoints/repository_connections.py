"""
Repository_Connections API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Repository_ConnectionsClient:
    """Client for repository_connections endpoints."""

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


    async def post_root(self, connection_in: Any):
        """POST /"""
        url = f"/"
        params = {}
        data = connection_in
        return await self._request("POST", url, params=params, json=data)


    async def get_root(self, provider_id: Optional[str] = None, connection_type: Optional[str] = None, is_active: Optional[bool] = None):
        """GET /"""
        url = f"/"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_connection_id(self, connection_id: str):
        """GET /{connection_id}"""
        url = f"/{connection_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def put_connection_id(self, connection_id: str, connection_update: Any):
        """PUT /{connection_id}"""
        url = f"/{connection_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("PUT", url, params=params, json=data)


    async def delete_connection_id(self, connection_id: str):
        """DELETE /{connection_id}"""
        url = f"/{connection_id}"
        params = {}
        data = connection_id
        return await self._request("DELETE", url, params=params, json=data)


    async def post_connection_id_validate(self, connection_id: str):
        """POST /{connection_id}/validate"""
        url = f"/{connection_id}/validate"
        params = {}
        data = connection_id
        return await self._request("POST", url, params=params, json=data)


    async def post_connection_id_refresh(self, connection_id: str):
        """POST /{connection_id}/refresh"""
        url = f"/{connection_id}/refresh"
        params = {}
        data = connection_id
        return await self._request("POST", url, params=params, json=data)

