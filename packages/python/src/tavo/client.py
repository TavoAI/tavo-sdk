"""Tavo AI API Client"""

import asyncio
from typing import Any, Dict, List, Optional, Callable
import httpx
import websockets
from pydantic import BaseModel, Field
import json
import uuid


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
    """WebSocket connection management"""

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
        """Send a message through the WebSocket"""
        if self.is_connected and self.websocket:
            try:
                await self.websocket.send(json.dumps(message))
                return True
            except Exception as e:
                print(f"Failed to send WebSocket message: {e}")
                return False
        return False

    def on_message(self, message_type: str, handler: Callable[[Dict[str, Any]], Any]):
        """Register a message handler"""
        self.message_handlers[message_type] = handler

    async def _heartbeat(self):
        """Send heartbeat messages to keep connection alive"""
        while self.is_connected:
            try:
                await self.send_message({"type": "ping"})
                await asyncio.sleep(self.ws_config.heartbeat_interval)
            except Exception:
                break

    async def _receive_loop(self):
        """Receive and handle messages from the WebSocket"""
        while self.is_connected and self.websocket:
            try:
                message_raw = await self.websocket.recv()
                message = json.loads(message_raw)

                # Handle message
                message_type = message.get("type")
                if message_type in self.message_handlers:
                    await self.message_handlers[message_type](message)
                elif message_type == "pong":
                    # Handle pong response
                    pass
                else:
                    print(f"Unhandled WebSocket message type: {message_type}")

            except websockets.exceptions.ConnectionClosed:
                self.is_connected = False
                if self.reconnect_attempts < self.ws_config.max_reconnect_attempts:
                    self._schedule_reconnect()
                break
            except Exception as e:
                print(f"WebSocket receive error: {e}")
                self.is_connected = False
                break

    def _schedule_reconnect(self):
        """Schedule a reconnection attempt"""
        if self.reconnect_task:
            self.reconnect_task.cancel()

        self.reconnect_attempts += 1
        self.reconnect_task = asyncio.create_task(self._reconnect())

    async def _reconnect(self):
        """Attempt to reconnect to the WebSocket server"""
        await asyncio.sleep(self.ws_config.reconnect_interval * self.reconnect_attempts)

        if await self.connect():
            print(f"WebSocket reconnected after {self.reconnect_attempts} attempts")
        else:
            if self.reconnect_attempts < self.ws_config.max_reconnect_attempts:
                self._schedule_reconnect()


