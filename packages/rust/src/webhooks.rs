//! Webhook operations

use crate::{Result, TavoClient, TavoError};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Webhook operations for the Tavo AI API
pub struct WebhookOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> WebhookOperations<'a> {
    /// Create a new WebhookOperations instance
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Create a webhook
    pub async fn create(
        &self,
        webhook_config: HashMap<String, serde_json::Value>,
    ) -> Result<Webhook> {
        self.client.post("/webhooks", &webhook_config).await
    }

    /// Get webhook details
    pub async fn get(&self, webhook_id: &str) -> Result<Webhook> {
        let url = format!("/webhooks/{}", webhook_id);
        self.client.get(&url).await
    }

    /// List webhooks
    pub async fn list(&self) -> Result<Vec<Webhook>> {
        self.client.get("/webhooks").await
    }

    /// Update a webhook
    pub async fn update(
        &self,
        webhook_id: &str,
        webhook_config: HashMap<String, serde_json::Value>,
    ) -> Result<Webhook> {
        let url = format!("/webhooks/{}", webhook_id);
        self.client.put(&url, &webhook_config).await
    }

    /// Delete a webhook
    pub async fn delete(&self, webhook_id: &str) -> Result<()> {
        let url = format!("/webhooks/{}", webhook_id);
        self.client.delete(&url).await
    }

    /// Test a webhook
    pub async fn test(&self, webhook_id: &str) -> Result<WebhookTestResult> {
        let url = format!("/webhooks/{}/test", webhook_id);
        self.client.post(&url, &HashMap::new()).await
    }

    /// Get webhook deliveries
    pub async fn get_deliveries(&self, webhook_id: &str) -> Result<Vec<WebhookDelivery>> {
        let url = format!("/webhooks/{}/deliveries", webhook_id);
        self.client.get(&url).await
    }
}

/// Webhook information
#[derive(Deserialize, Debug, Clone)]
pub struct Webhook {
    pub id: String,
    pub url: String,
    pub events: Vec<String>,
    pub secret: Option<String>,
    pub active: bool,
    pub created_at: String,
    pub updated_at: String,
}

/// Webhook test result
#[derive(Deserialize, Debug, Clone)]
pub struct WebhookTestResult {
    pub success: bool,
    pub status_code: Option<u16>,
    pub response_time_ms: Option<u64>,
    pub error_message: Option<String>,
}

/// Webhook delivery information
#[derive(Deserialize, Debug, Clone)]
pub struct WebhookDelivery {
    pub id: String,
    pub webhook_id: String,
    pub event: String,
    pub payload: serde_json::Value,
    pub status_code: Option<u16>,
    pub delivered_at: Option<String>,
    pub error_message: Option<String>,
}
