//! Code submission operations for CLI tools and scanners.
//!
//! Provides direct code submission, repository analysis, and scan result
//! retrieval optimized for automated tools and CLI applications.

use crate::{TavoClient, TavoError, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Code submission response
#[derive(Deserialize, Debug, Clone)]
pub struct CodeSubmissionResponse {
    pub scan_id: String,
    pub status: String,
    pub submitted_at: String,
    pub estimated_completion: Option<String>,
}

/// Repository submission response
#[derive(Deserialize, Debug, Clone)]
pub struct RepositorySubmissionResponse {
    pub scan_id: String,
    pub repository_url: String,
    pub status: String,
    pub submitted_at: String,
    pub snapshot_id: Option<String>,
}

/// Analysis submission response
#[derive(Deserialize, Debug, Clone)]
pub struct AnalysisSubmissionResponse {
    pub analysis_id: String,
    pub status: String,
    pub submitted_at: String,
    pub language: String,
}

/// Scan status information
#[derive(Deserialize, Debug, Clone)]
pub struct ScanStatus {
    pub scan_id: String,
    pub status: String,
    pub progress: Option<f64>,
    pub started_at: Option<String>,
    pub completed_at: Option<String>,
    pub error_message: Option<String>,
}

/// Scan results summary (CLI-optimized)
#[derive(Deserialize, Debug, Clone)]
pub struct ScanResultsSummary {
    pub scan_id: String,
    pub total_issues: u32,
    pub high_severity: u32,
    pub medium_severity: u32,
    pub low_severity: u32,
    pub issues_by_category: HashMap<String, u32>,
    pub scan_duration: Option<u64>,
    pub rules_used: Vec<String>,
    pub plugins_used: Vec<String>,
}

/// File information for code submission
#[derive(Serialize, Debug, Clone)]
pub struct FileInfo {
    pub filename: String,
    pub content: String,
    pub language: Option<String>,
}

/// Repository snapshot data
#[derive(Serialize, Debug, Clone)]
pub struct RepositorySnapshot {
    pub url: String,
    pub branch: Option<String>,
    pub commit_sha: Option<String>,
    pub files: Vec<FileInfo>,
}

/// Analysis context
#[derive(Serialize, Debug, Clone)]
pub struct AnalysisContext {
    pub language: String,
    pub analysis_type: Option<String>,
    pub rules: Option<Vec<String>>,
    pub plugins: Option<Vec<String>>,
    pub context: Option<HashMap<String, serde_json::Value>>,
}

/// Code submission operations for CLI tools and scanners
pub struct CodeSubmissionOperations<'a> {
    pub client: &'a TavoClient,
}

impl<'a> CodeSubmissionOperations<'a> {
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Submit code files directly for scanning
    ///
    /// # Arguments
    ///
    /// * `files` - List of file information to submit
    /// * `repository_name` - Optional repository name
    /// * `branch` - Optional branch name
    /// * `commit_sha` - Optional commit SHA
    /// * `scan_config` - Optional scan configuration
    ///
    pub async fn submit_code(
        &self,
        files: Vec<FileInfo>,
        repository_name: Option<&str>,
        branch: Option<&str>,
        commit_sha: Option<&str>,
        scan_config: Option<HashMap<String, serde_json::Value>>,
    ) -> Result<CodeSubmissionResponse> {
        let mut data = HashMap::new();

        // Add files
        let files_json: Vec<HashMap<String, serde_json::Value>> = files
            .into_iter()
            .map(|file| {
                let mut file_map = HashMap::new();
                file_map.insert("filename".to_string(), serde_json::Value::String(file.filename));
                file_map.insert("content".to_string(), serde_json::Value::String(file.content));
                if let Some(language) = file.language {
                    file_map.insert("language".to_string(), serde_json::Value::String(language));
                }
                file_map
            })
            .collect();
        data.insert("files".to_string(), serde_json::Value::Array(
            files_json.into_iter().map(|h| serde_json::Value::Object(h.into_iter().collect())).collect()
        ));

        // Add optional parameters
        if let Some(repository_name) = repository_name {
            data.insert("repository_name".to_string(), serde_json::Value::String(repository_name.to_string()));
        }
        if let Some(branch) = branch {
            data.insert("branch".to_string(), serde_json::Value::String(branch.to_string()));
        }
        if let Some(commit_sha) = commit_sha {
            data.insert("commit_sha".to_string(), serde_json::Value::String(commit_sha.to_string()));
        }
        if let Some(scan_config) = scan_config {
            data.insert("scan_config".to_string(), serde_json::Value::Object(scan_config.into_iter().collect()));
        }

        self.client.post("/code/submit", &data).await
    }

