"""
Registry API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class RegistryClient:
    """Client for registry endpoints."""

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


    async def get_marketplace(self):
        """GET /marketplace"""
        url = f"/marketplace"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_categories(self):
        """GET /categories"""
        url = f"/categories"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_bundles(self, bundle: Any):
        """POST /bundles"""
        url = f"/bundles"
        params = {}
        data = bundle
        return await self._request("POST", url, params=params, json=data)


    async def get_bundles_bundle_id(self, bundle_id: str):
        """GET /bundles/{bundle_id}"""
        url = f"/bundles/{bundle_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def put_bundles_bundle_id(self, bundle_id: str, bundle_update: Any):
        """PUT /bundles/{bundle_id}"""
        url = f"/bundles/{bundle_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("PUT", url, params=params, json=data)


    async def delete_bundles_bundle_id(self, bundle_id: str):
        """DELETE /bundles/{bundle_id}"""
        url = f"/bundles/{bundle_id}"
        params = {}
        data = bundle_id
        return await self._request("DELETE", url, params=params, json=data)


    async def get_bundles_bundle_id_download(self, bundle_id: str):
        """GET /bundles/{bundle_id}/download"""
        url = f"/bundles/{bundle_id}/download"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_bundles_bundle_id_install(self, bundle_id: str, installation: Any):
        """POST /bundles/{bundle_id}/install"""
        url = f"/bundles/{bundle_id}/install"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_my_bundles(self):
        """GET /my-bundles"""
        url = f"/my-bundles"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_execute_code_rule(self):
        """POST /execute/code-rule"""
        url = f"/execute/code-rule"
        params = {}
        data = None
        return await self._request("POST", url, params=params, json=data)


    async def get_executions_execution_id(self, execution_id: str):
        """GET /executions/{execution_id}"""
        url = f"/executions/{execution_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_my_executions(self, page: Optional[float] = None, per_page: Optional[float] = None):
        """GET /my-executions"""
        url = f"/my-executions"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_bundles_bundle_id_rate(self, bundle_id: str, rating: Any):
        """POST /bundles/{bundle_id}/rate"""
        url = f"/bundles/{bundle_id}/rate"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def post_bundles_bundle_id_review(self, bundle_id: str, review: Any):
        """POST /bundles/{bundle_id}/review"""
        url = f"/bundles/{bundle_id}/review"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_bundles_bundle_id_reviews(self, bundle_id: str, page: Optional[float] = None, per_page: Optional[float] = None):
        """GET /bundles/{bundle_id}/reviews"""
        url = f"/bundles/{bundle_id}/reviews"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_bundles_bundle_id_versions(self, bundle_id: str):
        """GET /bundles/{bundle_id}/versions"""
        url = f"/bundles/{bundle_id}/versions"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_bundles_bundle_id_changelog(self, bundle_id: str):
        """GET /bundles/{bundle_id}/changelog"""
        url = f"/bundles/{bundle_id}/changelog"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

