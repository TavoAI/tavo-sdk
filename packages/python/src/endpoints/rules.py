"""
Rules API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class RulesClient:
    """Client for rules endpoints."""

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


    async def get_bundles(self, category: Optional[str] = None, official_only: Optional[bool] = None, page: Optional[float] = None, per_page: Optional[float] = None):
        """GET /bundles"""
        url = f"/bundles"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_bundles_bundle_id_install(self, bundle_id: str, installation: Any):
        """POST /bundles/{bundle_id}/install"""
        url = f"/bundles/{bundle_id}/install"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_bundles_bundle_id_rules(self, bundle_id: str):
        """GET /bundles/{bundle_id}/rules"""
        url = f"/bundles/{bundle_id}/rules"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_validate(self):
        """POST /validate"""
        url = f"/validate"
        params = {}
        data = None
        return await self._request("POST", url, params=params, json=data)


    async def get_updates(self):
        """GET /updates"""
        url = f"/updates"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def delete_bundles_bundle_id_install(self, bundle_id: str):
        """DELETE /bundles/{bundle_id}/install"""
        url = f"/bundles/{bundle_id}/install"
        params = {}
        data = bundle_id
        return await self._request("DELETE", url, params=params, json=data)


    async def get_organizations_organization_id_bundles(self, organization_id: str):
        """GET /organizations/{organization_id}/bundles"""
        url = f"/organizations/{organization_id}/bundles"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_organizations_organization_id_bundles_bundle_id_install(self, organization_id: str, bundle_id: str):
        """POST /organizations/{organization_id}/bundles/{bundle_id}/install"""
        url = f"/organizations/{organization_id}/bundles/{bundle_id}/install"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def delete_organizations_organization_id_bundles_bundle_id(self, organization_id: str, bundle_id: str):
        """DELETE /organizations/{organization_id}/bundles/{bundle_id}"""
        url = f"/organizations/{organization_id}/bundles/{bundle_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("DELETE", url, params=params, json=data)


    async def get_organizations_organization_id_rules(self, organization_id: str, category: Optional[str] = None, severity: Optional[str] = None):
        """GET /organizations/{organization_id}/rules"""
        url = f"/organizations/{organization_id}/rules"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_organizations_organization_id_rules_stats(self, organization_id: str):
        """GET /organizations/{organization_id}/rules/stats"""
        url = f"/organizations/{organization_id}/rules/stats"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

