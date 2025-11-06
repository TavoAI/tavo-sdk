"""
Scan_Tools API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Scan_ToolsClient:
    """Client for scan_tools endpoints."""

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


    async def get_tools(self, active_only: Optional[bool] = None):
        """GET /tools"""
        url = f"/tools"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_tools_tool_name(self, tool_name: str):
        """GET /tools/{tool_name}"""
        url = f"/tools/{tool_name}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_templates(self, tool: Optional[str] = None, category: Optional[str] = None, language: Optional[str] = None, active_only: Optional[bool] = None):
        """GET /templates"""
        url = f"/templates"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_templates_template_id(self, template_id: str):
        """GET /templates/{template_id}"""
        url = f"/templates/{template_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_validate_configuration(self):
        """POST /validate-configuration"""
        url = f"/validate-configuration"
        params = {}
        data = None
        return await self._request("POST", url, params=params, json=data)


    async def get_repositories_repository_id_settings(self, repository_id: str):
        """GET /repositories/{repository_id}/settings"""
        url = f"/repositories/{repository_id}/settings"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def put_repositories_repository_id_settings(self, repository_id: str, settings: Any):
        """PUT /repositories/{repository_id}/settings"""
        url = f"/repositories/{repository_id}/settings"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("PUT", url, params=params, json=data)


    async def post_validate_access(self):
        """POST /validate-access"""
        url = f"/validate-access"
        params = {}
        data = None
        return await self._request("POST", url, params=params, json=data)

