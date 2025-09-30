//! Billing operations

use crate::{Result, TavoClient, TavoError};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Billing operations for the Tavo AI API
pub struct BillingOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> BillingOperations<'a> {
    /// Create a new BillingOperations instance
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Get current billing plan
    pub async fn get_current_plan(&self) -> Result<BillingPlan> {
        self.client.get("/billing/plan").await
    }

    /// Get billing usage
    pub async fn get_usage(&self, period: Option<&str>) -> Result<BillingUsage> {
        let url = match period {
            Some(p) => format!("/billing/usage?period={}", p),
            None => "/billing/usage".to_string(),
        };
        self.client.get(&url).await
    }

    /// Get billing history
    pub async fn get_history(&self) -> Result<Vec<BillingInvoice>> {
        self.client.get("/billing/history").await
    }

    /// Update billing plan
    pub async fn update_plan(&self, plan_id: &str) -> Result<BillingPlan> {
        let data = HashMap::from([(
            "plan_id".to_string(),
            serde_json::Value::String(plan_id.to_string()),
        )]);
        self.client.put("/billing/plan", &data).await
    }

    /// Add payment method
    pub async fn add_payment_method(
        &self,
        payment_data: HashMap<String, serde_json::Value>,
    ) -> Result<PaymentMethod> {
        self.client
            .post("/billing/payment-methods", &payment_data)
            .await
    }

    /// List payment methods
    pub async fn list_payment_methods(&self) -> Result<Vec<PaymentMethod>> {
        self.client.get("/billing/payment-methods").await
    }

    /// Delete payment method
    pub async fn delete_payment_method(&self, payment_method_id: &str) -> Result<()> {
        let url = format!("/billing/payment-methods/{}", payment_method_id);
        self.client.delete(&url).await
    }
}

/// Billing plan information
#[derive(Deserialize, Debug, Clone)]
pub struct BillingPlan {
    pub id: String,
    pub name: String,
    pub price: f64,
    pub currency: String,
    pub interval: String,
    pub features: Vec<String>,
    pub limits: HashMap<String, serde_json::Value>,
}

/// Billing usage information
#[derive(Deserialize, Debug, Clone)]
pub struct BillingUsage {
    pub period: String,
    pub scans_used: u32,
    pub scans_limit: u32,
    pub api_calls_used: u32,
    pub api_calls_limit: u32,
    pub storage_used_gb: f64,
    pub storage_limit_gb: f64,
}

/// Billing invoice information
#[derive(Deserialize, Debug, Clone)]
pub struct BillingInvoice {
    pub id: String,
    pub amount: f64,
    pub currency: String,
    pub status: String,
    pub invoice_date: String,
    pub due_date: Option<String>,
    pub paid_at: Option<String>,
    pub invoice_url: Option<String>,
}

/// Payment method information
#[derive(Deserialize, Debug, Clone)]
pub struct PaymentMethod {
    pub id: String,
    pub type_: String,
    pub last4: String,
    pub brand: Option<String>,
    pub expiry_month: Option<u32>,
    pub expiry_year: Option<u32>,
    pub is_default: bool,
}
