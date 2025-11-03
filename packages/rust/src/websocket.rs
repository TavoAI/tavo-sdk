//! WebSocket operations for real-time communication with Tavo AI.
//!
//! Provides real-time scan monitoring, live updates, and bidirectional
//! communication with the Tavo AI platform.

use crate::{TavoClient, TavoError, Result};
use futures_util::{SinkExt, StreamExt};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::mpsc;
use tokio::sync::Mutex;
use tokio_tungstenite::{connect_async, tungstenite::protocol::Message};
use tokio_util::sync::CancellationToken;

/// WebSocket configuration
#[derive(Debug, Clone)]
pub struct WebSocketConfig {
    /// Reconnect interval between attempts
    pub reconnect_interval: std::time::Duration,
    /// Maximum number of reconnection attempts
    pub max_reconnect_attempts: usize,
    /// Ping interval for connection health
    pub ping_interval: std::time::Duration,
    /// Read timeout for WebSocket messages
    pub read_timeout: std::time::Duration,
    /// Write timeout for WebSocket messages
    pub write_timeout: std::time::Duration,
}

impl Default for WebSocketConfig {
    fn default() -> Self {
        Self {
            reconnect_interval: std::time::Duration::from_secs(5),
            max_reconnect_attempts: 10,
            ping_interval: std::time::Duration::from_secs(30),
            read_timeout: std::time::Duration::from_secs(60),
            write_timeout: std::time::Duration::from_secs(10),
        }
    }
}

/// WebSocket message types
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "data")]
pub enum WebSocketMessage {
    /// Scan progress update
    #[serde(rename = "scan_progress")]
    ScanProgress {
        scan_id: String,
        progress: f64,
        status: String,
        current_step: Option<String>,
        estimated_completion: Option<String>,
    },

    /// Scan completed
    #[serde(rename = "scan_completed")]
    ScanCompleted {
        scan_id: String,
        total_issues: u32,
        high_severity: u32,
        medium_severity: u32,
        low_severity: u32,
        scan_duration: u64,
    },

    /// Scan error
    #[serde(rename = "scan_error")]
    ScanError {
        scan_id: String,
        error_message: String,
        error_code: Option<String>,
    },

    /// General system update
    #[serde(rename = "system_update")]
    SystemUpdate {
        message: String,
        level: String,
        timestamp: u64,
    },

    /// Heartbeat/ping response
    #[serde(rename = "heartbeat")]
    Heartbeat {
        server_time: u64,
    },
}

/// WebSocket connection with automatic reconnection
pub struct WebSocketConnection {
    config: WebSocketConfig,
    base_url: String,
    api_key: Option<String>,
    jwt_token: Option<String>,
    session_token: Option<String>,
    endpoint: String,

    stream: Option<mpsc::UnboundedSender<WebSocketMessage>>,
    is_connected: Arc<Mutex<bool>>,
    reconnect_attempts: Arc<Mutex<usize>>,
    cancellation_token: CancellationToken,
}

impl WebSocketConnection {
    /// Create a new WebSocket connection
    pub fn new(
        base_url: String,
        endpoint: String,
        api_key: Option<String>,
        jwt_token: Option<String>,
        session_token: Option<String>,
        config: WebSocketConfig,
    ) -> Self {
        Self {
            config,
            base_url,
            api_key,
            jwt_token,
            session_token,
            endpoint,
            stream: None,
            is_connected: Arc::new(Mutex::new(false)),
            reconnect_attempts: Arc::new(Mutex::new(0)),
            cancellation_token: CancellationToken::new(),
        }
    }

    /// Connect to the WebSocket endpoint
    pub async fn connect(&mut self) -> Result<mpsc::UnboundedReceiver<WebSocketMessage>> {
        let (tx, rx) = mpsc::unbounded_channel();
        self.stream = Some(tx);

        let cancellation_token = self.cancellation_token.clone();
        let is_connected = Arc::clone(&self.is_connected);
        let reconnect_attempts = Arc::clone(&self.reconnect_attempts);
        let config = self.config.clone();
        let base_url = self.base_url.clone();
        let endpoint = self.endpoint.clone();
        let api_key = self.api_key.clone();
        let jwt_token = self.jwt_token.clone();
        let session_token = self.session_token.clone();
        let stream = self.stream.clone();

        tokio::spawn(async move {
            Self::connection_loop(
                base_url,
                endpoint,
                api_key,
                jwt_token,
                session_token,
                config,
                stream,
                is_connected,
                reconnect_attempts,
                cancellation_token,
            ).await;
        });

        Ok(rx)
    }

