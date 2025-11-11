"""
WebSocket Handler for Tavo Scanner

Handles real-time updates via WebSocket connections for scan monitoring.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Callable
import time


class WebSocketHandler:
    """Handles WebSocket connections for real-time scan updates."""

    def __init__(self, sdk_integration):
        """Initialize WebSocket handler.

        Args:
            sdk_integration: SDK integration instance
        """
        self.sdk_integration = sdk_integration
        self.websocket = None
        self.connected = False
        self.subscribed_scans = set()
        self.message_handlers = []

    async def connect(self) -> None:
        """Establish WebSocket connection."""
        if self.connected:
            return

        try:
            # Use SDK's WebSocket connection
            async with self.sdk_integration.websocket_connection() as ws:
                self.websocket = ws
                self.connected = True
                print("WebSocket connected for real-time updates")
        except Exception as e:
            print(f"Warning: WebSocket connection failed: {e}")
            self.connected = False

    async def disconnect(self) -> None:
        """Close WebSocket connection."""
        if self.websocket:
            try:
                await self.websocket.close()
            except Exception:
                pass

        self.websocket = None
        self.connected = False
        self.subscribed_scans.clear()

    async def subscribe_to_scan(self, scan_id: str) -> None:
        """Subscribe to real-time updates for a scan.

        Args:
            scan_id: Scan identifier
        """
        if not self.connected:
            await self.connect()

        if self.websocket and scan_id not in self.subscribed_scans:
            try:
                # Send subscription message
                subscribe_msg = {
                    'type': 'subscribe',
                    'scan_id': scan_id
                }
                await self.websocket.send(json.dumps(subscribe_msg))
                self.subscribed_scans.add(scan_id)
                print(f"Subscribed to scan updates: {scan_id}")
            except Exception as e:
                print(f"Warning: Failed to subscribe to scan {scan_id}: {e}")

    async def unsubscribe_from_scan(self, scan_id: str) -> None:
        """Unsubscribe from scan updates.

        Args:
            scan_id: Scan identifier
        """
        if not self.connected or scan_id not in self.subscribed_scans:
            return

        try:
            # Send unsubscription message
            unsubscribe_msg = {
                'type': 'unsubscribe',
                'scan_id': scan_id
            }
            await self.websocket.send(json.dumps(unsubscribe_msg))
            self.subscribed_scans.remove(scan_id)
            print(f"Unsubscribed from scan updates: {scan_id}")
        except Exception as e:
            print(f"Warning: Failed to unsubscribe from scan {scan_id}: {e}")

    def add_message_handler(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Add a message handler for incoming WebSocket messages.

        Args:
            handler: Function to call with message data
        """
        self.message_handlers.append(handler)

    def remove_message_handler(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Remove a message handler.

        Args:
            handler: Handler function to remove
        """
        if handler in self.message_handlers:
            self.message_handlers.remove(handler)

    async def listen_for_updates(self, timeout_seconds: Optional[int] = None) -> None:
        """Listen for WebSocket messages.

        Args:
            timeout_seconds: Optional timeout for listening
        """
        if not self.connected or not self.websocket:
            return

        start_time = time.time()

        try:
            async for message in self.websocket:
                # Parse message
                try:
                    if isinstance(message, str):
                        data = json.loads(message)
                    else:
                        data = message
                except json.JSONDecodeError:
                    continue

                # Handle message
                await self._handle_message(data)

                # Check timeout
                if timeout_seconds and (time.time() - start_time) > timeout_seconds:
                    break

        except Exception as e:
            print(f"Warning: WebSocket listen error: {e}")

    async def _handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming WebSocket message.

        Args:
            message: Message data
        """
        # Call all registered handlers
        for handler in self.message_handlers:
            try:
                await handler(message)
            except Exception as e:
                print(f"Warning: Message handler error: {e}")

        # Handle specific message types
        msg_type = message.get('type', '')

        if msg_type == 'scan_update':
            await self._handle_scan_update(message)
        elif msg_type == 'scan_complete':
            await self._handle_scan_complete(message)
        elif msg_type == 'scan_error':
            await self._handle_scan_error(message)

    async def _handle_scan_update(self, message: Dict[str, Any]) -> None:
        """Handle scan progress update."""
        scan_id = message.get('scan_id')
        progress = message.get('progress', {})
        status = message.get('status', 'unknown')

        files_processed = progress.get('files_processed', 0)
        total_files = progress.get('total_files', 0)
        findings = progress.get('findings', 0)

        print(f"Scan {scan_id}: {status} - {files_processed}/{total_files} files, {findings} findings")

    async def _handle_scan_complete(self, message: Dict[str, Any]) -> None:
        """Handle scan completion."""
        scan_id = message.get('scan_id')
        results = message.get('results', {})

        vulnerabilities = results.get('vulnerabilities', [])
        scan_time = results.get('scan_time', 0)

        print(f"✅ Scan {scan_id} completed in {scan_time:.2f}s")
        print(f"   Found {len(vulnerabilities)} vulnerabilities")

    async def _handle_scan_error(self, message: Dict[str, Any]) -> None:
        """Handle scan error."""
        scan_id = message.get('scan_id')
        error = message.get('error', 'Unknown error')

        print(f"❌ Scan {scan_id} failed: {error}")

    async def wait_for_scan_completion(
        self,
        scan_id: str,
        timeout_seconds: int = 300,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Dict[str, Any]:
        """Wait for scan completion with real-time updates.

        Args:
            scan_id: Scan identifier
            timeout_seconds: Maximum wait time
            progress_callback: Optional callback for progress updates

        Returns:
            Final scan results
        """
        if progress_callback:
            self.add_message_handler(progress_callback)

        try:
            # Subscribe to scan updates
            await self.subscribe_to_scan(scan_id)

            # Listen for updates with timeout
            await self.listen_for_updates(timeout_seconds)

            # Get final results
            return await self.sdk_integration.get_scan_results(scan_id)

        finally:
            if progress_callback:
                self.remove_message_handler(progress_callback)
            await self.unsubscribe_from_scan(scan_id)

    def is_connected(self) -> bool:
        """Check if WebSocket is connected.

        Returns:
            True if connected
        """
        return self.connected

    def get_subscribed_scans(self) -> List[str]:
        """Get list of subscribed scan IDs.

        Returns:
            List of scan IDs
        """
        return list(self.subscribed_scans)


