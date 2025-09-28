#!/usr/bin/env python3
"""
Tavo AI Python SDK - WebSocket Example

This example demonstrates how to use WebSocket connections for real-time features
including scan progress updates, notifications, and general broadcasts.
"""

import asyncio
import os
from tavo.client import (
    TavoClient,
    ScanUpdateMessage,
    NotificationMessage,
    GeneralMessage,
)


async def monitor_scan_progress(client: TavoClient, scan_id: str):
    """Monitor scan progress via WebSocket"""
    try:
        connection_id = await client.websocket().connect_to_scan(
            scan_id, lambda message: handle_scan_message(message)
        )

        print(f"Connected to scan {scan_id} with connection ID: {connection_id}")

        # Optional: Send a ping message
        await asyncio.sleep(5)
        await client.websocket().send_message(connection_id, {"type": "ping"})

        # Keep connection alive for demonstration
        await asyncio.sleep(300)  # 5 minutes

    except Exception as error:
        print(f"Failed to connect to scan WebSocket: {error}")


def handle_scan_message(message: ScanUpdateMessage):
    """Handle scan update messages"""
    print(f"Scan update: {message}")

    if message.update_type == "started":
        print(f"Scan {message.scan_id} has started")
    elif message.update_type == "progress":
        print(f"Scan progress: {message.message}")
    elif message.update_type == "completed":
        print(f"Scan {message.scan_id} completed successfully")
    elif message.update_type == "error":
        print(f"Scan error: {message.message}")


async def monitor_notifications(client: TavoClient):
    """Monitor user notifications via WebSocket"""
    try:
        connection_id = await client.websocket().connect_to_notifications(
            lambda message: handle_notification(message)
        )

        print(f"Connected to notifications with connection ID: {connection_id}")

        # Keep connection alive
        await asyncio.sleep(300)  # 5 minutes

    except Exception as error:
        print(f"Failed to connect to notifications WebSocket: {error}")


def handle_notification(message: NotificationMessage):
    """Handle notification messages"""
    print(f"Notification received: {message}")

    if message.type == "info":
        print(f"ℹ️  {message.title}: {message.message}")
    elif message.type == "warning":
        print(f"⚠️  {message.title}: {message.message}")
    elif message.type == "error":
        print(f"❌ {message.title}: {message.message}")
    elif message.type == "success":
        print(f"✅ {message.title}: {message.message}")


async def monitor_general_broadcasts(client: TavoClient):
    """Monitor general broadcasts via WebSocket"""
    try:
        connection_id = await client.websocket().connect_to_general(
            lambda message: handle_general_message(message)
        )

        print(f"Connected to general broadcasts with connection ID: {connection_id}")

        # Keep connection alive
        await asyncio.sleep(300)  # 5 minutes

    except Exception as error:
        print(f"Failed to connect to general WebSocket: {error}")


def handle_general_message(message: GeneralMessage):
    """Handle general broadcast messages"""
    print(f"General broadcast: {message}")


async def cleanup_connections(client: TavoClient):
    """Clean up all WebSocket connections"""
    print("Disconnecting all WebSocket connections...")
    await client.websocket().disconnect_all()
    print("All connections closed")


async def main():
    """Main example function"""
    # Initialize the client
    client = TavoClient(
        jwt_token=os.getenv("TAVO_JWT_TOKEN"),  # or api_key/session_token
        base_url="https://api.tavoai.net",
    )

    try:
        # Start monitoring notifications (in background)
        _ = asyncio.create_task(monitor_notifications(client))

        # Start monitoring general broadcasts (in background)
        _ = asyncio.create_task(monitor_general_broadcasts(client))

        # Create and monitor a scan
        try:
            scan_result = await client.scans().create(
                repository_url="https://github.com/example/repo", scan_type="security"
            )

            print(f"Scan created: {scan_result}")
            await monitor_scan_progress(client, scan_result["id"])

        except Exception as error:
            print(f"Scan creation failed: {error}")

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await cleanup_connections(client)


if __name__ == "__main__":
    print("Tavo AI WebSocket Example")
    print("Make sure to set TAVO_JWT_TOKEN environment variable")
    print("Press Ctrl+C to exit\n")

    asyncio.run(main())