    /// Send a message over the WebSocket
    pub async fn send_message(&self, message: WebSocketMessage) -> Result<()> {
        if let Some(stream) = &self.stream {
            stream.send(message).map_err(|_| {
                TavoError::Api {
                    message: "Failed to send WebSocket message".to_string(),
                }
            })?;
        }
        Ok(())
    }

    /// Check if the connection is currently active
    pub async fn is_connected(&self) -> bool {
        *self.is_connected.lock().await
    }

    /// Disconnect from the WebSocket
    pub async fn disconnect(&self) -> Result<()> {
        self.cancellation_token.cancel();
        Ok(())
    }

    /// Internal connection loop with automatic reconnection
    async fn connection_loop(
        base_url: String,
        endpoint: String,
        api_key: Option<String>,
        jwt_token: Option<String>,
        session_token: Option<String>,
        config: WebSocketConfig,
        stream: Option<mpsc::UnboundedSender<WebSocketMessage>>,
        is_connected: Arc<Mutex<bool>>,
        reconnect_attempts: Arc<Mutex<usize>>,
        cancellation_token: CancellationToken,
    ) {
        loop {
            tokio::select! {
                _ = cancellation_token.cancelled() => {
                    break;
                }
                _ = Self::attempt_connection(
                    &base_url,
                    &endpoint,
                    &api_key,
                    &jwt_token,
                    &session_token,
                    &config,
                    &stream,
                    &is_connected,
                    &reconnect_attempts,
                    &cancellation_token,
                ) => {
                    // Connection attempt completed, will retry if needed
                }
            }

            if cancellation_token.is_cancelled() {
                break;
            }

            // Wait before attempting to reconnect
            tokio::time::sleep(config.reconnect_interval).await;
        }
    }

    /// Attempt a single WebSocket connection
    async fn attempt_connection(
        base_url: &str,
        endpoint: &str,
        api_key: &Option<String>,
        jwt_token: &Option<String>,
        session_token: &Option<String>,
        config: &WebSocketConfig,
        stream: &Option<mpsc::UnboundedSender<WebSocketMessage>>,
        is_connected: &Arc<Mutex<bool>>,
        reconnect_attempts: &Arc<Mutex<usize>>,
        cancellation_token: &CancellationToken,
    ) {
        let mut attempts = reconnect_attempts.lock().await;
        *attempts += 1;

        println!("Attempting WebSocket connection (attempt {})", *attempts);

        // Convert HTTP URL to WebSocket URL
        let ws_url = if base_url.starts_with("https://") {
            format!("wss://{}", &base_url[8..])
        } else if base_url.starts_with("http://") {
            format!("ws://{}", &base_url[7..])
        } else {
            base_url.to_string()
        };

        let full_url = format!("{}{}", ws_url, endpoint);

        // Create request with authentication headers
        let mut request = tokio_tungstenite::tungstenite::client::IntoClientRequest::into_client_request(&full_url)
            .expect("Failed to create WebSocket request");

        let headers = request.headers_mut();
        if let Some(api_key) = api_key {
            headers.insert("X-API-Key", api_key.parse().unwrap());
        }
        if let Some(jwt_token) = jwt_token {
            headers.insert("Authorization", format!("Bearer {}", jwt_token).parse().unwrap());
        }
        if let Some(session_token) = session_token {
            headers.insert("X-Session-Token", session_token.parse().unwrap());
        }

        // Attempt to connect
        match connect_async(request).await {
            Ok((ws_stream, _)) => {
                println!("WebSocket connected successfully");
                *is_connected.lock().await = true;
                *reconnect_attempts.lock().await = 0;

                // Handle the WebSocket stream
                Self::handle_stream(
                    ws_stream,
                    stream,
                    is_connected,
                    config.clone(),
                    cancellation_token.clone(),
                ).await;
            }
            Err(e) => {
                println!("WebSocket connection failed: {:?}", e);
                *is_connected.lock().await = false;

                if *attempts >= config.max_reconnect_attempts {
                    println!("Max reconnection attempts reached, giving up");
                    return;
                }
            }
        }
    }

