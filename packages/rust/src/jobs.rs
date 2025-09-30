//! Job operations

use crate::{Result, TavoClient, TavoError};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Job operations for the Tavo AI API
pub struct JobOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> JobOperations<'a> {
    /// Create a new JobOperations instance
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Submit a new job
    pub async fn submit(&self, job_config: HashMap<String, serde_json::Value>) -> Result<Job> {
        self.client.post("/jobs", &job_config).await
    }

    /// Get job status
    pub async fn get(&self, job_id: &str) -> Result<Job> {
        let url = format!("/jobs/{}", job_id);
        self.client.get(&url).await
    }

    /// List jobs
    pub async fn list(
        &self,
        params: Option<HashMap<String, serde_json::Value>>,
    ) -> Result<Vec<Job>> {
        match params {
            Some(p) => self.client.get_with_params("/jobs", &p).await,
            None => self.client.get("/jobs").await,
        }
    }

    /// Cancel a job
    pub async fn cancel(&self, job_id: &str) -> Result<()> {
        let url = format!("/jobs/{}/cancel", job_id);
        self.client.post(&url, &HashMap::new()).await
    }

    /// Get job logs
    pub async fn get_logs(&self, job_id: &str) -> Result<String> {
        let url = format!("/jobs/{}/logs", job_id);
        self.client.get_text(&url).await
    }

    /// Delete a job
    pub async fn delete(&self, job_id: &str) -> Result<()> {
        let url = format!("/jobs/{}", job_id);
        self.client.delete(&url).await
    }
}

/// Job information
#[derive(Deserialize, Debug, Clone)]
pub struct Job {
    pub id: String,
    pub status: String,
    pub job_type: String,
    pub created_at: String,
    pub updated_at: String,
    pub started_at: Option<String>,
    pub completed_at: Option<String>,
    pub progress: Option<f32>,
    pub result: Option<serde_json::Value>,
}
