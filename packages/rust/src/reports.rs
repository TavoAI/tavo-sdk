//! Report operations

use crate::{Result, TavoClient, TavoError};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Report operations for the Tavo AI API
pub struct ReportOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> ReportOperations<'a> {
    /// Create a new ReportOperations instance
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Generate a new report
    pub async fn generate(&self, params: HashMap<String, serde_json::Value>) -> Result<Report> {
        self.client.post("/reports", &params).await
    }

    /// Get a specific report
    pub async fn get(&self, report_id: &str) -> Result<Report> {
        let url = format!("/reports/{}", report_id);
        self.client.get(&url).await
    }

    /// List all reports
    pub async fn list(
        &self,
        params: Option<HashMap<String, serde_json::Value>>,
    ) -> Result<Vec<Report>> {
        match params {
            Some(p) => self.client.get_with_params("/reports", &p).await,
            None => self.client.get("/reports").await,
        }
    }

    /// Delete a report
    pub async fn delete(&self, report_id: &str) -> Result<()> {
        let url = format!("/reports/{}", report_id);
        self.client.delete(&url).await
    }

    /// Download a report file
    pub async fn download(&self, report_id: &str) -> Result<Vec<u8>> {
        let url = format!("/reports/{}/download", report_id);
        self.client.get_bytes(&url).await
    }

    /// Get report summary statistics
    pub async fn get_summary(&self) -> Result<ReportSummary> {
        self.client.get("/reports/summary").await
    }
}

/// Report information
#[derive(Deserialize, Debug, Clone)]
pub struct Report {
    pub id: String,
    pub title: String,
    pub description: Option<String>,
    pub status: String,
    pub created_at: String,
    pub updated_at: String,
    pub scan_id: Option<String>,
    pub total_issues: u32,
    pub high_severity: u32,
    pub medium_severity: u32,
    pub low_severity: u32,
}

/// Report summary statistics
#[derive(Deserialize, Debug, Clone)]
pub struct ReportSummary {
    pub total_reports: u32,
    pub total_scans: u32,
    pub total_issues: u32,
    pub high_severity_issues: u32,
    pub medium_severity_issues: u32,
    pub low_severity_issues: u32,
    pub scans_by_language: HashMap<String, u32>,
    pub issues_by_category: HashMap<String, u32>,
}
