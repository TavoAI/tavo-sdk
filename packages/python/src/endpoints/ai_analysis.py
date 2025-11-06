"""
Ai_Analysis API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Ai_AnalysisClient:
    """Client for ai_analysis endpoints."""

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


    async def post_analyze_scan_id(self, scan_id: str, background_tasks: Any):
        """POST /analyze/{scan_id}"""
        url = f"/analyze/{scan_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def post_classify_scan_id(self, scan_id: str, background_tasks: Any):
        """POST /classify/{scan_id}"""
        url = f"/classify/{scan_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def post_risk_score_scan_id(self, scan_id: str):
        """POST /risk-score/{scan_id}"""
        url = f"/risk-score/{scan_id}"
        params = {}
        data = scan_id
        return await self._request("POST", url, params=params, json=data)


    async def post_compliance_scan_id(self, scan_id: float, framework: Optional[str] = None):
        """POST /compliance/{scan_id}"""
        url = f"/compliance/{scan_id}"
        params = {}
        data = {", ".join(body_dict)}
        return await self._request("POST", url, params=params, json=data)


    async def post_predictive_scan_id(self, scan_id: str):
        """POST /predictive/{scan_id}"""
        url = f"/predictive/{scan_id}"
        params = {}
        data = scan_id
        return await self._request("POST", url, params=params, json=data)


    async def get_fix_suggestions(self, search: Optional[str] = None, status: Optional[str] = None, severity: Optional[str] = None, analysis_type: Optional[str] = None, limit: Optional[float] = None, offset: Optional[float] = None):
        """GET /fix-suggestions"""
        url = f"/fix-suggestions"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_predictive(self, time_horizon: Optional[str] = None, severity: Optional[str] = None, prediction_type: Optional[str] = None, analysis_type: Optional[str] = None):
        """GET /predictive"""
        url = f"/predictive"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_compliance(self, framework: Optional[str] = None, status: Optional[str] = None, risk_level: Optional[str] = None, category: Optional[str] = None):
        """GET /compliance"""
        url = f"/compliance"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

