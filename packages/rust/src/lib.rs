//! # Tavo AI Rust SDK - Tooling-Focused Implementation
//!
//! Memory-safe, high-performance Rust SDK for CLI tools, scanners, and automated security analysis.
//! Features async runtime integration, cancellation support, and comprehensive tooling endpoints.
//!
//! ## Core Features
//!
//! - **Async/Await**: Full tokio async runtime integration
//! - **Cancellation**: Cooperative cancellation using tokio-util CancellationToken
//! - **Memory Safe**: Zero-cost abstractions with Rust's ownership system
//! - **Tooling Focused**: Optimized for CLI tools, scanners, and automation
//! - **Type Safe**: Compile-time guarantees with Rust's type system
//!
//! ## Week 15/16 Tooling Endpoints
//!
//! - **Device Auth**: CLI device code flow with polling and status tracking
//! - **Scanner Integration**: Rule/plugin discovery, heartbeats, recommendations
//! - **Code Submission**: Direct file/repo/code analysis with scan status/results
//!
//! ## Example Usage
//!
//! ### Device Authentication (CLI Tools)
//!
//! ```rust,no_run
//! use tavo_ai::TavoClient;
//!
//! #[tokio::main]
//! async fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let client = TavoClient::new("your-api-key")?;
//!
//!     // Create device code for CLI authentication
//!     let device_code = client.device()
//!         .create_device_code_for_cli(None, None)
//!         .await?;
//!
//!     println!("Go to {} and enter: {}", device_code.verification_uri, device_code.user_code);
//!
//!     // Poll for token (with timeout)
//!     let token = client.device()
//!         .poll_device_token(&device_code.device_code)
//!         .await?;
//!
//!     // Use authenticated client
//!     let limits = client.device().get_limits().await?;
//!     Ok(())
//! }
//! ```
//!
//! ### Scanner Integration
//!
//! ```rust,no_run
//! use tavo_ai::{TavoClient, HeartbeatData};
//!
//! #[tokio::main]
//! async fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let client = TavoClient::new("api-key")?;
//!
//!     // Discover rules for Rust security scanning
//!     let rules = client.scanner()
//!         .discover_rules(Some("sast"), Some("rust"), None)
//!         .await?;
//!
//!     // Send scanner heartbeat
//!     let mut system_info = std::collections::HashMap::new();
//!     system_info.insert("os".to_string(), serde_json::Value::String("linux".to_string()));
//!
//!     let heartbeat = HeartbeatData {
//!         scanner_version: "1.0.0".to_string(),
//!         scanner_type: "sast".to_string(),
//!         active_rules: rules.iter().map(|r| r.id.clone()).collect(),
//!         active_plugins: vec!["rust-security".to_string()],
//!         system_info,
//!         scan_count: Some(42),
//!     };
//!
//!     let response = client.scanner().send_heartbeat(heartbeat).await?;
//!     Ok(())
//! }
//! ```
//!
//! ### Code Submission and Analysis
//!
//! ```rust,no_run
//! use tavo_ai::{TavoClient, FileInfo};
//!
//! #[tokio::main]
//! async fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let client = TavoClient::new("api-key")?;
//!
//!     // Submit code for analysis
//!     let files = vec![FileInfo {
//!         filename: "main.rs".to_string(),
//!         content: "fn main() { println!(\"Hello!\"); }".to_string(),
//!         language: Some("rust".to_string()),
//!     }];
//!
//!     let submission = client.code_submission()
//!         .submit_code(files, Some("my-repo"), Some("main"), None, None)
//!         .await?;
//!
//!     // Check scan status
//!     loop {
//!         let status = client.code_submission()
//!             .get_scan_status(&submission.scan_id)
//!             .await?;
//!
//!         match status.status.as_str() {
//!             "completed" => break,
//!             "failed" => return Err("Scan failed".into()),
//!             _ => {
//!                 tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;
//!             }
//!         }
//!     }
//!
//!     // Get results
//!     let results = client.code_submission()
//!         .get_scan_results(&submission.scan_id)
//!         .await?;
//!
//!     println!("Found {} issues", results.total_issues);
//!     Ok(())
//! }
//! ```
//!
//! ### Cancellation Support
//!
//! ```rust,no_run
//! use tavo_ai::TavoClient;
//! use tokio_util::sync::CancellationToken;
//!
//! #[tokio::main]
//! async fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let client = TavoClient::new("api-key")?;
//!     let token = CancellationToken::new();
//!
//!     // Cancel operation after 30 seconds
//!     let token_clone = token.clone();
//!     tokio::spawn(async move {
//!         tokio::time::sleep(tokio::time::Duration::from_secs(30)).await;
//!         token_clone.cancel();
//!     });
//!
//!     // Operation will be cancelled if it takes too long
//!     let result = client.device()
//!         .create_device_code_cancellable(None, None, &token)
//!         .await;
//!
//!     match result {
//!         Ok(code) => println!("Got device code: {}", code.device_code),
//!         Err(e) if e.to_string().contains("cancelled") => println!("Operation was cancelled"),
//!         Err(e) => return Err(e.into()),
//!     }
//!
//!     Ok(())
//! }
//! ```

