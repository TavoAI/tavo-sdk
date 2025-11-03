//! Device authentication operations for CLI tools and scanners.
//!
//! Provides device code flow authentication optimized for command-line tools
//! and automated scanners. Includes usage tracking and limits management.

use crate::{TavoClient, TavoError, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use tokio_util::sync::CancellationToken;

/// Device code response for CLI authentication
#[derive(Deserialize, Debug, Clone)]
pub struct DeviceCodeResponse {
    pub device_code: String,
    pub user_code: String,
    pub verification_uri: String,
    pub verification_uri_complete: Option<String>,
    pub expires_in: u32,
    pub interval: u32,
}

/// Device token response after polling
#[derive(Deserialize, Debug, Clone)]
pub struct DeviceTokenResponse {
    pub access_token: String,
    pub token_type: String,
    pub expires_in: u32,
    pub refresh_token: Option<String>,
}

/// Usage warnings and limits information
#[derive(Deserialize, Debug, Clone)]
pub struct UsageWarnings {
    pub warnings: Vec<String>,
    pub limits: HashMap<String, serde_json::Value>,
}

/// Device operations for CLI tools and scanners
pub struct DeviceOperations<'a> {
    pub client: &'a TavoClient,
}

impl<'a> DeviceOperations<'a> {
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Create device code for authentication
    ///
    /// # Arguments
    ///
    /// * `client_id` - Optional client ID for the device
    /// * `client_name` - Optional client name for the device
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let device_code = client.device().create_device_code(Some("cli-tool"), Some("Tavo CLI")).await?;
    /// println!("Go to {} and enter: {}", device_code.verification_uri, device_code.user_code);
    /// # Ok(())
    /// # }
    /// ```
    pub async fn create_device_code(
        &self,
        client_id: Option<&str>,
        client_name: Option<&str>,
    ) -> Result<DeviceCodeResponse> {
        let mut data = HashMap::new();
        if let Some(client_id) = client_id {
            data.insert("client_id".to_string(), serde_json::Value::String(client_id.to_string()));
        }
        if let Some(client_name) = client_name {
            data.insert("client_name".to_string(), serde_json::Value::String(client_name.to_string()));
        }

        self.client.post("/device/code", &data).await
    }

    /// Create CLI-optimized device code for authentication
    ///
    /// # Arguments
    ///
    /// * `client_id` - Optional client ID for the CLI tool
    /// * `client_name` - Optional client name (defaults to "Tavo CLI")
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let device_code = client.device().create_device_code_for_cli(None, None).await?;
    /// // Optimized for CLI tools - shorter polling interval, better error messages
    /// # Ok(())
    /// # }
    /// ```
    pub async fn create_device_code_for_cli(
        &self,
        client_id: Option<&str>,
        client_name: Option<&str>,
    ) -> Result<DeviceCodeResponse> {
        let client_name = client_name.unwrap_or("Tavo CLI");

        let mut data = HashMap::new();
        data.insert("client_name".to_string(), serde_json::Value::String(client_name.to_string()));
        if let Some(client_id) = client_id {
            data.insert("client_id".to_string(), serde_json::Value::String(client_id.to_string()));
        }

        self.client.post("/device/code/cli", &data).await
    }

    /// Poll for device token (after user has authorized the device)
    ///
    /// # Arguments
    ///
    /// * `device_code` - The device code to poll for
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let token = client.device().poll_device_token("device-code-123").await?;
    /// // Use token.access_token for authenticated requests
    /// # Ok(())
    /// # }
    /// ```
    pub async fn poll_device_token(&self, device_code: &str) -> Result<DeviceTokenResponse> {
        let mut data = HashMap::new();
        data.insert("device_code".to_string(), serde_json::Value::String(device_code.to_string()));

        self.client.post("/device/token", &data).await
    }

    /// Get device code status (lightweight polling for CLI)
    ///
    /// # Arguments
    ///
    /// * `device_code` - The device code to check
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let status = client.device().get_device_code_status("device-code-123").await?;
    /// // Check if user has authorized the device yet
    /// # Ok(())
    /// # }
    /// ```
    pub async fn get_device_code_status(&self, device_code: &str) -> Result<HashMap<String, serde_json::Value>> {
        self.client.get(&format!("/device/code/{}/status", device_code)).await
    }

    /// Get usage warnings and limits for CLI tools
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let warnings = client.device().get_usage_warnings().await?;
    /// for warning in warnings.warnings {
    ///     println!("Warning: {}", warning);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub async fn get_usage_warnings(&self) -> Result<UsageWarnings> {
        self.client.get("/device/usage/warnings").await
    }

    /// Get current limits and quotas for CLI tools
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let limits = client.device().get_limits().await?;
    /// // Check rate limits and quotas
    /// # Ok(())
    /// # }
    /// ```
    pub async fn get_limits(&self) -> Result<HashMap<String, serde_json::Value>> {
        self.client.get("/device/limits").await
    }
}

// ===========================================
// Cancellable Operations with CancellationToken
// ===========================================

impl<'a> DeviceOperations<'a> {
    /// Create device code with cancellation support
    ///
    /// # Arguments
    ///
    /// * `client_id` - Optional client ID
    /// * `client_name` - Optional client name
    /// * `cancellation_token` - Token for cancelling the operation
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # use tokio_util::sync::CancellationToken;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let token = CancellationToken::new();
    ///
    /// // Cancel after 5 seconds
    /// let token_clone = token.clone();
    /// tokio::spawn(async move {
    ///     tokio::time::sleep(tokio::time::Duration::from_secs(5)).await;
    ///     token_clone.cancel();
    /// });
    ///
    /// let result = client.device().create_device_code_cancellable(None, None, &token).await;
    /// // Will either succeed or return cancellation error
    /// # Ok(())
    /// # }
    /// ```
    pub async fn create_device_code_cancellable(
        &self,
        client_id: Option<&str>,
        client_name: Option<&str>,
        cancellation_token: &CancellationToken,
    ) -> Result<DeviceCodeResponse> {
        tokio::select! {
            result = self.create_device_code(client_id, client_name) => result,
            _ = cancellation_token.cancelled() => {
                Err(crate::TavoError::Api { message: "Operation cancelled".to_string() })
            }
        }
    }

    /// Poll device token with cancellation support
    ///
    /// # Arguments
    ///
    /// * `device_code` - The device code to poll for
    /// * `cancellation_token` - Token for cancelling the operation
    pub async fn poll_device_token_cancellable(
        &self,
        device_code: &str,
        cancellation_token: &CancellationToken,
    ) -> Result<DeviceTokenResponse> {
        tokio::select! {
            result = self.poll_device_token(device_code) => result,
            _ = cancellation_token.cancelled() => {
                Err(crate::TavoError::Api { message: "Operation cancelled".to_string() })
            }
        }
    }
}
