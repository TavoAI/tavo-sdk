"""Tavo AI API Client"""

import asyncio
from typing import Any, Dict, Optional
import httpx
from pydantic import BaseModel, Field


class TavoConfig(BaseModel):
    """Configuration for Tavo API client"""

    api_key: Optional[str] = Field(
        default=None, description="API key for authentication"
    )
    jwt_token: Optional[str] = Field(
        default=None, description="JWT token for authentication"
    )
    base_url: str = Field(
        default="https://api.tavo.ai", description="Base URL for API"
    )
    api_version: str = Field(default="v1", description="API version to use")
    timeout: float = Field(
        default=30.0, description="Request timeout in seconds"
    )
    max_retries: int = Field(
        default=3, description="Maximum number of retries"
    )


class TavoClient:
    """Main client for interacting with Tavo AI API"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        jwt_token: Optional[str] = None,
        base_url: str = "https://api.tavo.ai",
        api_version: str = "v1",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize Tavo API client

        Args:
            api_key: API key for authentication. If not provided, will look
                for TAVO_API_KEY env var
            jwt_token: JWT token for authentication
            base_url: Base URL for the API
            api_version: API version to use
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        # Handle authentication - prefer JWT token over API key
        if jwt_token is None and api_key is None:
            import os
            api_key = os.getenv("TAVO_API_KEY")
            jwt_token = os.getenv("TAVO_JWT_TOKEN")

        if jwt_token is None and api_key is None:
            raise ValueError(
                "Either API key or JWT token must be provided, or set "
                "TAVO_API_KEY or TAVO_JWT_TOKEN environment variables"
            )

        self.config = TavoConfig(
            api_key=api_key,
            jwt_token=jwt_token,
            base_url=base_url,
            api_version=api_version,
            timeout=timeout,
            max_retries=max_retries,
        )

        self._client = httpx.AsyncClient(
            base_url=f"{base_url}/api/{api_version}",
            headers=self._get_auth_headers(),
            timeout=timeout,
        )

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers based on available credentials"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "tavo-python-sdk/0.1.0",
        }

        if self.config.jwt_token:
            headers["Authorization"] = f"Bearer {self.config.jwt_token}"
        elif self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        return headers

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API"""
        for attempt in range(self.config.max_retries + 1):
            try:
                response = await self._client.request(
                    method=method,
                    url=endpoint,
                    json=data,
                    params=params,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if (e.response.status_code >= 500 and
                        attempt < self.config.max_retries):
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
            except httpx.RequestError:
                if attempt < self.config.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise

        raise RuntimeError("Request failed after all retries")

    # Placeholder methods - will be expanded with actual API endpoints
    async def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        return await self._request("GET", "/health")

    # Authentication methods
    def auth(self):
        """Access authentication operations"""
        return AuthOperations(self)

    def users(self):
        """Access user management operations"""
        return UserOperations(self)

    def organizations(self):
        """Access organization operations"""
        return OrganizationOperations(self)

    def jobs(self):
        """Access job operations"""
        return JobOperations(self)

    def scans(self):
        """Access scan-related operations"""
        return ScanOperations(self)

    def webhooks(self):
        """Access webhook operations"""
        return WebhookOperations(self)

    def ai(self):
        """Access AI analysis operations"""
        return AIAnalysisOperations(self)

    def billing(self):
        """Access billing operations"""
        return BillingOperations(self)

    def reports(self):
        """Access report operations"""
        return ReportOperations(self)


class ScanOperations:
    """Operations for security scans"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def create(self, repository_url: str, **kwargs) -> Dict[str, Any]:
        """Create a new security scan"""
        data = {"repository_url": repository_url, **kwargs}
        return await self._client._request("POST", "/scans", data=data)

    async def get(self, scan_id: str) -> Dict[str, Any]:
        """Get scan details"""
        return await self._client._request("GET", f"/scans/{scan_id}")

    async def list(self, **params) -> Dict[str, Any]:
        """List scans"""
        return await self._client._request("GET", "/scans", params=params)

    async def results(self, scan_id: str, **params) -> Dict[str, Any]:
        """Get scan results"""
        return await self._client._request(
            "GET", f"/scans/{scan_id}/results", params=params
        )

    async def cancel(self, scan_id: str) -> Dict[str, Any]:
        """Cancel a running scan"""
        return await self._client._request("POST", f"/scans/{scan_id}/cancel")

    def rules(self):
        """Access scan rules operations"""
        return ScanRuleOperations(self._client)


class AuthOperations:
    """Authentication operations"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and get JWT token"""
        data = {"username": username, "password": password}
        return await self._client._request("POST", "/auth/login", data=data)

    async def register(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new user"""
        return await self._client._request(
            "POST", "/auth/register", data=user_data
        )

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh JWT token"""
        data = {"refresh_token": refresh_token}
        return await self._client._request("POST", "/auth/refresh", data=data)

    async def me(self) -> Dict[str, Any]:
        """Get current user information"""
        return await self._client._request("GET", "/auth/me")


class UserOperations:
    """User management operations"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user (admin only)"""
        return await self._client._request("POST", "/users", data=user_data)

    async def list(self) -> Dict[str, Any]:
        """List all users (admin only)"""
        return await self._client._request("GET", "/users")

    async def get(self, user_id: str) -> Dict[str, Any]:
        """Get user details"""
        return await self._client._request("GET", f"/users/{user_id}")

    async def update(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user information"""
        return await self._client._request(
            "PUT", f"/users/{user_id}", data=user_data
        )

    async def get_me(self) -> Dict[str, Any]:
        """Get current user profile"""
        return await self._client._request("GET", "/users/me")

    async def update_me(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update current user profile"""
        return await self._client._request("PUT", "/users/me", data=user_data)

    def api_keys(self):
        """Access API key operations"""
        return APIKeyOperations(self._client)


class APIKeyOperations:
    """API key management operations"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def list_my_keys(self) -> Dict[str, Any]:
        """List current user's API keys"""
        return await self._client._request("GET", "/users/me/api-keys")

    async def create_key(self, name: str, **kwargs) -> Dict[str, Any]:
        """Create a new API key"""
        data = {"name": name, **kwargs}
        return await self._client._request(
            "POST", "/users/me/api-keys", data=data
        )


class OrganizationOperations:
    """Organization management operations"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def create(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new organization"""
        return await self._client._request(
            "POST", "/organizations", data=org_data
        )

    async def list(self) -> Dict[str, Any]:
        """List organizations the user belongs to"""
        return await self._client._request("GET", "/organizations")

    async def get(self, org_id: str) -> Dict[str, Any]:
        """Get organization details"""
        return await self._client._request("GET", f"/organizations/{org_id}")

    async def update(self, org_id: str, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update organization"""
        return await self._client._request(
            "PUT", f"/organizations/{org_id}", data=org_data
        )

    def members(self, org_id: str):
        """Access organization member operations"""
        return OrganizationMemberOperations(self._client, org_id)

    def invites(self, org_id: str):
        """Access organization invite operations"""
        return OrganizationInviteOperations(self._client, org_id)


class OrganizationMemberOperations:
    """Organization member management operations"""

    def __init__(self, client: TavoClient, org_id: str):
        self._client = client
        self.org_id = org_id

    async def list(self) -> Dict[str, Any]:
        """List organization members"""
        return await self._client._request(
            "GET", f"/organizations/{self.org_id}/members"
        )


class OrganizationInviteOperations:
    """Organization invite management operations"""

    def __init__(self, client: TavoClient, org_id: str):
        self._client = client
        self.org_id = org_id

    async def create(self, invite_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create organization invite"""
        return await self._client._request(
            "POST", f"/organizations/{self.org_id}/invites", data=invite_data
        )

    async def list(self) -> Dict[str, Any]:
        """List organization invites"""
        return await self._client._request(
            "GET", f"/organizations/{self.org_id}/invites"
        )

    async def accept(self, token: str) -> Dict[str, Any]:
        """Accept organization invite"""
        return await self._client._request(
            "POST", f"/organizations/invites/{token}/accept"
        )

    async def reject(self, token: str) -> Dict[str, Any]:
        """Reject organization invite"""
        return await self._client._request(
            "POST", f"/organizations/invites/{token}/reject"
        )


class ScanRuleOperations:
    """Scan rule management operations"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def create(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new scan rule"""
        return await self._client._request(
            "POST", "/scans/rules", data=rule_data
        )

    async def list(self) -> Dict[str, Any]:
        """List all scan rules"""
        return await self._client._request("GET", "/scans/rules")

    async def get(self, rule_id: str) -> Dict[str, Any]:
        """Get scan rule details"""
        return await self._client._request("GET", f"/scans/rules/{rule_id}")

    async def update(self, rule_id: str, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update scan rule"""
        return await self._client._request(
            "PUT", f"/scans/rules/{rule_id}", data=rule_data
        )

    async def delete(self, rule_id: str) -> Dict[str, Any]:
        """Delete scan rule"""
        return await self._client._request("DELETE", f"/scans/rules/{rule_id}")

    def upload(self) -> Dict[str, Any]:
        """Upload scan rules file"""
        # This would need special handling for file uploads
        # For now, return a placeholder
        return {"message": "File upload not yet implemented"}


class JobOperations:
    """Operations for job management."""

    def __init__(self, client: "TavoClient"):
        self._client = client

    async def status(self, job_id: str) -> Dict[str, Any]:
        """Get job status."""
        response = await self._client._request("GET", f"/jobs/status/{job_id}")
        return response

    async def dashboard(self) -> Dict[str, Any]:
        """Get job dashboard."""
        response = await self._client._request("GET", "/jobs/dashboard")
        return response


class WebhookOperations:
    """Operations for webhook management."""

    def __init__(self, client: "TavoClient"):
        self._client = client

    async def list_events(self) -> Dict[str, Any]:
        """List webhook events."""
        response = await self._client._request("GET", "/webhooks/events")
        return response

    async def get_event(self, event_id: str) -> Dict[str, Any]:
        """Get a specific webhook event."""
        response = await self._client._request(
            "GET", f"/webhooks/events/{event_id}"
        )
        return response


class AIAnalysisOperations:
    """Operations for AI analysis."""

    def __init__(self, client: "TavoClient"):
        self._client = client

    async def analyze_code(
        self, scan_id: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze code for fixes."""
        data = options or {}
        response = await self._client._request(
            "POST", f"/ai/analyze/{scan_id}", data=data
        )
        return response

    async def classify_vulnerabilities(
        self, scan_id: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Classify vulnerabilities."""
        data = options or {}
        response = await self._client._request(
            "POST", f"/ai/classify/{scan_id}", data=data
        )
        return response

    async def calculate_risk_score(
        self, scan_id: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Calculate risk score."""
        data = options or {}
        response = await self._client._request(
            "POST", f"/ai/risk-score/{scan_id}", data=data
        )
        return response

    async def generate_compliance_report(
        self, scan_id: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate compliance report."""
        data = options or {}
        response = await self._client._request(
            "POST", f"/ai/compliance/{scan_id}", data=data
        )
        return response

    async def predictive_analysis(
        self, scan_id: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Perform predictive analysis."""
        data = options or {}
        response = await self._client._request(
            "POST", f"/ai/predictive/{scan_id}", data=data
        )
        return response


class BillingOperations:
    """Operations for billing and usage."""

    def __init__(self, client: "TavoClient"):
        self._client = client

    async def get_usage(self) -> Dict[str, Any]:
        """Get usage report."""
        response = await self._client._request("GET", "/billing/usage")
        return response

    async def get_usage_summary(self) -> Dict[str, Any]:
        """Get usage summary."""
        response = await self._client._request("GET", "/billing/usage/summary")
        return response

    async def get_subscription(self) -> Dict[str, Any]:
        """Get subscription info."""
        response = await self._client._request("GET", "/billing/subscription")
        return response

    async def get_features(self) -> Dict[str, Any]:
        """Get feature access."""
        response = await self._client._request("GET", "/billing/features")
        return response

    async def get_billing_info(self) -> Dict[str, Any]:
        """Get billing information."""
        response = await self._client._request("GET", "/billing/billing")
        return response

    async def upgrade_subscription(self, new_tier: str) -> Dict[str, Any]:
        """Upgrade subscription tier."""
        params = {"new_tier": new_tier}
        response = await self._client._request(
            "POST", "/billing/upgrade", params=params
        )
        return response


class ReportOperations:
    """Operations for security reports"""

    def __init__(self, client: "TavoClient"):
        self._client = client

    async def create(
        self,
        scan_id: str,
        report_type: str = "scan_summary",
        format: str = "json",
        title: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new report"""
        data = {
            "scan_id": scan_id,
            "report_type": report_type,
            "format": format,
            "title": title,
            "description": description,
            **kwargs
        }
        return await self._client._request("POST", "/reports", data=data)

    async def get(self, report_id: str) -> Dict[str, Any]:
        """Get report details"""
        return await self._client._request("GET", f"/reports/{report_id}")

    async def list(
        self,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        report_type: Optional[str] = None,
        status: Optional[str] = None,
        scan_id: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        **params
    ) -> Dict[str, Any]:
        """List reports with optional filtering"""
        query_params = {
            "skip": skip,
            "limit": limit,
            "report_type": report_type,
            "status": status,
            "scan_id": scan_id,
            "sort_by": sort_by,
            "sort_order": sort_order,
            **params
        }
        # Remove None values
        query_params = {k: v for k, v in query_params.items() if v is not None}
        return await self._client._request("GET", "/reports", params=query_params)

    async def update(self, report_id: str, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update report status and content"""
        return await self._client._request("PUT", f"/reports/{report_id}", data=report_data)

    async def delete(self, report_id: str) -> Dict[str, Any]:
        """Delete a report"""
        await self._client._request("DELETE", f"/reports/{report_id}")
        return {"message": "Report deleted successfully"}

    async def download(self, report_id: str) -> bytes:
        """Download report file content"""
        # Make direct HTTP request to get the file content
        response = await self._client._client.get(
            f"/reports/{report_id}/download"
        )
        response.raise_for_status()
        return response.content

    async def get_summary(self) -> Dict[str, Any]:
        """Get report summary statistics"""
        return await self._client._request("GET", "/reports/summary")

    async def generate_scan_summary(
        self,
        scan_id: str,
        format: str = "json",
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a scan summary report"""
        return await self.create(
            scan_id=scan_id,
            report_type="scan_summary",
            format=format,
            title=title,
            description=description
        )

    async def generate_sarif(
        self,
        scan_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a SARIF report"""
        return await self.create(
            scan_id=scan_id,
            report_type="sarif",
            format="sarif",
            title=title,
            description=description
        )

    async def generate_compliance(
        self,
        scan_id: str,
        framework: str = "OWASP",
        format: str = "json",
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a compliance report"""
        return await self.create(
            scan_id=scan_id,
            report_type="compliance",
            format=format,
            title=title,
            description=description,
            compliance_framework=framework
        )

    async def generate_pdf(
        self,
        scan_id: str,
        report_type: str = "scan_summary",
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a PDF report"""
        return await self.create(
            scan_id=scan_id,
            report_type=report_type,
            format="pdf",
            title=title,
            description=description
        )

    async def generate_csv(
        self,
        scan_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a CSV report"""
        return await self.create(
            scan_id=scan_id,
            report_type="scan_summary",
            format="csv",
            title=title,
            description=description
        )

    async def generate_html(
        self,
        scan_id: str,
        report_type: str = "scan_summary",
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate an HTML report"""
        return await self.create(
            scan_id=scan_id,
            report_type=report_type,
            format="html",
            title=title,
            description=description
        )