pub mod ai_analysis;
pub mod auth;
pub mod billing;
pub mod code_submission;
pub mod device;
pub mod jobs;
pub mod organizations;
pub mod reports;
pub mod scans;
pub mod scanner;
pub mod users;
pub mod webhooks;
pub mod websocket;

use reqwest::Client;
use serde::Deserialize;
use std::collections::HashMap;
use thiserror::Error;

pub use ai_analysis::*;
pub use auth::*;
pub use billing::*;
pub use code_submission::*;
pub use device::*;
pub use jobs::*;
pub use organizations::*;
pub use reports::*;
pub use scans::*;
pub use scanner::*;
pub use users::*;
pub use webhooks::*;
pub use websocket::*;

/// Errors that can occur when using the Tavo AI SDK
#[derive(Error, Debug)]
pub enum TavoError {
    #[error("HTTP request failed: {0}")]
    Http(#[from] reqwest::Error),

    #[error("JSON serialization failed: {0}")]
    Json(#[from] serde_json::Error),

    #[error("Invalid API key")]
    InvalidApiKey,

    #[error("API error: {message}")]
    Api { message: String },
}

/// Result type for Tavo AI operations
pub type Result<T> = std::result::Result<T, TavoError>;

/// Main client for interacting with the Tavo AI API
pub struct TavoClient {
    client: Client,
    api_key: Option<String>,
    jwt_token: Option<String>,
    session_token: Option<String>,
    base_url: String,
}

impl TavoClient {
    /// Create a new TavoClient with the given API key
    ///
    /// # Arguments
    ///
    /// * `api_key` - Your Tavo AI API key
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// use tavo_ai::TavoClient;
    ///
    /// let client = TavoClient::new("your-api-key")?;
    /// # Ok::<(), Box<dyn std::error::Error>>(())
    /// ```
    pub fn new(api_key: impl Into<String>) -> Result<Self> {
        Self::with_api_key(api_key)
    }

    /// Create a new TavoClient with API key authentication
    pub fn with_api_key(api_key: impl Into<String>) -> Result<Self> {
        let api_key = api_key.into();
        if api_key.is_empty() {
            return Err(TavoError::InvalidApiKey);
        }

        Ok(Self {
            client: Client::new(),
            api_key: Some(api_key),
            jwt_token: None,
            session_token: None,
            base_url: "https://api.tavoai.net".to_string(),
        })
    }

    /// Create a new TavoClient with JWT token authentication
    pub fn with_jwt_token(jwt_token: impl Into<String>) -> Result<Self> {
        let jwt_token = jwt_token.into();
        if jwt_token.is_empty() {
            return Err(TavoError::InvalidApiKey);
        }

        Ok(Self {
            client: Client::new(),
            api_key: None,
            jwt_token: Some(jwt_token),
            session_token: None,
            base_url: "https://api.tavoai.net".to_string(),
        })
    }

    /// Create a new TavoClient with session token authentication
    pub fn with_session_token(session_token: impl Into<String>) -> Result<Self> {
        let session_token = session_token.into();
        if session_token.is_empty() {
            return Err(TavoError::InvalidApiKey);
        }

        Ok(Self {
            client: Client::new(),
            api_key: None,
            jwt_token: None,
            session_token: Some(session_token),
            base_url: "https://api.tavoai.net".to_string(),
        })
    }

    /// Create a new TavoClient with custom base URL
    pub fn with_base_url(api_key: impl Into<String>, base_url: impl Into<String>) -> Result<Self> {
        let api_key = api_key.into();
        if api_key.is_empty() {
            return Err(TavoError::InvalidApiKey);
        }

        Ok(Self {
            client: Client::new(),
            api_key: Some(api_key),
            jwt_token: None,
            session_token: None,
            base_url: base_url.into(),
        })
    }

    /// Create a request builder with appropriate authentication headers
    fn authenticated_request(&self, method: reqwest::Method, url: &str) -> reqwest::RequestBuilder {
        let mut request = self.client.request(method, url);

        if let Some(jwt_token) = &self.jwt_token {
            request = request.header("Authorization", format!("Bearer {}", jwt_token));
        } else if let Some(session_token) = &self.session_token {
            request = request.header("X-Session-Token", session_token);
        } else if let Some(api_key) = &self.api_key {
            request = request.header("X-API-Key", api_key);
        }

        request
    }

    // Helper methods for making HTTP requests

    /// Make a GET request and deserialize JSON response
    async fn get<T: for<'de> Deserialize<'de>>(&self, endpoint: &str) -> Result<T> {
        let url = format!("{}/api/v1{}", self.base_url, endpoint);
        let response = self
            .authenticated_request(reqwest::Method::GET, &url)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        let result = response.json().await?;
        Ok(result)
    }

    /// Make a GET request with query parameters
    async fn get_with_params<T: for<'de> Deserialize<'de>>(
        &self,
        endpoint: &str,
        params: &HashMap<String, serde_json::Value>,
    ) -> Result<T> {
        let mut url = format!("{}/api/v1{}", self.base_url, endpoint);
        if !params.is_empty() {
            url.push('?');
            for (key, value) in params {
                if !url.ends_with('?') {
                    url.push('&');
                }
                url.push_str(&format!("{}={}", key, value));
            }
        }

        let response = self
            .authenticated_request(reqwest::Method::GET, &url)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        let result = response.json().await?;
        Ok(result)
    }

    /// Make a POST request
    async fn post<T: for<'de> Deserialize<'de>>(
        &self,
        endpoint: &str,
        data: &HashMap<String, serde_json::Value>,
    ) -> Result<T> {
        let url = format!("{}/api/v1{}", self.base_url, endpoint);
        let response = self
            .authenticated_request(reqwest::Method::POST, &url)
            .json(data)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        let result = response.json().await?;
        Ok(result)
    }

    /// Make a PUT request
    async fn put<T: for<'de> Deserialize<'de>>(
        &self,
        endpoint: &str,
        data: &HashMap<String, serde_json::Value>,
    ) -> Result<T> {
        let url = format!("{}/api/v1{}", self.base_url, endpoint);
        let response = self
            .authenticated_request(reqwest::Method::PUT, &url)
            .json(data)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        let result = response.json().await?;
        Ok(result)
    }

    /// Make a DELETE request
    async fn delete(&self, endpoint: &str) -> Result<()> {
        let url = format!("{}/api/v1{}", self.base_url, endpoint);
        let response = self
            .authenticated_request(reqwest::Method::DELETE, &url)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        Ok(())
    }

    /// Get raw text response
    async fn get_text(&self, endpoint: &str) -> Result<String> {
        let url = format!("{}/api/v1{}", self.base_url, endpoint);
        let response = self
            .authenticated_request(reqwest::Method::GET, &url)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        let result = response.text().await?;
        Ok(result)
    }

    /// Get raw bytes response
    async fn get_bytes(&self, endpoint: &str) -> Result<Vec<u8>> {
        let url = format!("{}/api/v1{}", self.base_url, endpoint);
        let response = self
            .authenticated_request(reqwest::Method::GET, &url)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        let result = response.bytes().await?;
        Ok(result.to_vec())
    }

    // Operation accessors

    /// Get authentication operations
    pub fn auth(&self) -> AuthOperations<'_> {
        AuthOperations::new(self)
    }

    /// Get user operations
    pub fn users(&self) -> UserOperations<'_> {
        UserOperations::new(self)
    }

