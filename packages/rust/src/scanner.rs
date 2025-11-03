//! Scanner integration operations for CLI tools and scanners.
//!
//! Provides rule discovery, plugin management, and heartbeat functionality
//! for security scanners and automated analysis tools.

use crate::{TavoClient, TavoError, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Discovered rule information
#[derive(Deserialize, Debug, Clone)]
pub struct DiscoveredRule {
    pub id: String,
    pub name: String,
    pub description: String,
    pub category: String,
    pub language: Option<String>,
    pub severity: String,
    pub tags: Vec<String>,
}

/// Discovered plugin information
#[derive(Deserialize, Debug, Clone)]
pub struct DiscoveredPlugin {
    pub id: String,
    pub name: String,
    pub description: String,
    pub version: String,
    pub author: String,
    pub language: Option<String>,
    pub category: String,
    pub capabilities: Vec<String>,
}

/// Bundle rule information
#[derive(Deserialize, Debug, Clone)]
pub struct BundleRule {
    pub rule_id: String,
    pub bundle_id: String,
    pub enabled: bool,
    pub priority: Option<i32>,
}

/// Plugin configuration
#[derive(Deserialize, Debug, Clone)]
pub struct PluginConfig {
    pub plugin_id: String,
    pub config: HashMap<String, serde_json::Value>,
    pub enabled: bool,
}

/// Recommendations for rules and plugins
#[derive(Deserialize, Debug, Clone)]
pub struct Recommendations {
    pub suggested_rules: Vec<String>,
    pub suggested_plugins: Vec<String>,
    pub reasoning: HashMap<String, String>,
}

/// Heartbeat data for scanner tracking
#[derive(Serialize, Debug, Clone)]
pub struct HeartbeatData {
    pub scanner_version: String,
    pub scanner_type: String,
    pub active_rules: Vec<String>,
    pub active_plugins: Vec<String>,
    pub system_info: HashMap<String, serde_json::Value>,
    pub scan_count: Option<u64>,
}

/// Heartbeat response
#[derive(Deserialize, Debug, Clone)]
pub struct HeartbeatResponse {
    pub acknowledged: bool,
    pub server_version: String,
    pub recommendations: Option<Recommendations>,
}

/// Scanner operations for CLI tools and scanners
pub struct ScannerOperations<'a> {
    pub client: &'a TavoClient,
}

impl<'a> ScannerOperations<'a> {
    pub fn new(client: &'a TavoClient) -> Self {
        Self { client }
    }

