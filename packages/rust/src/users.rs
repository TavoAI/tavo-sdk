//! User management operations

use crate::{Result, TavoClient};
use serde::Deserialize;
use std::collections::HashMap;

/// User operations for the Tavo AI API
pub struct UserOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> UserOperations<'a> {
    /// Create a new UserOperations instance
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Get current user profile
    pub async fn get_current_user(&self) -> Result<User> {
        self.client.get("/users/me").await
    }

    /// Update current user profile
    pub async fn update_profile(
        &self,
        profile_data: HashMap<String, serde_json::Value>,
    ) -> Result<User> {
        self.client.put("/users/me", &profile_data).await
    }

    /// List current user's API keys
    pub async fn list_api_keys(&self) -> Result<Vec<ApiKey>> {
        self.client.get("/users/me/api-keys").await
    }

    /// Create a new API key
    pub async fn create_api_key(
        &self,
        name: &str,
        additional_data: Option<HashMap<String, serde_json::Value>>,
    ) -> Result<ApiKey> {
        let mut data = HashMap::new();
        data.insert(
            "name".to_string(),
            serde_json::Value::String(name.to_string()),
        );

        if let Some(additional) = additional_data {
            for (k, v) in additional {
                data.insert(k, v);
            }
        }

        self.client.post("/users/me/api-keys", &data).await
    }

    /// Update an API key
    pub async fn update_api_key(
        &self,
        api_key_id: &str,
        update_data: HashMap<String, serde_json::Value>,
    ) -> Result<ApiKey> {
        let url = format!("/users/me/api-keys/{}", api_key_id);
        self.client.put(&url, &update_data).await
    }

    /// Delete an API key
    pub async fn delete_api_key(&self, api_key_id: &str) -> Result<()> {
        let url = format!("/users/me/api-keys/{}", api_key_id);
        self.client.delete(&url).await
    }

    /// Rotate an API key (generate new secret)
    pub async fn rotate_api_key(
        &self,
        api_key_id: &str,
        additional_data: Option<HashMap<String, serde_json::Value>>,
    ) -> Result<ApiKey> {
        let url = format!("/users/me/api-keys/{}/rotate", api_key_id);
        match additional_data {
            Some(data) => self.client.post(&url, &data).await,
            None => self.client.post(&url, &HashMap::new()).await,
        }
    }
}

/// User profile information
#[derive(Deserialize, Debug, Clone)]
pub struct User {
    pub id: String,
    pub email: String,
    pub name: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

/// API key information
#[derive(Deserialize, Debug, Clone)]
pub struct ApiKey {
    pub id: String,
    pub name: String,
    pub key_preview: String,
    pub created_at: String,
    pub last_used_at: Option<String>,
    pub permissions: Vec<String>,
}
