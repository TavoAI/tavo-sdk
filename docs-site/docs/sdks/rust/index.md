# Rust SDK

The Tavo AI Rust SDK provides generated API clients for all platform endpoints plus integrated tavo-scanner execution capabilities. Built with Rust's memory safety and zero-cost abstractions.

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
tavo-sdk = "0.1"
```

## Architecture

The Rust SDK provides two main components:

### API Clients
Generated async clients for all Tavo AI REST API endpoints located in `packages/rust/src/endpoints/`:
- `DeviceAuthClient` - Device authentication operations
- `ScanToolsClient` - Core scanning functionality
- And 22+ additional endpoint clients

### Scanner Integration
Built-in tavo-scanner wrapper in `packages/rust/src/scanner.rs`:
- Tokio-based subprocess execution of tavo-scanner binary
- Plugin and rule configuration management
- Automatic binary discovery
- Async execution with proper error handling

## Quick Start

```rust
use tavo_sdk::{create_client_with_auth, create_scanner};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // API client usage
    let client = create_client_with_auth(
        Some("your-api-key".to_string()), 
        None, 
        None
    );
    let result = client.device_auth.post_code("123".to_string(), Some("test".to_string())).await?;

    // Scanner usage
    let scanner = create_scanner_with_plugins(vec!["security".to_string(), "performance".to_string()]);
    let scan_result = scanner.scan_directory("./my-project", None).await?;

    Ok(())
}
```

## Authentication

```rust
use tavo_sdk::*;

// API Key authentication (recommended)
let client = create_client_with_auth(Some("your-api-key".to_string()), None, None);

// JWT Token authentication
let client = create_client_with_auth(None, Some("your-jwt-token".to_string()), None);

// Device token authentication
let client = create_client_with_auth(None, None, Some("your-device-token".to_string()));
```

## API Client Usage

```rust
let client = create_client_with_auth(Some("your-api-key".to_string()), None, None);

// Authentication operations
let auth_result = client.device_auth.post_code("client_id".to_string(), Some("client_name".to_string())).await?;

// Scanning operations
let scan_result = client.scan_tools.get_scan("scan_id".to_string()).await?;
let bulk_result = client.scan_bulk_operations.create_bulk_scan(scan_configs).await?;

// AI Analysis
let analysis = client.ai_analysis.analyze_code("code".to_string(), "rust".to_string()).await?;

// Jobs management
let jobs = client.jobs.list_jobs().await?;
let job_status = client.jobs.get_job("job_id".to_string()).await?;

// Health checks
let health = client.health.health_check().await?;
```

## Scanner Integration

```rust
use tavo_sdk::*;

// Basic scanning
let scanner = create_scanner();
let result = scanner.scan_directory("./my-project", None).await?;

// Advanced scanning with plugins
let result = scanner.scan_with_plugins("./my-project", vec!["security".to_string(), "performance".to_string()]).await?;

// Custom rules and configuration
let result = scanner.scan_with_rules("./my-project", "./custom-rules.json").await?;
```

## Contributing & Support

- 📖 [API Reference](../../api-reference/overview.md)
- 🐛 [GitHub Issues](https://github.com/tavoai/tavo-sdk/issues)