    /// Get organization operations
    pub fn organizations(&self) -> OrganizationOperations<'_> {
        OrganizationOperations::new(self)
    }

    /// Get scan operations
    pub fn scans(&self) -> ScanOperations<'_> {
        ScanOperations::new(self)
    }

    /// Get job operations
    pub fn jobs(&self) -> JobOperations<'_> {
        JobOperations::new(self)
    }

    /// Get webhook operations
    pub fn webhooks(&self) -> WebhookOperations<'_> {
        WebhookOperations::new(self)
    }

    /// Get AI analysis operations
    pub fn ai_analysis(&self) -> AIAnalysisOperations<'_> {
        AIAnalysisOperations::new(self)
    }

    /// Get billing operations
    pub fn billing(&self) -> BillingOperations<'_> {
        BillingOperations::new(self)
    }

    /// Get report operations
    pub fn reports(&self) -> ReportOperations<'_> {
        ReportOperations::new(self)
    }

    /// Get device operations (CLI tools and scanners)
    pub fn device(&self) -> DeviceOperations<'_> {
        DeviceOperations::new(self)
    }

    /// Get scanner operations (rule/plugin discovery, heartbeats)
    pub fn scanner(&self) -> ScannerOperations<'_> {
        ScannerOperations::new(self)
    }

    /// Get code submission operations (file/repo/code analysis)
    pub fn code_submission(&self) -> CodeSubmissionOperations<'_> {
        CodeSubmissionOperations::new(self)
    }

    /// Get WebSocket operations for real-time communication
    pub fn websocket(&self) -> WebSocketOperations<'_> {
        WebSocketOperations::new(self)
    }

    /// Health check - verify API connectivity
    pub async fn health_check(&self) -> Result<HealthResponse> {
        let url = format!("{}/", self.base_url);
        let response = self
            .authenticated_request(reqwest::Method::GET, &url)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        let result = response.json().await?;
        Ok(result)
    }
}

