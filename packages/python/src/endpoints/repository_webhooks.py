"""
Repository_Webhooks API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Repository_WebhooksClient:
    """Client for repository_webhooks endpoints."""

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


    async def post_github(self, x_hub_signature_256: Optional[str] = None, x_github_event: Optional[str] = None, x_github_delivery: Optional[str] = None):
        """POST /github"""
        url = f"/github"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def post_repository_id_setup(self, repository_id: str):
        """POST /{repository_id}/setup"""
        url = f"/{repository_id}/setup"
        params = {}
        data = repository_id
        return await self._request("POST", url, params=params, json=data)


    async def get_repository_id_status(self, repository_id: str):
        """GET /{repository_id}/status"""
        url = f"/{repository_id}/status"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def delete_repository_id_webhook(self, repository_id: str):
        """DELETE /{repository_id}/webhook"""
        url = f"/{repository_id}/webhook"
        params = {}
        data = repository_id
        return await self._request("DELETE", url, params=params, json=data)

