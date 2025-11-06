"""
Tavo AI API Client

Official Python SDK for the Tavo API with WebSocket support.
"""

import asyncio
from typing import Any, Dict, List, Optional, Callable
import httpx
import websockets
from pydantic import BaseModel, Field
import json
import uuid

# Import generated endpoint clients
from .ai_analysis_core import AiAnalysisCoreClient
from .ai_analysis import AiAnalysisClient
from .ai_bulk_operations import AiBulkOperationsClient
from .ai_performance_quality import AiPerformanceQualityClient
from .ai_results_export import AiResultsExportClient
from .ai_risk_compliance import AiRiskComplianceClient
from .code_submission import CodeSubmissionClient
from .device_auth import DeviceAuthClient
from .health import HealthClient
from .jobs import JobClient
from .plugin_execution import PluginExecutionClient
from .plugin_marketplace import PluginMarketplaceClient
from .registry import RegistryClient
from .repositories import RepositoriesClient
from .repository_connections import RepositoryConnectionsClient
from .repository_providers import RepositoryProvidersClient
from .repository_webhooks import RepositoryWebhooksClient
from .rules import RulesClient
from .scan_bulk_operations import ScanBulkOperationsClient
from .scan_management import ScanManagementClient
from .scan_rules import ScanRulesClient
from .scan_schedules import ScanSchedulesClient
from .scan_tools import ScanToolsClient
from .scanner_integration import ScannerIntegrationClient


class WebSocketConfig(BaseModel):
    """Configuration for WebSocket connections"""

    reconnect_interval: float = Field(
        default=5.0, description="Reconnection interval in seconds"
    )
    max_reconnect_attempts: int = Field(
        default=5, description="Maximum reconnection attempts"
    )
    heartbeat_interval: float = Field(
        default=30.0, description="Heartbeat interval in seconds"
    )


