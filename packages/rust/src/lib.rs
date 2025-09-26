//! # Tavo AI Rust SDK
//!
//! The official Tavo AI SDK for Rust applications, providing comprehensive
//! security scanning and AI model analysis capabilities.
//!
//! ## Example
//!
//! ```rust,no_run
//! use tavo_ai::TavoClient;
//!
//! #[tokio::main]
//! async fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let client = TavoClient::new("your-api-key")?;
//!
//!     // Scan code for vulnerabilities
//!     let result = client.scan_code(r#"
//!         fn process_input(input: &str) {
//!             let query = format!("SELECT * FROM users WHERE id = '{}'", input);
//!             // Potential SQL injection vulnerability
//!         }
//!     "#, "rust").await?;
//!
//!     println!("Found {} issues", result.total_issues);
//!     Ok(())
//! }
//! ```

use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use thiserror::Error;

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
            base_url: "https://api.tavo.ai".to_string(),
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
            base_url: "https://api.tavo.ai".to_string(),
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
            base_url: "https://api.tavo.ai".to_string(),
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

    /// Scan code for security vulnerabilities
    ///
    /// # Arguments
    ///
    /// * `code` - The source code to scan
    /// * `language` - Programming language (optional, defaults to "rust")
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// use tavo_ai::TavoClient;
    ///
    /// #[tokio::main]
    /// async fn main() -> Result<(), Box<dyn std::error::Error>> {
    ///     let client = TavoClient::new("your-api-key")?;
    ///     let result = client.scan_code("fn main() {}", "rust").await?;
    ///     println!("Scan completed: {}", result.success);
    ///     Ok(())
    /// }
    /// ```
    pub async fn scan_code(&self, code: &str, language: &str) -> Result<ScanResult> {
        let request = ScanRequest {
            code: code.to_string(),
            language: language.to_string(),
        };

        let url = format!("{}/api/v1/scan", self.base_url);
        let response = self
            .authenticated_request(reqwest::Method::POST, &url)
            .json(&request)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        let result: ScanResult = response.json().await?;
        Ok(result)
    }

    /// Analyze AI model for security risks
    ///
    /// # Arguments
    ///
    /// * `model_config` - Model configuration as a JSON value
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # use serde_json::json;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("your-api-key")?;
    /// let config = json!({
    ///     "model_type": "transformer",
    ///     "parameters": {
    ///         "layers": 12,
    ///         "heads": 8
    ///     }
    /// });
    /// let result = client.analyze_model(config).await?;
    /// println!("Model is safe: {}", result.safe);
    /// # Ok(())
    /// # }
    /// ```
    pub async fn analyze_model(&self, model_config: serde_json::Value) -> Result<ModelAnalysisResult> {
        let url = format!("{}/api/v1/analyze/model", self.base_url);
        let response = self
            .authenticated_request(reqwest::Method::POST, &url)
            .json(&model_config)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_msg = response.text().await.unwrap_or_default();
            return Err(TavoError::Api { message: error_msg });
        }

        let result: ModelAnalysisResult = response.json().await?;
        Ok(result)
    }
}

/// Request payload for code scanning
#[derive(Serialize)]
struct ScanRequest {
    code: String,
    language: String,
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