class TavoConfig(BaseModel):
    """Configuration for Tavo API client"""

    api_key: Optional[str] = Field(
        default=None, description="API key for authentication"
    )
    jwt_token: Optional[str] = Field(
        default=None, description="JWT token for authentication"
    )
    session_token: Optional[str] = Field(
        default=None, description="Session token for authentication"
    )
    base_url: str = Field(
        default="https://api.tavoai.net", description="Base URL for API"
    )
    api_version: str = Field(default="v1", description="API version to use")
    timeout: float = Field(default=30.0, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retries")
    websocket_config: WebSocketConfig = Field(
        default_factory=WebSocketConfig,
        description="WebSocket connection configuration",
    )


class TavoClient:
    """Main client for interacting with Tavo AI API"""

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

        self.config = TavoConfig(
            api_key=api_key,
            jwt_token=jwt_token,
            session_token=session_token,
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

        # WebSocket connections storage
        self._websocket_connections: Dict[str, "WebSocketConnectionManager"] = {}

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers based on available credentials"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "tavo-python-sdk/0.1.0",
        }

        if self.config.jwt_token:
            headers["Authorization"] = f"Bearer {self.config.jwt_token}"
        elif self.config.session_token:
            headers["X-Session-Token"] = self.config.session_token
        elif self.config.api_key:
            headers["X-API-Key"] = self.config.api_key

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
                if e.response.status_code >= 500 and attempt < self.config.max_retries:
                    await asyncio.sleep(2**attempt)  # Exponential backoff
                    continue
                raise
            except httpx.RequestError:
                if attempt < self.config.max_retries:
                    await asyncio.sleep(2**attempt)
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

    def rule_management(self):
        """Access rule management operations"""
        return RuleManagementOperations(self)

    def device_auth(self):
        """Access device authentication operations"""
        return DeviceAuthOperations(self)

    def session_auth(self):
        """Access session authentication operations"""
        return SessionAuthOperations(self)

    def local_scanner(self):
        """Access local scanning operations"""
        return LocalScannerOperations()

    def websocket(self):
        """Access WebSocket operations for real-time features"""
        return WebSocketOperations(self)


class WebSocketOperations:
    """WebSocket operations for real-time features"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def connect_to_scan(
        self, scan_id: str, on_message: Callable[[ScanUpdateMessage], Any]
    ) -> str:
        """Connect to scan progress updates WebSocket

        Args:
            scan_id: The scan ID to monitor
            on_message: Callback function for handling scan update messages

        Returns:
            Connection ID for the WebSocket connection
        """
        connection_id = f"scan_{scan_id}_{uuid.uuid4().hex[:8]}"

        # Build WebSocket URL
        ws_url = self._client.config.base_url.replace("http", "ws")
        ws_url = f"{ws_url}/ws/scan/{scan_id}"

        # Get auth token
        auth_token = (
            self._client.config.jwt_token
            or self._client.config.session_token
            or self._client.config.api_key
        )
        if not auth_token:
            raise ValueError("Authentication token required for WebSocket connection")

        # Create connection manager
        client_id = f"client_{uuid.uuid4().hex[:8]}"
        connection_manager = WebSocketConnectionManager(
            ws_url, auth_token, client_id, self._client.config.websocket_config
        )

        # Set up message handler
        async def handle_scan_message(message: Dict[str, Any]):
            if message.get("type") in [
                "scan_update",
                "progress",
                "started",
                "completed",
                "error",
            ]:
                scan_message = ScanUpdateMessage(**message.get("data", message))
                await on_message(scan_message)

        connection_manager.on_message("scan_update", handle_scan_message)
        connection_manager.on_message("progress", handle_scan_message)
        connection_manager.on_message("started", handle_scan_message)
        connection_manager.on_message("completed", handle_scan_message)
        connection_manager.on_message("error", handle_scan_message)

        # Connect
        if await connection_manager.connect():
            self._client._websocket_connections[connection_id] = connection_manager
            return connection_id
        else:
            raise Exception(f"Failed to connect to scan WebSocket for scan {scan_id}")

    async def connect_to_notifications(
        self, on_message: Callable[[NotificationMessage], Any]
    ) -> str:
        """Connect to user notifications WebSocket

        Args:
            on_message: Callback function for handling notification messages

        Returns:
            Connection ID for the WebSocket connection
        """
        connection_id = f"notifications_{uuid.uuid4().hex[:8]}"

        # Build WebSocket URL
        ws_url = self._client.config.base_url.replace("http", "ws")
        ws_url = f"{ws_url}/ws/notifications"

        # Get auth token
        auth_token = (
            self._client.config.jwt_token
            or self._client.config.session_token
            or self._client.config.api_key
        )
        if not auth_token:
            raise ValueError("Authentication token required for WebSocket connection")

        # Create connection manager
        client_id = f"client_{uuid.uuid4().hex[:8]}"
        connection_manager = WebSocketConnectionManager(
            ws_url, auth_token, client_id, self._client.config.websocket_config
        )

        # Set up message handler
        async def handle_notification_message(message: Dict[str, Any]):
            if message.get("type") == "notification":
                notification = NotificationMessage(**message.get("data", message))
                await on_message(notification)

        connection_manager.on_message("notification", handle_notification_message)

        # Connect
        if await connection_manager.connect():
            self._client._websocket_connections[connection_id] = connection_manager
            return connection_id
        else:
            raise Exception("Failed to connect to notifications WebSocket")

    async def connect_to_general(
        self, on_message: Callable[[GeneralMessage], Any]
    ) -> str:
        """Connect to general broadcasts WebSocket

        Args:
            on_message: Callback function for handling general messages

        Returns:
            Connection ID for the WebSocket connection
        """
        connection_id = f"general_{uuid.uuid4().hex[:8]}"

        # Build WebSocket URL
        ws_url = self._client.config.base_url.replace("http", "ws")
        ws_url = f"{ws_url}/ws/general"

        # Get auth token
        auth_token = (
            self._client.config.jwt_token
            or self._client.config.session_token
            or self._client.config.api_key
        )
        if not auth_token:
            raise ValueError("Authentication token required for WebSocket connection")

        # Create connection manager
        client_id = f"client_{uuid.uuid4().hex[:8]}"
        connection_manager = WebSocketConnectionManager(
            ws_url, auth_token, client_id, self._client.config.websocket_config
        )

        # Set up message handler
        async def handle_general_message(message: Dict[str, Any]):
            general_message = GeneralMessage(**message.get("data", message))
            await on_message(general_message)

        connection_manager.on_message("general", handle_general_message)

        # Connect
        if await connection_manager.connect():
            self._client._websocket_connections[connection_id] = connection_manager
            return connection_id
        else:
            raise Exception("Failed to connect to general WebSocket")

    async def disconnect(self, connection_id: str):
        """Disconnect from a WebSocket connection

        Args:
            connection_id: The connection ID to disconnect
        """
        connection_manager = self._client._websocket_connections.get(connection_id)
        if connection_manager:
            await connection_manager.disconnect()
            del self._client._websocket_connections[connection_id]

    async def disconnect_all(self):
        """Disconnect from all WebSocket connections"""
        for connection_manager in self._client._websocket_connections.values():
            await connection_manager.disconnect()
        self._client._websocket_connections.clear()

    async def send_message(self, connection_id: str, message: Dict[str, Any]) -> bool:
        """Send a message through a WebSocket connection

        Args:
            connection_id: The connection ID to send through
            message: The message to send

        Returns:
            True if sent successfully, False otherwise
        """
        connection_manager = self._client._websocket_connections.get(connection_id)
        if connection_manager:
            return await connection_manager.send_message(message)
        return False


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
        return await self._client._request("POST", "/auth/register", data=user_data)

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
        return await self._client._request("PUT", f"/users/{user_id}", data=user_data)

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
        return await self._client._request("POST", "/users/me/api-keys", data=data)

    async def update_key(self, api_key_id: str, name: str, **kwargs) -> Dict[str, Any]:
        """Update an API key"""
        data = {"name": name, **kwargs}
        return await self._client._request(
            "PUT", f"/users/me/api-keys/{api_key_id}", data=data
        )

    async def delete_key(self, api_key_id: str) -> Dict[str, Any]:
        """Delete an API key"""
        await self._client._request("DELETE", f"/users/me/api-keys/{api_key_id}")
        return {"message": "API key deleted successfully"}

    async def rotate_key(self, api_key_id: str, **kwargs) -> Dict[str, Any]:
        """Rotate an API key"""
        data = kwargs
        return await self._client._request(
            "POST", f"/users/me/api-keys/{api_key_id}/rotate", data=data
        )


class OrganizationOperations:
    """Organization management operations"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def create(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new organization"""
        return await self._client._request("POST", "/organizations", data=org_data)

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
        return await self._client._request("POST", "/scans/rules", data=rule_data)

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

    async def upload(self, file_path: str) -> Dict[str, Any]:
        """Upload scan rules file"""
        import os
        import asyncio

        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        # Read file content asynchronously
        def read_file():
            with open(file_path, "rb") as f:
                return f.read()

        file_content = await asyncio.get_event_loop().run_in_executor(None, read_file)

        # Prepare multipart form data
        files = {
            "file": (
                os.path.basename(file_path),
                file_content,
                "application/octet-stream",
            )
        }

        # Make request with files
        async with httpx.AsyncClient(
            base_url=self._client.config.base_url
            + f"/api/{self._client.config.api_version}",
            headers=self._client._get_auth_headers(),
            timeout=self._client.config.timeout,
        ) as client:
            response = await client.post("/scans/rules/upload", files=files)
            response.raise_for_status()
            return response.json()


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
        response = await self._client._request("GET", f"/webhooks/events/{event_id}")
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
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new report"""
        data = {
            "scan_id": scan_id,
            "report_type": report_type,
            "format": format,
            "title": title,
            "description": description,
            **kwargs,
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
        **params,
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
            **params,
        }
        # Remove None values
        query_params = {k: v for k, v in query_params.items() if v is not None}
        return await self._client._request("GET", "/reports", params=query_params)

    async def update(
        self, report_id: str, report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update report status and content"""
        return await self._client._request(
            "PUT", f"/reports/{report_id}", data=report_data
        )

    async def delete(self, report_id: str) -> Dict[str, Any]:
        """Delete a report"""
        await self._client._request("DELETE", f"/reports/{report_id}")
        return {"message": "Report deleted successfully"}

    async def download(self, report_id: str) -> bytes:
        """Download report file content"""
        # Make direct HTTP request to get the file content
        response = await self._client._client.get(f"/reports/{report_id}/download")
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
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a scan summary report"""
        return await self.create(
            scan_id=scan_id,
            report_type="scan_summary",
            format=format,
            title=title,
            description=description,
        )

    async def generate_sarif(
        self,
        scan_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a SARIF report"""
        return await self.create(
            scan_id=scan_id,
            report_type="sarif",
            format="sarif",
            title=title,
            description=description,
        )

    async def generate_compliance(
        self,
        scan_id: str,
        framework: str = "OWASP",
        format: str = "json",
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a compliance report"""
        return await self.create(
            scan_id=scan_id,
            report_type="compliance",
            format=format,
            title=title,
            description=description,
            compliance_framework=framework,
        )

    async def generate_pdf(
        self,
        scan_id: str,
        report_type: str = "scan_summary",
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a PDF report"""
        return await self.create(
            scan_id=scan_id,
            report_type=report_type,
            format="pdf",
            title=title,
            description=description,
        )

    async def generate_csv(
        self,
        scan_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a CSV report"""
        return await self.create(
            scan_id=scan_id,
            report_type="scan_summary",
            format="csv",
            title=title,
            description=description,
        )

    async def generate_html(
        self,
        scan_id: str,
        report_type: str = "scan_summary",
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate an HTML report"""
        return await self.create(
            scan_id=scan_id,
            report_type=report_type,
            format="html",
            title=title,
            description=description,
        )


class RuleManagementOperations:
    """Operations for rule bundle management"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def list_bundles(
        self,
        category: Optional[str] = None,
        official_only: bool = False,
        page: int = 1,
        per_page: int = 50,
    ) -> Dict[str, Any]:
        """List available rule bundles"""
        params = {"page": page, "per_page": per_page}
        if category:
            params["category"] = category
        if official_only:
            params["official_only"] = official_only

        return await self._client._request("GET", "/rules/bundles", params=params)

    async def get_bundle_rules(self, bundle_id: str) -> Dict[str, Any]:
        """Get rules from a specific bundle"""
        return await self._client._request("GET", f"/rules/bundles/{bundle_id}/rules")

    async def install_bundle(
        self, bundle_id: str, organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Install a rule bundle"""
        data = {}
        if organization_id:
            data["organization_id"] = organization_id

        return await self._client._request(
            "POST", f"/rules/bundles/{bundle_id}/install", data=data
        )

    async def uninstall_bundle(self, bundle_id: str) -> Dict[str, Any]:
        """Uninstall a rule bundle"""
        return await self._client._request(
            "DELETE", f"/rules/bundles/{bundle_id}/install"
        )

    async def validate_rules(self, rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate rule syntax"""
        data = {"rules": rules}
        return await self._client._request("POST", "/rules/validate", data=data)

    async def check_bundle_updates(
        self, bundle_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Check for updates to installed rule bundles"""
        params = {}
        if bundle_ids:
            params["bundle_ids"] = ",".join(bundle_ids)

        return await self._client._request("GET", "/rules/updates", params=params)


class LocalScannerOperations:
    """Local scanning operations using scanner binaries"""

    def __init__(self):
        self.scanner_path = self._find_scanner_binary()

    def _find_scanner_binary(self) -> str:
        """Find the scanner binary in the SDK or system PATH"""
        from pathlib import Path

        # First, try to find it relative to the SDK installation
        sdk_dir = Path(__file__).parent.parent.parent.parent
        scanner_path = sdk_dir / "scanner" / "dist" / "tavo-scanner"

        if scanner_path.exists():
            return str(scanner_path)

        # Try to find it in the workspace
        current_dir = Path.cwd()
        workspace_root = current_dir
        while workspace_root != workspace_root.parent:
            scanner_path = (
                workspace_root
                / "tavo-api"
                / "packages"
                / "scanner"
                / "dist"
                / "tavo-scanner"
            )
            if scanner_path.exists():
                return str(scanner_path)
            workspace_root = workspace_root.parent

        # Fall back to system PATH
        return "tavo-scanner"

    async def scan_codebase(
        self, path: str, bundle: str = "llm-security", output_format: str = "json"
    ) -> Dict[str, Any]:
        """Scan a codebase using the local scanner binary"""
        import subprocess
        import json

        if not self.scanner_path:
            raise RuntimeError(
                "Scanner binary not found. Please install the Tavo scanner."
            )

        # Build command
        cmd = [self.scanner_path, path, "--bundle", bundle, "--format", output_format]

        # Run scanner in subprocess
        def run_scanner():
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout
                    cwd=None,
                )
                return result
            except subprocess.TimeoutExpired as exc:
                raise RuntimeError("Scanner timed out") from exc
            except FileNotFoundError as exc:
                raise RuntimeError(
                    f"Scanner binary not found at {self.scanner_path}"
                ) from exc

        # Run in thread pool to avoid blocking
        result = await asyncio.get_event_loop().run_in_executor(None, run_scanner)

        if result.returncode not in [0, 1]:  # 0 = passed, 1 = failed with findings
            error_msg = result.stderr.strip() or "Unknown scanner error"
            raise RuntimeError(f"Scanner failed: {error_msg}")

        # Parse JSON output
        if output_format == "json":
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Failed to parse scanner output: {e}") from e

        # For text format, return structured data
        return {
            "output": result.stdout,
            "exit_code": result.returncode,
            "passed": result.returncode == 0,
        }

    async def scan_file(
        self, file_path: str, bundle: str = "llm-security"
    ) -> Dict[str, Any]:
        """Scan a single file"""
        return await self.scan_codebase(file_path, bundle)

    async def scan_directory(
        self, dir_path: str, bundle: str = "llm-security"
    ) -> Dict[str, Any]:
        """Scan a directory"""
        return await self.scan_codebase(dir_path, bundle)


class DeviceAuthOperations:
    """Device code authentication operations"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def create_device_code(
        self, client_id: Optional[str] = None, client_name: str = "Tavo SDK"
    ) -> Dict[str, Any]:
        """Create a device code for authentication"""
        data = {"client_name": client_name}
        if client_id:
            data["client_id"] = client_id

        return await self._client._request("POST", "/device/code", data=data)

    async def poll_device_token(self, device_code: str) -> Dict[str, Any]:
        """Poll for device token status"""
        return await self._client._request(
            "POST", "/device/token", data={"device_code": device_code}
        )


class SessionAuthOperations:
    """Session token authentication operations"""

    def __init__(self, client: TavoClient):
        self._client = client

    async def create_session_token(
        self, description: str = "SDK Session"
    ) -> Dict[str, Any]:
        """Create a new session token"""
        return await self._client._request(
            "POST", "/auth/session/create", data={"description": description}
        )

    async def list_session_tokens(self) -> Dict[str, Any]:
        """List all session tokens"""
        return await self._client._request("GET", "/auth/session/list")

    async def delete_session_token(self, token_id: str) -> Dict[str, Any]:
        """Delete a specific session token"""
        return await self._client._request("DELETE", f"/auth/session/{token_id}")

    async def delete_all_session_tokens(self) -> Dict[str, Any]:
        """Delete all session tokens"""
        return await self._client._request("DELETE", "/auth/session/")

    async def validate_session_token(self, token: str) -> Dict[str, Any]:
        """Validate a session token"""
        return await self._client._request(
            "POST", "/auth/session/validate", data={"token": token}
        )

    async def authenticate_with_session_token(self, token: str) -> Dict[str, Any]:
        """Authenticate using a session token"""
        return await self._client._request(
            "POST", "/auth/session/authenticate", data={"token": token}
        )