class ScanUpdateMessage(BaseModel):
    """Message schema for scan updates"""

    scan_id: str
    update_type: str  # 'started', 'progress', 'result', 'completed', 'error'
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class NotificationMessage(BaseModel):
    """Message schema for notifications"""

    type: str  # 'info', 'warning', 'error', 'success'
    title: str
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class GeneralMessage(BaseModel):
    """Message schema for general broadcasts"""

    type: str
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class WebSocketConnectionManager:
    """WebSocket connection management with async context manager support"""

    def __init__(
        self,
        websocket_url: str,
        auth_token: str,
        client_id: str,
        ws_config: WebSocketConfig,
    ):
        self.websocket_url = websocket_url
        self.auth_token = auth_token
        self.client_id = client_id
        self.ws_config = ws_config
        self.websocket: Optional[Any] = None
        self.is_connected = False
        self.reconnect_attempts = 0
        self.heartbeat_task: Optional[asyncio.Task] = None
        self.receive_task: Optional[asyncio.Task] = None
        self.reconnect_task: Optional[asyncio.Task] = None
        self.message_handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    async def connect(self) -> bool:
        """Connect to the WebSocket server"""
        try:
            # Build WebSocket URL with authentication
            url = f"{self.websocket_url}?token={self.auth_token}&client_id={self.client_id}"
            self.websocket = await websockets.connect(url)
            self.is_connected = True
            self.reconnect_attempts = 0

            # Start heartbeat and receive tasks
            self.heartbeat_task = asyncio.create_task(self._heartbeat())
            self.receive_task = asyncio.create_task(self._receive_loop())

            return True
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
            self.is_connected = False
            return False

    async def disconnect(self):
        """Disconnect from the WebSocket server"""
        self.is_connected = False

        # Cancel tasks
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
        if self.receive_task:
            self.receive_task.cancel()
        if self.reconnect_task:
            self.reconnect_task.cancel()

        # Close WebSocket
        if self.websocket:
            await self.websocket.close()

    async def send_message(self, message: Dict[str, Any]) -> bool:
        """Send a message to the WebSocket server"""
        if not self.is_connected or not self.websocket:
            return False

        try:
            await self.websocket.send(json.dumps(message))
            return True
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False

    def on_message(self, message_type: str, handler: Callable[[Dict[str, Any]], Any]):
        """Register a message handler"""
        self.message_handlers[message_type] = handler

    async def _heartbeat(self):
        """Send periodic heartbeat messages"""
        while self.is_connected:
            try:
                await asyncio.sleep(self.ws_config.heartbeat_interval)
                if self.is_connected:
                    await self.send_message({"type": "heartbeat", "timestamp": str(uuid.uuid4())})
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Heartbeat failed: {e}")

    async def _receive_loop(self):
        """Receive and process messages from the WebSocket server"""
        while self.is_connected:
            try:
                if self.websocket:
                    message = await self.websocket.recv()
                    data = json.loads(message)

                    # Handle message based on type
                    message_type = data.get("type")
                    if message_type in self.message_handlers:
                        handler = self.message_handlers[message_type]
                        await handler(data)
                    else:
                        # Default handling for unknown message types
                        print(f"Received unhandled message type: {message_type}")
            except websockets.exceptions.ConnectionClosed:
                if self.is_connected:
                    self._schedule_reconnect()
                break
            except Exception as e:
                print(f"Receive loop error: {e}")

    def _schedule_reconnect(self):
        """Schedule a reconnection attempt"""
        if self.reconnect_attempts < self.ws_config.max_reconnect_attempts:
            self.reconnect_attempts += 1
            self.reconnect_task = asyncio.create_task(self._reconnect())

    async def _reconnect(self):
        """Attempt to reconnect to the WebSocket server"""
        await asyncio.sleep(self.ws_config.reconnect_interval)
        if not self.is_connected:
            print(f"Attempting to reconnect (attempt {self.reconnect_attempts})")
            await self.connect()


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
        jwt_token: Optional[str] = None,
        session_token: Optional[str] = None,
        base_url: str = "https://api.tavoai.net",
        api_version: str = "v1",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize Tavo API client

        Args:
            api_key: API key for authentication. If not provided, will look
                for TAVO_API_KEY env var
            jwt_token: JWT token for authentication
            session_token: Session token for authentication
            base_url: Base URL for the API
            api_version: API version to use
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        # Handle authentication - prefer JWT token over session token over API key
        if jwt_token is None and session_token is None and api_key is None:
            import os

            api_key = os.getenv("TAVO_API_KEY")
            jwt_token = os.getenv("TAVO_JWT_TOKEN")
            session_token = os.getenv("TAVO_SESSION_TOKEN")

        if jwt_token is None and session_token is None and api_key is None:
            raise ValueError(
                "Either API key, JWT token, or session token must be provided, or set "
                "TAVO_API_KEY, TAVO_JWT_TOKEN, or TAVO_SESSION_TOKEN environment variables"
            )

        self.config = type('Config', (), {
            'api_key': api_key,
            'jwt_token': jwt_token,
            'session_token': session_token,
            'base_url': base_url,
            'api_version': api_version,
            'timeout': timeout,
            'max_retries': max_retries,
        })()

        # Create HTTP client with appropriate auth headers
        headers = {"User-Agent": "tavo-sdk-python/0.1.0"}
        auth_headers = self._get_auth_headers()
        headers.update(auth_headers)

        self._client = httpx.AsyncClient(
            base_url=f"{base_url}/{api_version}",
            headers=headers,
            timeout=timeout
        )

        # Initialize WebSocket manager
        self.websocket_manager: Optional[WebSocketConnectionManager] = None
        self.ws_config = WebSocketConfig()

        # Initialize generated endpoint clients
        self.device_auth = DeviceAuthClient(base_url, self._client)
        self.scans = ScanToolsClient(base_url, self._client)
        self.scan_management = ScanManagementClient(base_url, self._client)
        self.scan_tools = ScanToolsClient(base_url, self._client)
        self.scan_rules = ScanRulesClient(base_url, self._client)
        self.scan_schedules = ScanSchedulesClient(base_url, self._client)
        self.scan_bulk_operations = ScanBulkOperationsClient(base_url, self._client)
        self.scanner_integration = ScannerIntegrationClient(base_url, self._client)
        self.ai_analysis = AiAnalysisClient(base_url, self._client)
        self.ai_analysis_core = AiAnalysisCoreClient(base_url, self._client)
        self.ai_bulk_operations = AiBulkOperationsClient(base_url, self._client)
        self.ai_performance_quality = AiPerformanceQualityClient(base_url, self._client)
        self.ai_results_export = AiResultsExportClient(base_url, self._client)
        self.ai_risk_compliance = AiRiskComplianceClient(base_url, self._client)
        self.registry = RegistryClient(base_url, self._client)
        self.plugin_execution = PluginExecutionClient(base_url, self._client)
        self.plugin_marketplace = PluginMarketplaceClient(base_url, self._client)
        self.rules = RulesClient(base_url, self._client)
        self.code_submission = CodeSubmissionClient(base_url, self._client)
        self.repositories = RepositoriesClient(base_url, self._client)
        self.repository_connections = RepositoryConnectionsClient(base_url, self._client)
        self.repository_providers = RepositoryProvidersClient(base_url, self._client)
        self.repository_webhooks = RepositoryWebhooksClient(base_url, self._client)
        self.jobs = JobClient(base_url, self._client)
        self.health = HealthClient(base_url, self._client)

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers based on available credentials"""
        headers = {}

        # Prefer JWT token over session token over API key
        if self.config.jwt_token:
            headers["Authorization"] = f"Bearer {self.config.jwt_token}"
        elif self.config.session_token:
            headers["Authorization"] = f"Bearer {self.config.session_token}"
        elif self.config.api_key:
            headers["X-API-Key"] = self.config.api_key

        return headers

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the HTTP client and WebSocket connection"""
        if self.websocket_manager:
            await self.websocket_manager.disconnect()
        await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Any:
        """Make HTTP request with retry logic"""
        url = f"{self.config.base_url}/{self.config.api_version}{path}"

        for attempt in range(self.config.max_retries + 1):
            try:
                response = await self._client.request(method, url, json=data, params=params, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < self.config.max_retries:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
            except Exception:
                if attempt < self.config.max_retries:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise

    # WebSocket methods
    async def connect_websocket(self, client_id: str) -> bool:
        """Connect to WebSocket server"""
        if not self.websocket_manager:
            # Get auth token for WebSocket
            auth_token = (
                self.config.jwt_token or
                self.config.session_token or
                self.config.api_key
            )
            if not auth_token:
                raise ValueError("Authentication token required for WebSocket connection")

            ws_url = self.config.base_url.replace("http", "ws") + "/ws"
            self.websocket_manager = WebSocketConnectionManager(
                ws_url, auth_token, client_id, self.ws_config
            )

        return await self.websocket_manager.connect()

    async def disconnect_websocket(self):
        """Disconnect from WebSocket server"""
        if self.websocket_manager:
            await self.websocket_manager.disconnect()

    def on_websocket_message(self, message_type: str, handler: Callable[[Dict[str, Any]], Any]):
        """Register WebSocket message handler"""
        if self.websocket_manager:
            self.websocket_manager.on_message(message_type, handler)

    async def send_websocket_message(self, message: Dict[str, Any]) -> bool:
        """Send message via WebSocket"""
        if self.websocket_manager:
            return await self.websocket_manager.send_message(message)
        return False

    # Wrapper methods for backward compatibility with tavo-scanner
    def auth(self):
        """Access authentication operations"""
        return self.device_auth

    def users(self):
        """Access user management operations"""
        # Users operations not in generated SDK - return None or create wrapper
        return None

    def organizations(self):
        """Access organization operations"""
        # Organizations operations not in generated SDK - return None or create wrapper
        return None

    def jobs(self):
        """Access job operations"""
        return self.jobs

    def scans(self):
        """Access scan-related operations"""
        return self.scan_tools

    def scan_rules(self):
        """Access scan rule operations"""
        return self.scan_rules

    def ai_analysis(self):
        """Access AI analysis operations"""
        return self.ai_analysis

    def code_submission(self):
        """Access code submission operations"""
        return self.code_submission

    def repositories(self):
        """Access repository operations"""
        return self.repositories

    def plugins(self):
        """Access plugin operations"""
        return self.plugin_execution

    def rules(self):
        """Access rule management operations"""
        return self.rules

    def registry(self):
        """Access registry operations"""
        return self.registry

    async def health_check(self) -> Dict[str, Any]:
        """Health check endpoint"""
        return await self.health.health_check()