/// Result of a security scan
#[derive(Deserialize, Debug, Clone)]
pub struct ScanResult {
    pub success: bool,
    pub vulnerabilities: Vec<Vulnerability>,
    pub total_issues: u32,
    pub scan_id: String,
}

/// Security vulnerability information
#[derive(Deserialize, Debug, Clone)]
pub struct Vulnerability {
    pub id: String,
    pub title: String,
    pub description: String,
    pub severity: String,
    pub category: String,
    pub location: Location,
}

/// Location of a vulnerability in code
#[derive(Deserialize, Debug, Clone)]
pub struct Location {
    pub file: String,
    pub line: u32,
    pub column: u32,
}

/// Result of AI model analysis
#[derive(Deserialize, Debug, Clone)]
pub struct ModelAnalysisResult {
    pub safe: bool,
    pub risks: Vec<String>,
    pub recommendations: HashMap<String, serde_json::Value>,
}

/// Health check response
#[derive(Deserialize, Debug, Clone)]
pub struct HealthResponse {
    pub message: String,
    pub version: String,
    pub status: String,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_client_creation() {
        let client = TavoClient::new("test-key");
        assert!(client.is_ok());
    }

    #[test]
    fn test_invalid_api_key() {
        let client = TavoClient::new("");
        assert!(matches!(client, Err(TavoError::InvalidApiKey)));
    }
}