    /// Submit repository for scanning
    ///
    /// # Arguments
    ///
    /// * `repository_url` - Repository URL or identifier
    /// * `snapshot` - Repository snapshot data
    /// * `branch` - Optional branch name
    /// * `commit_sha` - Optional commit SHA
    /// * `scan_config` - Optional scan configuration
    ///
    pub async fn submit_repository(
        &self,
        repository_url: &str,
        snapshot: RepositorySnapshot,
        branch: Option<&str>,
        commit_sha: Option<&str>,
        scan_config: Option<HashMap<String, serde_json::Value>>,
    ) -> Result<RepositorySubmissionResponse> {
        let mut data = HashMap::new();

        // Add repository URL
        data.insert("repository_url".to_string(), serde_json::Value::String(repository_url.to_string()));

        // Add snapshot data
        let mut snapshot_data = HashMap::new();
        snapshot_data.insert("url".to_string(), serde_json::Value::String(snapshot.url));
        if let Some(branch) = snapshot.branch {
            snapshot_data.insert("branch".to_string(), serde_json::Value::String(branch));
        }
        if let Some(commit_sha) = snapshot.commit_sha {
            snapshot_data.insert("commit_sha".to_string(), serde_json::Value::String(commit_sha));
        }

        let files_json: Vec<HashMap<String, serde_json::Value>> = snapshot.files
            .into_iter()
            .map(|file| {
                let mut file_map = HashMap::new();
                file_map.insert("filename".to_string(), serde_json::Value::String(file.filename));
                file_map.insert("content".to_string(), serde_json::Value::String(file.content));
                if let Some(language) = file.language {
                    file_map.insert("language".to_string(), serde_json::Value::String(language));
                }
                file_map
            })
            .collect();
        snapshot_data.insert("files".to_string(), serde_json::Value::Array(
            files_json.into_iter().map(|h| serde_json::Value::Object(h.into_iter().collect())).collect()
        ));

        data.insert("snapshot_data".to_string(), serde_json::Value::Object(snapshot_data.into_iter().collect()));

        // Add optional parameters
        if let Some(branch) = branch {
            data.insert("branch".to_string(), serde_json::Value::String(branch.to_string()));
        }
        if let Some(commit_sha) = commit_sha {
            data.insert("commit_sha".to_string(), serde_json::Value::String(commit_sha.to_string()));
        }
        if let Some(scan_config) = scan_config {
            data.insert("scan_config".to_string(), serde_json::Value::Object(scan_config.into_iter().collect()));
        }

        self.client.post("/code/submit/repository", &data).await
    }

    /// Submit code for targeted analysis
    ///
    /// # Arguments
    ///
    /// * `code_content` - The code content to analyze
    /// * `analysis_context` - Analysis context including language, rules, plugins
    ///
    pub async fn submit_analysis(
        &self,
        code_content: &str,
        analysis_context: AnalysisContext,
    ) -> Result<AnalysisSubmissionResponse> {
        let mut data = HashMap::new();

        // Add code content
        data.insert("code_content".to_string(), serde_json::Value::String(code_content.to_string()));

        // Add analysis context
        data.insert("language".to_string(), serde_json::Value::String(analysis_context.language));
        if let Some(analysis_type) = analysis_context.analysis_type {
            data.insert("analysis_type".to_string(), serde_json::Value::String(analysis_type));
        }
        if let Some(rules) = analysis_context.rules {
            data.insert("rules".to_string(), serde_json::Value::Array(
                rules.into_iter().map(serde_json::Value::String).collect()
            ));
        }
        if let Some(plugins) = analysis_context.plugins {
            data.insert("plugins".to_string(), serde_json::Value::Array(
                plugins.into_iter().map(serde_json::Value::String).collect()
            ));
        }
        if let Some(context) = analysis_context.context {
            data.insert("context".to_string(), serde_json::Value::Object(context.into_iter().collect()));
        }

        self.client.post("/code/analyze", &data).await
    }

    /// Get scan status (CLI-optimized)
    ///
    /// # Arguments
    ///
    /// * `scan_id` - The scan ID to check status for
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let status = client.code_submission().get_scan_status("scan-123").await?;
    ///
    /// match status.status.as_str() {
    ///     "pending" => println!("Scan is queued..."),
    ///     "running" => println!("Scan in progress: {:.1}%", status.progress.unwrap_or(0.0)),
    ///     "completed" => println!("Scan completed!"),
    ///     "failed" => println!("Scan failed: {:?}", status.error_message),
    ///     _ => println!("Unknown status: {}", status.status),
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub async fn get_scan_status(&self, scan_id: &str) -> Result<ScanStatus> {
        self.client.get(&format!("/code/scans/{}/status", scan_id)).await
    }

    /// Get scan results summary (CLI-optimized)
    ///
    /// # Arguments
    ///
    /// * `scan_id` - The scan ID to get results for
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let results = client.code_submission().get_scan_results("scan-123").await?;
    ///
    /// println!("Scan Results Summary:");
    /// println!("Total issues: {}", results.total_issues);
    /// println!("High severity: {}", results.high_severity);
    /// println!("Medium severity: {}", results.medium_severity);
    /// println!("Low severity: {}", results.low_severity);
    ///
    /// println!("Issues by category:");
    /// for (category, count) in &results.issues_by_category {
    ///     println!("  {}: {}", category, count);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub async fn get_scan_results(&self, scan_id: &str) -> Result<ScanResultsSummary> {
        self.client.get(&format!("/code/scans/{}/results/summary", scan_id)).await
    }
}
