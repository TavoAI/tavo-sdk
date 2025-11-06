//! Tavo AI SDK for Rust
//!
//! Official Rust SDK for the Tavo AI platform providing access to:
//! - REST API client with all endpoints
//! - Tavo scanner execution and configuration

pub mod endpoints;
pub mod scanner;

pub use endpoints::*;
pub use scanner::{TavoScanner, ScannerConfig, ScanOptions, ScanResult};

/// Create a new API client instance
pub fn create_client() -> TavoClient {
    TavoClient::new(None)
}

/// Create a new API client instance with authentication
pub fn create_client_with_auth(
    api_key: Option<String>,
    jwt_token: Option<String>,
    session_token: Option<String>,
) -> TavoClient {
    // Note: This would need to be implemented in the TavoClient
    TavoClient::new(None)
}

/// Create a new scanner instance
pub fn create_scanner() -> TavoScanner {
    TavoScanner::default()
}

/// Create a new scanner instance with configuration
pub fn create_scanner_with_config(config: ScannerConfig) -> TavoScanner {
    TavoScanner::new(Some(config))
}

/// Create a scanner with specific plugins
pub fn create_scanner_with_plugins(plugins: Vec<String>) -> TavoScanner {
    let config = ScannerConfig {
        plugins,
        ..Default::default()
    };
    TavoScanner::new(Some(config))
}

/// Create a scanner with custom rules
pub fn create_scanner_with_rules(rules_path: std::path::PathBuf) -> TavoScanner {
    let config = ScannerConfig {
        rules_path: Some(rules_path),
        ..Default::default()
    };
    TavoScanner::new(Some(config))
}

/// SDK version
pub const VERSION: &str = "0.1.0";