    /// Discover rules optimized for scanner types
    ///
    /// # Arguments
    ///
    /// * `scanner_type` - Optional scanner type filter
    /// * `language` - Optional language filter
    /// * `category` - Optional category filter
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let rules = client.scanner().discover_rules(Some("sast"), Some("rust"), None).await?;
    /// for rule in rules {
    ///     println!("Found rule: {}", rule.name);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub async fn discover_rules(
        &self,
        scanner_type: Option<&str>,
        language: Option<&str>,
        category: Option<&str>,
    ) -> Result<Vec<DiscoveredRule>> {
        let mut params = HashMap::new();
        if let Some(scanner_type) = scanner_type {
            params.insert("scanner_type".to_string(), serde_json::Value::String(scanner_type.to_string()));
        }
        if let Some(language) = language {
            params.insert("language".to_string(), serde_json::Value::String(language.to_string()));
        }
        if let Some(category) = category {
            params.insert("category".to_string(), serde_json::Value::String(category.to_string()));
        }

        self.client.get_with_params("/scanner/rules", &params).await
    }

    /// Get rules for a specific bundle
    ///
    /// # Arguments
    ///
    /// * `bundle_id` - The bundle ID to get rules for
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let bundle_rules = client.scanner().get_bundle_rules("bundle-123").await?;
    /// for rule in bundle_rules {
    ///     if rule.enabled {
    ///         println!("Enabled rule: {}", rule.rule_id);
    ///     }
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub async fn get_bundle_rules(&self, bundle_id: &str) -> Result<Vec<BundleRule>> {
        self.client.get(&format!("/scanner/bundles/{}/rules", bundle_id)).await
    }

    /// Track bundle usage for analytics
    ///
    /// # Arguments
    ///
    /// * `bundle_id` - The bundle ID to track
    /// * `usage_data` - Optional usage data
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let mut usage_data = std::collections::HashMap::new();
    /// usage_data.insert("scan_count".to_string(), serde_json::Value::Number(42.into()));
    /// client.scanner().track_bundle_usage("bundle-123", Some(usage_data)).await?;
    /// # Ok(())
    /// # }
    /// ```
    pub async fn track_bundle_usage(
        &self,
        bundle_id: &str,
        usage_data: Option<HashMap<String, serde_json::Value>>,
    ) -> Result<HashMap<String, serde_json::Value>> {
        let mut data = HashMap::new();
        if let Some(usage_data) = usage_data {
            for (key, value) in usage_data {
                data.insert(key, value);
            }
        }

        self.client.post(&format!("/scanner/bundles/{}/usage", bundle_id), &data).await
    }

    /// Discover plugins for scanners
    ///
    /// # Arguments
    ///
    /// * `scanner_type` - Optional scanner type filter
    /// * `language` - Optional language filter
    /// * `category` - Optional category filter
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let plugins = client.scanner().discover_plugins(Some("sast"), Some("rust"), None).await?;
    /// for plugin in plugins {
    ///     println!("Found plugin: {} v{}", plugin.name, plugin.version);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub async fn discover_plugins(
        &self,
        scanner_type: Option<&str>,
        language: Option<&str>,
        category: Option<&str>,
    ) -> Result<Vec<DiscoveredPlugin>> {
        let mut params = HashMap::new();
        if let Some(scanner_type) = scanner_type {
            params.insert("scanner_type".to_string(), serde_json::Value::String(scanner_type.to_string()));
        }
        if let Some(language) = language {
            params.insert("language".to_string(), serde_json::Value::String(language.to_string()));
        }
        if let Some(category) = category {
            params.insert("category".to_string(), serde_json::Value::String(category.to_string()));
        }

        self.client.get_with_params("/scanner/plugins", &params).await
    }

    /// Get configuration for a specific plugin
    ///
    /// # Arguments
    ///
    /// * `plugin_id` - The plugin ID to get config for
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let config = client.scanner().get_plugin_config("plugin-123").await?;
    /// if config.enabled {
    ///     // Use plugin configuration
    ///     println!("Plugin config: {:?}", config.config);
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub async fn get_plugin_config(&self, plugin_id: &str) -> Result<PluginConfig> {
        self.client.get(&format!("/scanner/plugins/{}/config", plugin_id)).await
    }

    /// Get recommendations for rules and plugins
    ///
    /// # Arguments
    ///
    /// * `language` - Optional language context
    /// * `scanner_type` - Optional scanner type context
    /// * `current_rules` - Current rules being used
    /// * `current_plugins` - Current plugins being used
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::TavoClient;
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let recommendations = client.scanner()
    ///     .get_recommendations(Some("rust"), Some("sast"), vec!["rule1".to_string()], vec!["plugin1".to_string()])
    ///     .await?;
    /// println!("Suggested rules: {:?}", recommendations.suggested_rules);
    /// # Ok(())
    /// # }
    /// ```
    pub async fn get_recommendations(
        &self,
        language: Option<&str>,
        scanner_type: Option<&str>,
        current_rules: Vec<String>,
        current_plugins: Vec<String>,
    ) -> Result<Recommendations> {
        let mut data = HashMap::new();
        if let Some(language) = language {
            data.insert("language".to_string(), serde_json::Value::String(language.to_string()));
        }
        if let Some(scanner_type) = scanner_type {
            data.insert("scanner_type".to_string(), serde_json::Value::String(scanner_type.to_string()));
        }
        data.insert("current_rules".to_string(), serde_json::Value::Array(
            current_rules.into_iter().map(serde_json::Value::String).collect()
        ));
        data.insert("current_plugins".to_string(), serde_json::Value::Array(
            current_plugins.into_iter().map(serde_json::Value::String).collect()
        ));

        self.client.post("/scanner/recommendations", &data).await
    }

    /// Send scanner heartbeat for tracking and analytics
    ///
    /// # Arguments
    ///
    /// * `heartbeat_data` - Heartbeat data including version, active rules/plugins, system info
    ///
    /// # Example
    ///
    /// ```rust,no_run
    /// # use tavo_ai::{TavoClient, HeartbeatData};
    /// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
    /// let client = TavoClient::new("api-key")?;
    /// let mut system_info = std::collections::HashMap::new();
    /// system_info.insert("os".to_string(), serde_json::Value::String("linux".to_string()));
    /// system_info.insert("arch".to_string(), serde_json::Value::String("x86_64".to_string()));
    ///
    /// let heartbeat = HeartbeatData {
    ///     scanner_version: "1.0.0".to_string(),
    ///     scanner_type: "sast".to_string(),
    ///     active_rules: vec!["rule1".to_string(), "rule2".to_string()],
    ///     active_plugins: vec!["plugin1".to_string()],
    ///     system_info,
    ///     scan_count: Some(42),
    /// };
    ///
    /// let response = client.scanner().send_heartbeat(heartbeat).await?;
    /// if let Some(recommendations) = response.recommendations {
    ///     // Server has recommendations for this scanner
    /// }
    /// # Ok(())
    /// # }
    /// ```
    pub async fn send_heartbeat(&self, heartbeat_data: HeartbeatData) -> Result<HeartbeatResponse> {
        let mut data = HashMap::new();
        data.insert("scanner_version".to_string(), serde_json::Value::String(heartbeat_data.scanner_version));
        data.insert("scanner_type".to_string(), serde_json::Value::String(heartbeat_data.scanner_type));
        data.insert("active_rules".to_string(), serde_json::Value::Array(
            heartbeat_data.active_rules.into_iter().map(serde_json::Value::String).collect()
        ));
        data.insert("active_plugins".to_string(), serde_json::Value::Array(
            heartbeat_data.active_plugins.into_iter().map(serde_json::Value::String).collect()
        ));
        data.insert("system_info".to_string(), serde_json::Value::Object(
            heartbeat_data.system_info.into_iter().collect()
        ));
        if let Some(scan_count) = heartbeat_data.scan_count {
            data.insert("scan_count".to_string(), serde_json::Value::Number(scan_count.into()));
        }

        self.client.post("/scanner/heartbeat", &data).await
    }
}
