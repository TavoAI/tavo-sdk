package net.tavoai;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import org.json.JSONObject;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Consumer;

/**
 * WebSocket operations for real-time communication with Tavo AI.
 */
public class WebSocketOperations {
    private final TavoClient client;

    public WebSocketOperations(TavoClient client) {
        this.client = client;
    }

    /**
     * WebSocket configuration
     */
    public static class WebSocketConfig {
        private int reconnectIntervalMs = 5000;
        private int maxReconnectAttempts = 10;
        private int pingIntervalMs = 30000;
        private int readTimeoutMs = 60000;
        private int writeTimeoutMs = 10000;

        public WebSocketConfig() {}

        public WebSocketConfig setReconnectIntervalMs(int reconnectIntervalMs) {
            this.reconnectIntervalMs = reconnectIntervalMs;
            return this;
        }

        public WebSocketConfig setMaxReconnectAttempts(int maxReconnectAttempts) {
            this.maxReconnectAttempts = maxReconnectAttempts;
            return this;
        }

        public WebSocketConfig setPingIntervalMs(int pingIntervalMs) {
            this.pingIntervalMs = pingIntervalMs;
            return this;
        }

        public WebSocketConfig setReadTimeoutMs(int readTimeoutMs) {
            this.readTimeoutMs = readTimeoutMs;
            return this;
        }

        public WebSocketConfig setWriteTimeoutMs(int writeTimeoutMs) {
            this.writeTimeoutMs = writeTimeoutMs;
            return this;
        }

        public int getReconnectIntervalMs() { return reconnectIntervalMs; }
        public int getMaxReconnectAttempts() { return maxReconnectAttempts; }
        public int getPingIntervalMs() { return pingIntervalMs; }
        public int getReadTimeoutMs() { return readTimeoutMs; }
        public int getWriteTimeoutMs() { return writeTimeoutMs; }
    }

    /**
     * WebSocket connection with automatic reconnection
     */
    public static class WebSocketConnection extends WebSocketClient {
        private final WebSocketConfig config;
        private final TavoClient client;
        private final Consumer<String> messageHandler;
        private final Consumer<Exception> errorHandler;
        private final Runnable connectHandler;
        private final Runnable disconnectHandler;

        private final AtomicBoolean connected = new AtomicBoolean(false);
        private final AtomicBoolean reconnecting = new AtomicBoolean(false);
        private volatile int reconnectAttempts = 0;
        private volatile Thread pingThread;
        private volatile boolean shouldRun = true;

        public WebSocketConnection(
            URI serverUri,
            WebSocketConfig config,
            TavoClient client,
            Consumer<String> messageHandler,
            Consumer<Exception> errorHandler,
            Runnable connectHandler,
            Runnable disconnectHandler
        ) {
            super(serverUri);
            this.config = config;
            this.client = client;
            this.messageHandler = messageHandler;
            this.errorHandler = errorHandler;
            this.connectHandler = connectHandler;
            this.disconnectHandler = disconnectHandler;

            // Add authentication headers
            if (client.config.getApiKey() != null) {
                addHeader("X-API-Key", client.config.getApiKey());
            }
            if (client.config.getJwtToken() != null) {
                addHeader("Authorization", "Bearer " + client.config.getJwtToken());
            }
            if (client.config.getSessionToken() != null) {
                addHeader("X-Session-Token", client.config.getSessionToken());
            }
        }

        @Override
        public void onOpen(ServerHandshake handshake) {
            connected.set(true);
            reconnectAttempts = 0;
            System.out.println("WebSocket connected");

            // Start ping thread
            startPingThread();

            if (connectHandler != null) {
                connectHandler.run();
            }
        }

        @Override
        public void onMessage(String message) {
            if (messageHandler != null) {
                messageHandler.accept(message);
            }
        }

        @Override
        public void onClose(int code, String reason, boolean remote) {
            connected.set(false);
            System.out.println("WebSocket closed: " + code + " " + reason);

            stopPingThread();

            if (disconnectHandler != null) {
                disconnectHandler.run();
            }

            // Attempt to reconnect if not manually closed
            if (shouldRun && remote) {
                attemptReconnect();
            }
        }

