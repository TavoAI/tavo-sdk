"""
Tavo SDK for Python

Official Python SDK for the Tavo API.
Designed for CLI tools, scanners, and programmatic access using API keys and device authentication.
"""

import httpx
from typing import Optional


class TavoClient:
    """Main Tavo API client for programmatic access.

    This client is optimized for CLI tools, scanners, and automated systems.
    It prioritizes API key and device authentication over JWT tokens.

    Authentication priority:
    1. API Key (X-API-Key header)
    2. Device Token (Authorization: Bearer)
    3. JWT Token (Authorization: Bearer) - fallback only
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        device_token: Optional[str] = None,
        base_url: str = "https://api.tavo.ai",
        timeout: float = 30.0
    ):
        """Initialize Tavo API client.

        Args:
            api_key: API key for authentication (preferred for programmatic access)
            device_token: Device authentication token
            base_url: Base URL for the API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.device_token = device_token
        self.timeout = timeout

        # Create HTTP client with appropriate auth headers
        headers = {"User-Agent": "tavo-sdk-python/0.1.0"}

        # Set authentication headers based on available credentials
        if api_key:
            headers["X-API-Key"] = api_key
        elif device_token:
            headers["Authorization"] = "Bearer " + device_token

        self.client = httpx.Client(
            base_url=self.base_url + "/api/v1",
            headers=headers,
            timeout=timeout
        )

        self.deviceauth = DeviceAuthClient(base_url)
        self.scans = ScansClient(base_url)
        self.scanmanagement = ScanManagementClient(base_url)
        self.scantools = ScanToolsClient(base_url)
        self.scanrules = ScanRulesClient(base_url)
        self.scanschedules = ScanSchedulesClient(base_url)
        self.scanbulkoperations = ScanBulkOperationsClient(base_url)
        self.scannerintegration = ScannerIntegrationClient(base_url)
        self.aianalysis = AiAnalysisClient(base_url)
        self.aianalysiscore = AiAnalysisCoreClient(base_url)
        self.aibulkoperations = AiBulkOperationsClient(base_url)
        self.aiperformancequality = AiPerformanceQualityClient(base_url)
        self.airesultsexport = AiResultsExportClient(base_url)
        self.airiskcompliance = AiRiskComplianceClient(base_url)
        self.registry = RegistryClient(base_url)
        self.pluginexecution = PluginExecutionClient(base_url)
        self.pluginmarketplace = PluginMarketplaceClient(base_url)
        self.rules = RulesClient(base_url)
        self.codesubmission = CodeSubmissionClient(base_url)
        self.repositories = RepositoriesClient(base_url)
        self.repositoryconnections = RepositoryConnectionsClient(base_url)
        self.repositoryproviders = RepositoryProvidersClient(base_url)
        self.repositorywebhooks = RepositoryWebhooksClient(base_url)
        self.jobs = JobsClient(base_url)
        self.health = HealthClient(base_url)
        self.websockets = WebsocketsClient(base_url)

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def set_api_key(self, api_key: str):
        """Update API key for authentication."""
        self.api_key = api_key
        self.client.headers["X-API-Key"] = api_key
        if "Authorization" in self.client.headers:
            del self.client.headers["Authorization"]

    def set_device_token(self, device_token: str):
        """Update device token for authentication."""
        self.device_token = device_token
        self.client.headers["Authorization"] = "Bearer " + device_token
        if "X-API-Key" in self.client.headers:
            del self.client.headers["X-API-Key"]
