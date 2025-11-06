"""
Plugin_Marketplace API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Plugin_MarketplaceClient:
    """Client for plugin_marketplace endpoints."""

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


    async def get_marketplace(self, plugin_type: Optional[str] = None, category: Optional[str] = None, pricing_tier: Optional[str] = None, search: Optional[str] = None, is_official: Optional[bool] = None, is_vetted: Optional[bool] = None, min_rating: Optional[float] = None, page: Optional[float] = None, per_page: Optional[float] = None, sort_by: Optional[str] = None, sort_order: Optional[str] = None):
        """GET /marketplace"""
        url = f"/marketplace"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_plugin_id(self, plugin_id: str):
        """GET /{plugin_id}"""
        url = f"/{plugin_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_plugin_id_install(self, plugin_id: str, organization_id: Optional[str] = None):
        """POST /{plugin_id}/install"""
        url = f"/{plugin_id}/install"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_plugin_id_download(self, plugin_id: str, version: Optional[str] = None):
        """GET /{plugin_id}/download"""
        url = f"/{plugin_id}/download"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_installed(self):
        """GET /installed"""
        url = f"/installed"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def put_plugin_id(self, plugin_id: str, plugin_data: Any):
        """PUT /{plugin_id}"""
        url = f"/{plugin_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("PUT", url, params=params, json=data)


    async def delete_plugin_id(self, plugin_id: str):
        """DELETE /{plugin_id}"""
        url = f"/{plugin_id}"
        params = {}
        data = plugin_id
        return await self._request("DELETE", url, params=params, json=data)


    async def post_plugin_id_publish(self, plugin_id: str):
        """POST /{plugin_id}/publish"""
        url = f"/{plugin_id}/publish"
        params = {}
        data = plugin_id
        return await self._request("POST", url, params=params, json=data)


    async def post_plugin_id_versions(self, plugin_id: str, version_data: Any):
        """POST /{plugin_id}/versions"""
        url = f"/{plugin_id}/versions"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_plugin_id_versions(self, plugin_id: str):
        """GET /{plugin_id}/versions"""
        url = f"/{plugin_id}/versions"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_plugin_id_reviews(self, plugin_id: str, page: Optional[float] = None, limit: Optional[float] = None, min_rating: Optional[float] = None, sort_by: Optional[str] = None, sort_order: Optional[str] = None):
        """GET /{plugin_id}/reviews"""
        url = f"/{plugin_id}/reviews"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_plugin_id_reviews(self, plugin_id: str, review_data: Any):
        """POST /{plugin_id}/reviews"""
        url = f"/{plugin_id}/reviews"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_plugin_id_reviews_review_id(self, plugin_id: str, review_id: str):
        """GET /{plugin_id}/reviews/{review_id}"""
        url = f"/{plugin_id}/reviews/{review_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def put_plugin_id_reviews_review_id(self, plugin_id: str, review_id: str, review_update: Any):
        """PUT /{plugin_id}/reviews/{review_id}"""
        url = f"/{plugin_id}/reviews/{review_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("PUT", url, params=params, json=data)


    async def delete_plugin_id_reviews_review_id(self, plugin_id: str, review_id: str):
        """DELETE /{plugin_id}/reviews/{review_id}"""
        url = f"/{plugin_id}/reviews/{review_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("DELETE", url, params=params, json=data)


    async def post_plugin_id_reviews_review_id_helpful(self, plugin_id: str, review_id: str):
        """POST /{plugin_id}/reviews/{review_id}/helpful"""
        url = f"/{plugin_id}/reviews/{review_id}/helpful"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)

