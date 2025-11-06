"""
Device_Auth API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Device_AuthClient:
    """Client for device_auth endpoints."""

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


    async def post_code(self, client_id: Optional[str] = None, client_name: Optional[str] = None):
        """POST /code"""
        url = f"/code"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def post_token(self, device_code: str):
        """POST /token"""
        url = f"/token"
        params = {}
        data = device_code
        return await self._request("POST", url, params=params, json=data)


    async def get_info(self, user_code: str):
        """GET /info"""
        url = f"/info"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def post_approve(self):
        """POST /approve"""
        url = f"/approve"
        params = {}
        data = None
        return await self._request("POST", url, params=params, json=data)


    async def post_code_cli(self, client_name: Optional[str] = None):
        """POST /code/cli"""
        url = f"/code/cli"
        params = {}
        data = client_name
        return await self._request("POST", url, params=params, json=data)


    async def get_code_device_code_status(self, device_code: str):
        """GET /code/{device_code}/status"""
        url = f"/code/{device_code}/status"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_usage_warnings(self):
        """GET /usage/warnings"""
        url = f"/usage/warnings"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_limits(self):
        """GET /limits"""
        url = f"/limits"
        params = {}
        data = None
        return await self._request("GET", url, params=params, json=data)

