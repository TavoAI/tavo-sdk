"""
Ai_Risk_Compliance API Client
"""

from typing import Dict, List, Optional, Any
import httpx


class Ai_Risk_ComplianceClient:
    """Client for ai_risk_compliance endpoints."""

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


    async def get_risk_scores(self, skip: Optional[float] = None, limit: Optional[float] = None, scan_id: Optional[str] = None, min_score: Optional[float] = None, max_score: Optional[float] = None):
        """GET /risk-scores"""
        url = f"/risk-scores"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_compliance_reports(self, skip: Optional[float] = None, limit: Optional[float] = None, scan_id: Optional[str] = None, framework: Optional[str] = None, status: Optional[str] = None):
        """GET /compliance-reports"""
        url = f"/compliance-reports"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)


    async def get_predictive_analyses(self, skip: Optional[float] = None, limit: Optional[float] = None, scan_id: Optional[str] = None, prediction_type: Optional[str] = None, confidence_threshold: Optional[float] = None):
        """GET /predictive-analyses"""
        url = f"/predictive-analyses"
        params = {", ".join(query_dict)}
        data = None
        return await self._request("GET", url, params=params, json=data)

