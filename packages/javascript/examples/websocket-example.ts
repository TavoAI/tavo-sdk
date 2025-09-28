/**
 * Tavo AI JavaScript SDK - WebSocket Example
 *
 * This example demonstrates how to use WebSocket connections for real-time features
 * including scan progress updates, notifications, and general broadcasts.
 */

import { GeneralMessage, NotificationMessage, ScanUpdateMessage, TavoClient } from '../src/index.js';

// Initialize the client
const client = new TavoClient({
    jwtToken: 'your-jwt-token-here', // or apiKey/sessionToken
    baseURL: 'https://api.tavoai.net',
});

// Example 1: Connect to scan progress updates
async function monitorScanProgress(scanId: string) {
    try {
        const connectionId = await client.websocket.connectToScan(
            scanId,
            (message: ScanUpdateMessage) => {
                console.log('Scan update:', message);

                switch (message.update_type) {
                    case 'started':
                        console.log(`Scan ${message.scan_id} has started`);
                        break;
                    case 'progress':
                        console.log(`Scan progress: ${message.message}`);
                        break;
                    case 'completed':
                        console.log(`Scan ${message.scan_id} completed successfully`);
                        // Disconnect when scan is done
                        client.websocket.disconnect(connectionId);
                        break;
                    case 'error':
                        console.error(`Scan error: ${message.message}`);
                        client.websocket.disconnect(connectionId);
                        break;
                }
            }
        );

        console.log(`Connected to scan ${scanId} with connection ID: ${connectionId}`);

        // Optional: Send a ping message
        setTimeout(() => {
            client.websocket.sendMessage(connectionId, { type: 'ping' });
        }, 5000);

    } catch (error) {
        console.error('Failed to connect to scan WebSocket:', error);
    }
}

// Example 2: Connect to notifications
async function monitorNotifications() {
    try {
        const connectionId = await client.websocket.connectToNotifications(
            (message: NotificationMessage) => {
                console.log('Notification received:', message);

                switch (message.type) {
                    case 'info':
                        console.info(message.title, message.message);
                        break;
                    case 'warning':
                        console.warn(message.title, message.message);
                        break;
                    case 'error':
                        console.error(message.title, message.message);
                        break;
                    case 'success':
                        console.log('✅', message.title, message.message);
                        break;
                }
            }
        );

        console.log(`Connected to notifications with connection ID: ${connectionId}`);

    } catch (error) {
        console.error('Failed to connect to notifications WebSocket:', error);
    }
}

// Example 3: Connect to general broadcasts
async function monitorGeneralBroadcasts() {
    try {
        const connectionId = await client.websocket.connectToGeneral(
            (message: GeneralMessage) => {
                console.log('General broadcast:', message);
            }
        );

        console.log(`Connected to general broadcasts with connection ID: ${connectionId}`);

    } catch (error) {
        console.error('Failed to connect to general WebSocket:', error);
    }
}

// Example 4: Clean up connections
async function cleanup() {
    console.log('Disconnecting all WebSocket connections...');
    await client.websocket.disconnectAll();
    console.log('All connections closed');
}

// Usage examples
async function main() {
    // Start monitoring notifications (long-running)
    await monitorNotifications();

    // Start monitoring general broadcasts (long-running)
    await monitorGeneralBroadcasts();

    // Create and monitor a scan
    try {
        const scanResult = await client.scans.create({
            repositoryUrl: 'https://github.com/example/repo',
            scanType: 'security'
        });

        console.log('Scan created:', scanResult);
        await monitorScanProgress(scanResult.id);

    } catch (error) {
        console.error('Scan creation failed:', error);
    }

    // Keep the process running for a while to receive messages
    console.log('Listening for real-time updates... Press Ctrl+C to exit');

    // In a real application, you might want to handle graceful shutdown
    process.on('SIGINT', async () => {
        await cleanup();
        process.exit(0);
    });
}

// Run the example
main().catch(console.error);