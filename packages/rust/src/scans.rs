//! Scan operations

use crate::{Result, TavoClient, ScanResult};
use serde::Deserialize;
use std::collections::HashMap;

/// Scan operations for the Tavo AI API
pub struct ScanOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> ScanOperations<'a> {
    /// Create a new ScanOperations instance
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Start a new scan
    pub async fn start(&self, scan_config: HashMap<String, serde_json::Value>) -> Result<Scan> {
        self.client.post("/scans", &scan_config).await
    }

    /// Scan code for security vulnerabilities
    ///
    /// # Arguments
    ///
    /// * `code` - The source code to scan
    /// * `language` - Programming language (optional, defaults to "rust")
    pub async fn start_scan(&self, code: &str, language: &str) -> Result<ScanResult> {
        let mut scan_config = HashMap::new();
        scan_config.insert(
            "code".to_string(),
            serde_json::Value::String(code.to_string()),
        );
        scan_config.insert(
            "language".to_string(),
            serde_json::Value::String(language.to_string()),
        );

        self.client.post("/scans/code", &scan_config).await
    }

    /// Scan code for security vulnerabilities (convenience method)
    ///
    /// # Arguments
    ///
    /// * `code` - The source code to scan
    /// * `language` - Programming language (optional, defaults to "rust")
    pub async fn scan_code(&self, code: &str, language: &str) -> Result<ScanResult> {
        let mut scan_config = HashMap::new();
        scan_config.insert(
            "code".to_string(),
            serde_json::Value::String(code.to_string()),
        );
        scan_config.insert(
            "language".to_string(),
            serde_json::Value::String(language.to_string()),
        );

        self.client.post("/scans/code", &scan_config).await
    }

    /// Get scan status
    pub async fn get(&self, scan_id: &str) -> Result<Scan> {
        let url = format!("/scans/{}", scan_id);
        self.client.get(&url).await
    }

    /// List scans
    pub async fn list(
        &self,
        params: Option<HashMap<String, serde_json::Value>>,
    ) -> Result<Vec<Scan>> {
        match params {
            Some(p) => self.client.get_with_params("/scans", &p).await,
            None => self.client.get("/scans").await,
        }
    }

    /// Cancel a scan
    pub async fn cancel(&self, scan_id: &str) -> Result<()> {
        let url = format!("/scans/{}/cancel", scan_id);
        self.client.post(&url, &HashMap::new()).await
    }

    /// Get scan results
    pub async fn get_results(&self, scan_id: &str) -> Result<ScanResults> {
        let url = format!("/scans/{}/results", scan_id);
        self.client.get(&url).await
    }

    /// Delete a scan
    pub async fn delete(&self, scan_id: &str) -> Result<()> {
        let url = format!("/scans/{}", scan_id);
        self.client.delete(&url).await
    }
}

/// Scan information
#[derive(Deserialize, Debug, Clone)]
pub struct Scan {
    pub id: String,
    pub status: String,
    pub created_at: String,
    pub updated_at: String,
    pub target: String,
    pub scan_type: String,
    pub total_issues: Option<u32>,
    pub progress: Option<f32>,
}

/// Scan results
#[derive(Deserialize, Debug, Clone)]
pub struct ScanResults {
    pub scan_id: String,
    pub vulnerabilities: Vec<Vulnerability>,
    pub total_issues: u32,
    pub high_severity: u32,
    pub medium_severity: u32,
    pub low_severity: u32,
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
    pub cwe_id: Option<String>,
    pub owasp_top_10: Option<String>,
}

/// Location of a vulnerability in code
#[derive(Deserialize, Debug, Clone)]
pub struct Location {
    pub file: String,
    pub line: u32,
    pub column: u32,
    pub snippet: Option<String>,
}
