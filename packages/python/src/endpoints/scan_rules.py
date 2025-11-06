"""
Scan_Rules API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Scan_RulesClient:
    """Client for scan_rules endpoints."""

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


    async def post_rules(self, rule_in: Any):
        """POST /rules"""
        url = f"/rules"
        params = {}
        data = rule_in
        return await self._request("POST", url, params=params, json=data)


    async def get_rules(self, skip: Optional[float] = None, limit: Optional[float] = None, tool_filter: Optional[str] = None, category_filter: Optional[str] = None, severity_filter: Optional[str] = None, language_filter: Optional[str] = None, is_active: Optional[bool] = None, organization_id: Optional[str] = None):
        """GET /rules"""
        url = f"/rules"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_rules_rule_id(self, rule_id: str):
        """GET /rules/{rule_id}"""
        url = f"/rules/{rule_id}"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_rules_upload(self, file: Optional[Any] = None, organization_id: Optional[str] = None):
        """POST /rules/upload"""
        url = f"/rules/upload"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def put_rules_rule_id(self, rule_id: str, rule_update: Any):
        """PUT /rules/{rule_id}"""
        url = f"/rules/{rule_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("PUT", url, params=params, json=data)


    async def delete_rules_rule_id(self, rule_id: str):
        """DELETE /rules/{rule_id}"""
        url = f"/rules/{rule_id}"
        params = {}
        data = rule_id
        return await self._request("DELETE", url, params=params, json=data)

