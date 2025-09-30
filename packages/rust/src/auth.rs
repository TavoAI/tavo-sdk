//! Authentication operations

use crate::{Result, TavoClient, TavoError};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Authentication operations for the Tavo AI API
pub struct AuthOperations<'a> {
    client: &'a TavoClient,
}

impl<'a> AuthOperations<'a> {
    /// Create a new AuthOperations instance
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Login with email and password
    pub async fn login(&self, email: &str, password: &str) -> Result<AuthResponse> {
        let data = HashMap::from([
            (
                "email".to_string(),
                serde_json::Value::String(email.to_string()),
            ),
            (
                "password".to_string(),
                serde_json::Value::String(password.to_string()),
            ),
        ]);
        self.client.post("/auth/login", &data).await
    }

    /// Register a new user
    pub async fn register(
        &self,
        user_data: HashMap<String, serde_json::Value>,
    ) -> Result<AuthResponse> {
        self.client.post("/auth/register", &user_data).await
    }

    /// Refresh authentication token
    pub async fn refresh_token(&self, refresh_token: &str) -> Result<AuthResponse> {
        let data = HashMap::from([(
            "refresh_token".to_string(),
            serde_json::Value::String(refresh_token.to_string()),
        )]);
        self.client.post("/auth/refresh", &data).await
    }

    /// Logout current session
    pub async fn logout(&self) -> Result<()> {
        self.client.post("/auth/logout", &HashMap::new()).await
    }

    /// Request password reset
    pub async fn request_password_reset(&self, email: &str) -> Result<()> {
        let data = HashMap::from([(
            "email".to_string(),
            serde_json::Value::String(email.to_string()),
        )]);
        self.client.post("/auth/password-reset", &data).await
    }

    /// Reset password with token
    pub async fn reset_password(&self, token: &str, new_password: &str) -> Result<()> {
        let data = HashMap::from([
            (
                "token".to_string(),
                serde_json::Value::String(token.to_string()),
            ),
            (
                "new_password".to_string(),
                serde_json::Value::String(new_password.to_string()),
            ),
        ]);
        self.client
            .post("/auth/password-reset/confirm", &data)
            .await
    }

    /// Verify email with token
    pub async fn verify_email(&self, token: &str) -> Result<()> {
        let data = HashMap::from([(
            "token".to_string(),
            serde_json::Value::String(token.to_string()),
        )]);
        self.client.post("/auth/verify-email", &data).await
    }

    /// Get current session info
    pub async fn get_session(&self) -> Result<SessionInfo> {
        self.client.get("/auth/session").await
    }
}

/// Authentication response
#[derive(Deserialize, Debug, Clone)]
pub struct AuthResponse {
    pub user: AuthUser,
    pub access_token: String,
    pub refresh_token: Option<String>,
    pub token_type: String,
    pub expires_in: u64,
}

/// Session information
#[derive(Deserialize, Debug, Clone)]
pub struct SessionInfo {
    pub user: AuthUser,
    pub session_id: String,
    pub created_at: String,
    pub expires_at: String,
    pub ip_address: Option<String>,
    pub user_agent: Option<String>,
}

/// User information for auth
#[derive(Deserialize, Debug, Clone)]
pub struct AuthUser {
    pub id: String,
    pub email: String,
    pub name: Option<String>,
    pub email_verified: bool,
    pub created_at: String,
}
