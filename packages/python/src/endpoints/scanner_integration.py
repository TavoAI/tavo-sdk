"""
Scanner_Integration API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Scanner_IntegrationClient:
    """Client for scanner_integration endpoints."""

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


    async def get_rules_discover(self, category: Optional[str] = None, language: Optional[str] = None, scanner_type: Optional[str] = None, limit: Optional[float] = None):
        """GET /rules/discover"""
        url = f"/rules/discover"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_rules_bundle_bundle_id_rules(self, bundle_id: str, severity: Optional[str] = None, language: Optional[str] = None, limit: Optional[float] = None):
        """GET /rules/bundle/{bundle_id}/rules"""
        url = f"/rules/bundle/{bundle_id}/rules"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_rules_bundle_bundle_id_use(self, bundle_id: str, scan_id: Optional[str] = None):
        """POST /rules/bundle/{bundle_id}/use"""
        url = f"/rules/bundle/{bundle_id}/use"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_plugins_discover(self, plugin_type: Optional[str] = None, language: Optional[str] = None, scanner_integration: Optional[bool] = None, limit: Optional[float] = None):
        """GET /plugins/discover"""
        url = f"/plugins/discover"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_plugins_plugin_id_config(self, plugin_id: str):
        """GET /plugins/{plugin_id}/config"""
        url = f"/plugins/{plugin_id}/config"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_scanner_heartbeat(self, scanner_version: str, scanner_type: Optional[str] = None, active_rules: Optional[List[str]] = None, active_plugins: Optional[List[str]] = None):
        """POST /scanner/heartbeat"""
        url = f"/scanner/heartbeat"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_scanner_recommendations(self, scanner_type: Optional[str] = None, current_rules: Optional[List[str]] = None, current_plugins: Optional[List[str]] = None):
        """GET /scanner/recommendations"""
        url = f"/scanner/recommendations"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