        @Override
        public void onError(Exception ex) {
            System.err.println("WebSocket error: " + ex.getMessage());
            if (errorHandler != null) {
                errorHandler.accept(ex);
            }
        }

        private void startPingThread() {
            pingThread = new Thread(() -> {
                while (shouldRun && connected.get()) {
                    try {
                        Thread.sleep(config.getPingIntervalMs());
                        if (connected.get()) {
                            sendPing();
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
            pingThread.setDaemon(true);
            pingThread.start();
        }

        private void stopPingThread() {
            if (pingThread != null) {
                pingThread.interrupt();
                try {
                    pingThread.join(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }

        private void attemptReconnect() {
            if (reconnecting.get() || !shouldRun) {
                return;
            }

            reconnecting.set(true);

            new Thread(() -> {
                try {
                    while (shouldRun && reconnectAttempts < config.getMaxReconnectAttempts()) {
                        reconnectAttempts++;
                        System.out.println("Attempting to reconnect (" + reconnectAttempts + "/" + config.getMaxReconnectAttempts() + ")");

                        try {
                            Thread.sleep(config.getReconnectIntervalMs());
                            reconnectBlocking();
                            System.out.println("Successfully reconnected on attempt " + reconnectAttempts);
                            return;
                        } catch (Exception e) {
                            System.err.println("Reconnection attempt " + reconnectAttempts + " failed: " + e.getMessage());
                        }
                    }

                    System.err.println("Failed to reconnect after " + config.getMaxReconnectAttempts() + " attempts");
                } finally {
                    reconnecting.set(false);
                }
            }).start();
        }

        /**
         * Send a message over the WebSocket
         */
        public void sendMessage(String messageType, Object data) {
            if (!connected.get()) {
                throw new IllegalStateException("Not connected");
            }

            JSONObject message = new JSONObject();
            message.put("type", messageType);
            message.put("data", data);
            message.put("timestamp", System.currentTimeMillis() / 1000);

            send(message.toString());
        }

        /**
         * Close the connection gracefully
         */
        public void closeConnection() {
            shouldRun = false;
            connected.set(false);
            stopPingThread();

            try {
                closeBlocking();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        /**
         * Check if the connection is active
         */
        public boolean isConnected() {
            return connected.get();
        }
    }

    /**
     * Create a default WebSocket configuration
     */
    public static WebSocketConfig defaultConfig() {
        return new WebSocketConfig();
    }

    /**
     * Connect to real-time scan progress updates for a specific scan
     */
    public CompletableFuture<WebSocketConnection> connectToScanProgress(
        String scanId,
        WebSocketConfig config,
        Consumer<String> messageHandler,
        Consumer<Exception> errorHandler,
        Runnable connectHandler,
        Runnable disconnectHandler
    ) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                String wsUrl = client.getBaseUrl().replaceFirst("^http", "ws") +
                               "/api/v1/code/scans/" + scanId + "/progress";

                URI uri = new URI(wsUrl);
                WebSocketConnection connection = new WebSocketConnection(
                    uri, config, client, messageHandler, errorHandler, connectHandler, disconnectHandler
                );

                connection.connectBlocking();
                return connection;

            } catch (URISyntaxException | InterruptedException e) {
                throw new RuntimeException("Failed to connect to scan progress WebSocket", e);
            }
        });
    }

    /**
     * Connect to general real-time updates
     */
    public CompletableFuture<WebSocketConnection> connectToGeneralUpdates(
        WebSocketConfig config,
        Consumer<String> messageHandler,
        Consumer<Exception> errorHandler,
        Runnable connectHandler,
        Runnable disconnectHandler
    ) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                String wsUrl = client.getBaseUrl().replaceFirst("^http", "ws") + "/api/v1/updates";

                URI uri = new URI(wsUrl);
                WebSocketConnection connection = new WebSocketConnection(
                    uri, config, client, messageHandler, errorHandler, connectHandler, disconnectHandler
                );

                connection.connectBlocking();
                return connection;

            } catch (URISyntaxException | InterruptedException e) {
                throw new RuntimeException("Failed to connect to general updates WebSocket", e);
            }
        });
    }
}
