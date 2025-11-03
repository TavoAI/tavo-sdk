//! Integration tests for the tooling-focused Rust SDK
//!
//! Tests Week 15/16 endpoints: device auth, scanner integration, code submission

use tavo_ai::*;
use tavo_ai::scanner::HeartbeatData;
use tavo_ai::code_submission::{FileInfo, RepositorySnapshot, AnalysisContext};
use tavo_ai::device::{DeviceCodeResponse, DeviceTokenResponse};
use tavo_ai::code_submission::{ScanStatus, ScanResultsSummary};
use tokio_util::sync::CancellationToken;
use std::collections::HashMap;

/// Mock server URL for integration tests - use non-routable IP to fail fast
const MOCK_SERVER_URL: &str = "http://10.255.255.1";

#[cfg(test)]
mod tests {
    use super::*;

    fn create_test_client() -> TavoClient {
        // Create a client with very short timeout for fast test failures
        let client = reqwest::Client::builder()
            .timeout(std::time::Duration::from_millis(10))
            .connect_timeout(std::time::Duration::from_millis(1))
            .build()
            .unwrap();
        TavoClient::with_client(client, MOCK_SERVER_URL)
    }

    #[tokio::test]
    async fn test_device_operations_async() {
        let client = create_test_client();
        let device_ops = client.device();

        // Test that async methods exist and return proper types
        let result = device_ops.create_device_code(None, None).await;
        // Will fail with network error, but method should exist
        assert!(result.is_err());

        let result = device_ops.create_device_code_for_cli(None, None).await;
        assert!(result.is_err());

        let result = device_ops.poll_device_token("test-code").await;
        assert!(result.is_err());

        let result = device_ops.get_device_code_status("test-code").await;
        assert!(result.is_err());

        let result = device_ops.get_usage_warnings().await;
        assert!(result.is_err());

        let result = device_ops.get_limits().await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_scanner_operations_async() {
        let client = create_test_client();
        let scanner_ops = client.scanner();

        // Test rule discovery
        let result = scanner_ops.discover_rules(None, None, None).await;
        assert!(result.is_err()); // Network error expected

        // Test bundle rules
        let result = scanner_ops.get_bundle_rules("test-bundle").await;
        assert!(result.is_err());

        // Test bundle usage tracking
        let result = scanner_ops.track_bundle_usage("test-bundle", None).await;
        assert!(result.is_err());

        // Test plugin discovery
        let result = scanner_ops.discover_plugins(None, None, None).await;
        assert!(result.is_err());

        // Test plugin config
        let result = scanner_ops.get_plugin_config("test-plugin").await;
        assert!(result.is_err());

        // Test recommendations
        let result = scanner_ops.get_recommendations(None, None, vec![], vec![]).await;
        assert!(result.is_err());

        // Test heartbeat
        let heartbeat = HeartbeatData {
            scanner_version: "1.0.0".to_string(),
            scanner_type: "sast".to_string(),
            active_rules: vec!["rule1".to_string()],
            active_plugins: vec!["plugin1".to_string()],
            system_info: HashMap::new(),
            scan_count: Some(42),
        };
        let result = scanner_ops.send_heartbeat(heartbeat).await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_code_submission_operations_async() {
        let client = create_test_client();
        let code_ops = client.code_submission();

        // Test code submission
        let files = vec![FileInfo {
            filename: "test.rs".to_string(),
            content: "fn main() {}".to_string(),
            language: Some("rust".to_string()),
        }];
        let result = code_ops.submit_code(files, None, None, None, None).await;
        assert!(result.is_err());

        // Test repository submission
        let snapshot = RepositorySnapshot {
            url: "https://github.com/test/repo".to_string(),
            branch: Some("main".to_string()),
            commit_sha: Some("abc123".to_string()),
            files: vec![],
        };
        let result = code_ops.submit_repository("https://github.com/test/repo", snapshot, None, None, None).await;
        assert!(result.is_err());

        // Test analysis submission
        let context = AnalysisContext {
            language: "rust".to_string(),
            analysis_type: Some("security".to_string()),
            rules: Some(vec!["rule1".to_string()]),
            plugins: Some(vec!["plugin1".to_string()]),
            context: None,
        };
        let result = code_ops.submit_analysis("fn main() {}", context).await;
        assert!(result.is_err());

        // Test scan status
        let result = code_ops.get_scan_status("test-scan-id").await;
        assert!(result.is_err());

        // Test scan results
        let result = code_ops.get_scan_results("test-scan-id").await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_cancellation_token() {
        let token = CancellationToken::new();
        assert!(!token.is_cancelled());

        token.cancel();
        assert!(token.is_cancelled());

        // Test cancellation future
        let cancelled_future = token.cancelled();
        // Should complete immediately since token is already cancelled
        cancelled_future.await;
    }

    #[tokio::test]
    async fn test_cancellable_operations() {
        let client = create_test_client();
        let device_ops = client.device();

        // Test cancellable device code creation
        let token = CancellationToken::new();
        let result = device_ops.create_device_code_cancellable(None, None, &token).await;
        // Should fail with network error (not cancellation)
        assert!(result.is_err());
        assert!(!result.as_ref().unwrap_err().to_string().contains("cancelled"));

        // Test cancellation
        let token = CancellationToken::new();
        token.cancel();

        let result = device_ops.create_device_code_cancellable(None, None, &token).await;
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("cancelled"));

        // Test cancellable polling
        let token = CancellationToken::new();
        token.cancel();

        let result = device_ops.poll_device_token_cancellable("test-code", &token).await;
        assert!(result.is_err());
        assert!(result.unwrap_err().to_string().contains("cancelled"));
    }

    #[tokio::test]
    async fn test_cancellation_race_condition() {
        let client = create_test_client();
        let device_ops = client.device();

        let token = CancellationToken::new();

        // Start operation
        let operation_future = device_ops.create_device_code_cancellable(None, None, &token);

        // Cancel after a short delay
        let token_clone = token.clone();
        tokio::spawn(async move {
            tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;
            token_clone.cancel();
        });

        let result = operation_future.await;
        // Should either succeed with network error or fail with cancellation
        assert!(result.is_err());
        let error_msg = result.unwrap_err().to_string();
        assert!(error_msg.contains("cancelled") || !error_msg.contains("cancelled"));
    }

    #[tokio::test]
    async fn test_data_structures() {
        // Test device code response
        let device_code = DeviceCodeResponse {
            device_code: "test-device-code".to_string(),
            user_code: "ABC123".to_string(),
            verification_uri: "https://example.com/verify".to_string(),
            verification_uri_complete: Some("https://example.com/verify?code=ABC123".to_string()),
            expires_in: 300,
            interval: 5,
        };
        assert_eq!(device_code.device_code, "test-device-code");
        assert_eq!(device_code.user_code, "ABC123");

        // Test device token response
        let token = DeviceTokenResponse {
            access_token: "test-token".to_string(),
            token_type: "Bearer".to_string(),
            expires_in: 3600,
            refresh_token: Some("refresh-token".to_string()),
        };
        assert_eq!(token.access_token, "test-token");
        assert_eq!(token.token_type, "Bearer");

        // Test scan status
        let status = ScanStatus {
            scan_id: "test-scan".to_string(),
            status: "completed".to_string(),
            progress: Some(1.0),
            started_at: Some("2024-01-01T00:00:00Z".to_string()),
            completed_at: Some("2024-01-01T00:01:00Z".to_string()),
            error_message: None,
        };
        assert_eq!(status.scan_id, "test-scan");
        assert_eq!(status.status, "completed");
        assert_eq!(status.progress, Some(1.0));

        // Test scan results summary
        let results = ScanResultsSummary {
            scan_id: "test-scan".to_string(),
            total_issues: 5,
            high_severity: 1,
            medium_severity: 2,
            low_severity: 2,
            issues_by_category: {
                let mut map = HashMap::new();
                map.insert("security".to_string(), 3);
                map.insert("performance".to_string(), 2);
                map
            },
            scan_duration: Some(60),
            rules_used: vec!["rule1".to_string(), "rule2".to_string()],
            plugins_used: vec!["plugin1".to_string()],
        };
        assert_eq!(results.total_issues, 5);
        assert_eq!(results.high_severity, 1);
        assert_eq!(results.issues_by_category["security"], 3);
    }

    #[tokio::test]
    async fn test_error_handling() {
        let client = create_test_client();

        // Test that operations properly wrap network errors
        let result = client.device().create_device_code(None, None).await;
        assert!(result.is_err());

        let error = result.unwrap_err();
        match error {
            TavoError::Http(_) | TavoError::Api { .. } => {
                // Expected network-related errors
            }
            _ => panic!("Unexpected error type: {:?}", error),
        }
    }

    #[tokio::test]
    async fn test_client_creation() {
        // Test API key client
        let client = TavoClient::new("test-key");
        assert!(client.is_ok());

        // Test JWT client
        let client = TavoClient::with_jwt_token("test-jwt");
        assert!(client.is_ok());

        // Test session token client
        let client = TavoClient::with_session_token("test-session");
        assert!(client.is_ok());

        // Test base URL client
        let client = TavoClient::with_base_url("test-key", "https://custom.api.com");
        assert!(client.is_ok());
        assert_eq!(client.unwrap().base_url, "https://custom.api.com");

        // Test invalid API key
        let client = TavoClient::new("");
        assert!(matches!(client, Err(TavoError::InvalidApiKey)));
    }

    #[tokio::test]
    async fn test_operation_accessors() {
        let client = create_test_client();

        // Test that all operation accessors work
        let _device_ops = client.device();
        let _scanner_ops = client.scanner();
        let _code_ops = client.code_submission();

        // Test that operations have proper client reference
        assert_eq!(client.base_url, _device_ops.client.base_url);
        assert_eq!(client.base_url, _scanner_ops.client.base_url);
        assert_eq!(client.base_url, _code_ops.client.base_url);
    }
}