    /// Handle the WebSocket stream once connected
    async fn handle_stream(
        ws_stream: tokio_tungstenite::WebSocketStream<tokio_tungstenite::MaybeTlsStream<tokio::net::TcpStream>>,
        stream: &Option<mpsc::UnboundedSender<WebSocketMessage>>,
        is_connected: &Arc<Mutex<bool>>,
        config: WebSocketConfig,
        cancellation_token: CancellationToken,
    ) {
        let (write, read) = ws_stream.split();
        let write = Arc::new(Mutex::new(write));

        // Ping task
        let ping_write = Arc::clone(&write);
        let ping_token = cancellation_token.clone();
        let ping_interval = config.ping_interval;
        let ping_handle = tokio::spawn(async move {
            let mut interval = tokio::time::interval(ping_interval);
            loop {
                tokio::select! {
                    _ = ping_token.cancelled() => break,
                    _ = interval.tick() => {
                        let mut write_guard = ping_write.lock().await;
                        if let Err(_) = write_guard.send(Message::Ping(vec![])).await {
                            break;
                        }
                    }
                }
            }
        });

        // Read messages
        let mut read_stream = read;
        while let Some(message) = tokio::select! {
            message = read_stream.next() => message,
            _ = cancellation_token.cancelled() => None,
        } {
            match message {
                Ok(Message::Text(text)) => {
                    if let Ok(ws_message) = serde_json::from_str::<WebSocketMessage>(&text) {
                        if let Some(ref stream_sender) = stream {
                            let _ = stream_sender.send(ws_message);
                        }
                    }
                }
                Ok(Message::Close(_)) => {
                    println!("WebSocket closed by server");
                    break;
                }
                Ok(Message::Ping(data)) => {
                    let mut write_guard = write.lock().await;
                    let _ = write_guard.send(Message::Pong(data)).await;
                }
                Err(e) => {
                    println!("WebSocket error: {:?}", e);
                    break;
                }
                _ => {} // Ignore other message types
            }
        }

        // Clean up
        *is_connected.lock().await = false;
        ping_handle.abort();
        let _ = ping_handle.await;
    }
}

/// WebSocket operations for real-time communication
pub struct WebSocketOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> WebSocketOperations<'a> {
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Connect to real-time scan progress updates for a specific scan
    ///
    /// # Arguments
    ///
    /// * `scan_id` - The scan ID to monitor
    /// * `config` - WebSocket configuration (optional, uses defaults if None)
    ///
    /// # Returns
    ///
    /// A receiver channel for WebSocket messages and the connection handle
    ///
    pub async fn connect_to_scan_progress(
        &self,
        scan_id: &str,
        config: Option<WebSocketConfig>,
    ) -> Result<WebSocketConnection> {
        let config = config.unwrap_or_default();
        let endpoint = format!("/api/v1/code/scans/{}/progress", scan_id);

        let mut connection = WebSocketConnection::new(
            self.client.base_url.clone(),
            endpoint,
            self.client.api_key.clone(),
            self.client.jwt_token.clone(),
            self.client.session_token.clone(),
            config,
        );

        // We don't need the receiver for this API - just the connection
        let _receiver = connection.connect().await?;

        Ok(connection)
    }

    /// Connect to general real-time updates
    ///
    /// # Arguments
    ///
    /// * `config` - WebSocket configuration (optional, uses defaults if None)
    ///
    /// # Returns
    ///
    /// A WebSocket connection for receiving general updates
    ///
    pub async fn connect_to_general_updates(
        &self,
        config: Option<WebSocketConfig>,
    ) -> Result<WebSocketConnection> {
        let config = config.unwrap_or_default();
        let endpoint = "/api/v1/updates".to_string();

        let mut connection = WebSocketConnection::new(
            self.client.base_url.clone(),
            endpoint,
            self.client.api_key.clone(),
            self.client.jwt_token.clone(),
            self.client.session_token.clone(),
            config,
        );

        // We don't need the receiver for this API - just the connection
        let _receiver = connection.connect().await?;

        Ok(connection)
    }
}
