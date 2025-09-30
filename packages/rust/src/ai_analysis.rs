//! AI Analysis operations

use crate::{Result, TavoClient, TavoError};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// AI Analysis operations for the Tavo AI API
pub struct AIAnalysisOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> AIAnalysisOperations<'a> {
    /// Create a new AIAnalysisOperations instance
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Analyze AI model for security risks
    pub async fn analyze_model(
        &self,
        model_config: serde_json::Value,
    ) -> Result<ModelAnalysisResult> {
        let mut data = HashMap::new();
        data.insert("model_config".to_string(), model_config);
        self.client.post("/ai/analysis/model", &data).await
    }

    /// Analyze code with AI
    pub async fn analyze_code(
        &self,
        code: &str,
        language: &str,
        analysis_type: Option<&str>,
    ) -> Result<CodeAnalysisResult> {
        let mut data = HashMap::new();
        data.insert(
            "code".to_string(),
            serde_json::Value::String(code.to_string()),
        );
        data.insert(
            "language".to_string(),
            serde_json::Value::String(language.to_string()),
        );

        if let Some(analysis_type) = analysis_type {
            data.insert(
                "analysis_type".to_string(),
                serde_json::Value::String(analysis_type.to_string()),
            );
        }

        self.client.post("/ai/analysis/code", &data).await
    }

    /// Get AI analysis history
    pub async fn get_history(
        &self,
        params: Option<HashMap<String, serde_json::Value>>,
    ) -> Result<Vec<AIAnalysis>> {
        match params {
            Some(p) => {
                self.client
                    .get_with_params("/ai/analysis/history", &p)
                    .await
            }
            None => self.client.get("/ai/analysis/history").await,
        }
    }

    /// Get specific AI analysis
    pub async fn get(&self, analysis_id: &str) -> Result<AIAnalysis> {
        let url = format!("/ai/analysis/{}", analysis_id);
        self.client.get(&url).await
    }

    /// Delete AI analysis
    pub async fn delete(&self, analysis_id: &str) -> Result<()> {
        let url = format!("/ai/analysis/{}", analysis_id);
        self.client.delete(&url).await
    }
}

/// AI model analysis result
#[derive(Deserialize, Debug, Clone)]
pub struct ModelAnalysisResult {
    pub safe: bool,
    pub risks: Vec<String>,
    pub recommendations: HashMap<String, serde_json::Value>,
    pub confidence_score: f32,
}

/// Code analysis result
#[derive(Deserialize, Debug, Clone)]
pub struct CodeAnalysisResult {
    pub analysis_id: String,
    pub language: String,
    pub issues: Vec<CodeIssue>,
    pub suggestions: Vec<String>,
    pub complexity_score: Option<f32>,
    pub maintainability_index: Option<f32>,
}

/// Code issue found by AI analysis
#[derive(Deserialize, Debug, Clone)]
pub struct CodeIssue {
    pub id: String,
    pub title: String,
    pub description: String,
    pub severity: String,
    pub category: String,
    pub line: u32,
    pub column: u32,
    pub suggestion: Option<String>,
}

/// AI analysis information
#[derive(Deserialize, Debug, Clone)]
pub struct AIAnalysis {
    pub id: String,
    pub analysis_type: String,
    pub target: String,
    pub status: String,
    pub created_at: String,
    pub completed_at: Option<String>,
    pub result: Option<serde_json::Value>,
}
