//! Organization operations

use crate::{TavoClient, TavoError, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Organization operations for the Tavo AI API
pub struct OrganizationOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> OrganizationOperations<'a> {
    /// Create a new OrganizationOperations instance
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// List organizations
    pub async fn list(&self) -> Result<Vec<Organization>> {
        self.client.get("/organizations").await
    }

    /// Get organization details
    pub async fn get(&self, org_id: &str) -> Result<Organization> {
        let url = format!("/organizations/{}", org_id);
        self.client.get(&url).await
    }

    /// Create a new organization
    pub async fn create(&self, org_data: HashMap<String, serde_json::Value>) -> Result<Organization> {
        self.client.post("/organizations", &org_data).await
    }

    /// Update an organization
    pub async fn update(&self, org_id: &str, org_data: HashMap<String, serde_json::Value>) -> Result<Organization> {
        let url = format!("/organizations/{}", org_id);
        self.client.put(&url, &org_data).await
    }

    /// Delete an organization
    pub async fn delete(&self, org_id: &str) -> Result<()> {
        let url = format!("/organizations/{}", org_id);
        self.client.delete(&url).await
    }

    /// Get organization members
    pub async fn get_members(&self, org_id: &str) -> Result<Vec<OrganizationMember>> {
        let url = format!("/organizations/{}/members", org_id);
        self.client.get(&url).await
    }

    /// Add member to organization
    pub async fn add_member(&self, org_id: &str, user_id: &str, role: &str) -> Result<OrganizationMember> {
        let url = format!("/organizations/{}/members", org_id);
        let data = HashMap::from([
            ("user_id".to_string(), serde_json::Value::String(user_id.to_string())),
            ("role".to_string(), serde_json::Value::String(role.to_string())),
        ]);
        self.client.post(&url, &data).await
    }

    /// Remove member from organization
    pub async fn remove_member(&self, org_id: &str, user_id: &str) -> Result<()> {
        let url = format!("/organizations/{}/members/{}", org_id, user_id);
        self.client.delete(&url).await
    }
}

/// Organization information
#[derive(Deserialize, Debug, Clone)]
pub struct Organization {
    pub id: String,
    pub name: String,
    pub description: Option<String>,
    pub created_at: String,
    pub updated_at: String,
    pub owner_id: String,
}

/// Organization member information
#[derive(Deserialize, Debug, Clone)]
pub struct OrganizationMember {
    pub user_id: String,
    pub email: String,
    pub name: Option<String>,
    pub role: String,
    pub joined_at: String,
}