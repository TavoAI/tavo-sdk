//! Ai_Performance_Quality API Client

use reqwest::Client;
use serde_json::Value;
use std::sync::Arc;

pub struct AiPerformanceQualityClient {
    client: Arc<Client>,
    base_url: String,
}

impl AiPerformanceQualityClient {
    pub fn new(client: Arc<Client>) -> Self {
        Self {
            client,
            base_url: "https://api.tavo.ai/api/v1".to_string(),
        }
    }

{methods_str}
}}
