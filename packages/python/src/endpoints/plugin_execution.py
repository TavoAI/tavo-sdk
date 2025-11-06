"""
Plugin_Execution API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Plugin_ExecutionClient:
    """Client for plugin_execution endpoints."""

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


    async def post_execute(self, background_tasks: Any):
        """POST /execute"""
        url = f"/execute"
        params = {}
        data = background_tasks
        return await self._request("POST", url, params=params, json=data)


    async def get_executions_execution_id(self, execution_id: str):
        """GET /executions/{execution_id}"""
        url = f"/executions/{execution_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_executions(self, plugin_id: Optional[str] = None, limit: Optional[float] = None):
        """GET /executions"""
        url = f"/executions"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

