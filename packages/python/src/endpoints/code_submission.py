"""
Code_Submission API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Code_SubmissionClient:
    """Client for code_submission endpoints."""

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


    async def post_submit_code(self, files: Optional[List[Any]] = None, scan_config: Optional[Any] = None, repository_name: Optional[str] = None, branch: Optional[str] = None, commit_sha: Optional[str] = None):
        """POST /submit/code"""
        url = f"/submit/code"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def post_submit_repository(self, repository_url: Optional[str] = None, snapshot_data: Optional[Any] = None, scan_config: Optional[Any] = None, branch: Optional[str] = None, commit_sha: Optional[str] = None):
        """POST /submit/repository"""
        url = f"/submit/repository"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def post_submit_analysis(self, code_content: Optional[str] = None, language: Optional[str] = None, analysis_type: Optional[str] = None, rules: Optional[List[str]] = None, plugins: Optional[List[str]] = None, context: Optional[Any] = None):
        """POST /submit/analysis"""
        url = f"/submit/analysis"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def get_scans_scan_id_status(self, scan_id: str):
        """GET /scans/{scan_id}/status"""
        url = f"/scans/{scan_id}/status"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_scans_scan_id_results_summary(self, scan_id: str):
        """GET /scans/{scan_id}/results/summary"""
        url = f"/scans/{scan_id}/results/summary"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

