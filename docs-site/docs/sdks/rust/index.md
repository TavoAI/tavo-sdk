# Rust SDK

The Tavo AI Rust SDK provides a safe, async-first interface for integrating with the Tavo AI platform. Built with Rust's ownership system and zero-cost abstractions.

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
tavo-ai = "1.0"
```

## Quick Start

```rust
use tavo_ai::Client;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize the client
    let client = Client::new("your-api-key")?;

    // Scan code for vulnerabilities
    let code = r#"
        fn process_user_input(user_input: &str) {
            let query = format!("SELECT * FROM users WHERE id = '{}'", user_input);
            // Potential SQL injection vulnerability
            execute_query(&query);
        }
    "#;

    let result = client.scan_code(code, "rust").await?;

    println!("Found {} issues", result.total_issues);
    for vuln in &result.vulnerabilities {
        println!("- {}: {}", vuln.title, vuln.description);
    }

    Ok(())
}
```

## Client Configuration

```rust
use std::time::Duration;
use tavo_ai::{Client, ClientOptions};

// Basic client
let client = Client::new("your-api-key")?;

// With custom options
let client = Client::with_options(ClientOptions {
    api_key: "your-api-key".to_string(),
    base_url: "https://api-staging.tavoai.net".to_string(),
    timeout: Duration::from_secs(30),
    max_retries: 3,
    retry_delay: Duration::from_secs(1),
})?;
```

## Core Operations

### Code Scanning

```rust
// Basic code scan
let result = client.scan_code(code, "rust").await?;

// Advanced scan with options
use tavo_ai::ScanOptions;

let result = client.scan_code_with_options(ScanOptions {
    code: code.to_string(),
    language: "rust".to_string(),
    timeout: Some(Duration::from_secs(60)),
    include_metrics: true,
}).await?;
```

### AI Model Analysis

```rust
use std::collections::HashMap;

let mut model_config = HashMap::new();
model_config.insert("model_type".to_string(), serde_json::json!("transformer"));

let mut parameters = HashMap::new();
parameters.insert("layers".to_string(), serde_json::json!(12));
parameters.insert("heads".to_string(), serde_json::json!(8));
parameters.insert("hidden_size".to_string(), serde_json::json!(768));

model_config.insert("parameters".to_string(), serde_json::json!(parameters));

let analysis = client.analyze_model(model_config).await?;
println!("Model is safe: {}", analysis.safe);
```

### User Management

```rust
// Get current user
let user = client.get_current_user().await?;

// Update user profile
use std::collections::HashMap;

let mut updates = HashMap::new();
updates.insert("name".to_string(), serde_json::json!("New Name"));
updates.insert("email".to_string(), serde_json::json!("new@example.com"));

let updated_user = client.update_user(user.id, updates).await?;

// API Key Management
let api_keys = client.list_api_keys().await?;

// Update API key
let mut key_updates = HashMap::new();
key_updates.insert("name".to_string(), serde_json::json!("Updated API Key Name"));
key_updates.insert("description".to_string(), serde_json::json!("Updated description"));

let updated_key = client.update_api_key(api_key_id, key_updates).await?;

// Rotate API key (generates new secret)
let rotated_key = client.rotate_api_key(api_key_id).await?;

// Delete API key
client.delete_api_key(api_key_id).await?;
```

### Organization Management

```rust
// List organizations
let organizations = client.list_organizations().await?;

// Create new organization
let mut org_data = HashMap::new();
org_data.insert("name".to_string(), serde_json::json!("My Company"));
org_data.insert("description".to_string(), serde_json::json!("Security scanning service"));

let new_org = client.create_organization(org_data).await?;
```

### Scan Jobs

```rust
// Start a new scan job
let mut job_data = HashMap::new();
job_data.insert("target_url".to_string(), serde_json::json!("https://example.com"));
job_data.insert("scan_type".to_string(), serde_json::json!("full_scan"));

let job = client.create_scan_job(job_data).await?;

// Get job status
let status = client.get_scan_job(job.id).await?;

// List all jobs with pagination
use tavo_ai::ListOptions;

let jobs = client.list_scan_jobs(ListOptions {
    limit: Some(10),
    offset: Some(0),
}).await?;
```

### Webhooks

```rust
use tavo_ai::WebhookConfig;

// Create webhook
let webhook = client.create_webhook(WebhookConfig {
    url: "https://myapp.com/webhook".to_string(),
    events: vec!["scan.completed".to_string(), "vulnerability.found".to_string()],
}).await?;

// List webhooks
let webhooks = client.list_webhooks().await?;

// Delete webhook
client.delete_webhook(webhook.id).await?;
```

### Billing & Reports

```rust
// Get billing information
let billing = client.get_billing_info().await?;

// Generate report
use tavo_ai::{ReportConfig, DateRange};

let report = client.generate_report(ReportConfig {
    report_type: "security_audit".to_string(),
    date_range: Some(DateRange {
        start: "2024-01-01".to_string(),
        end: "2024-01-31".to_string(),
    }),
}).await?;

// Get report summary statistics
let summary = client.get_report_summary().await?;

println!("Total scans: {}", summary.total_scans);
println!("Total vulnerabilities: {}", summary.total_vulnerabilities);
println!("Critical issues: {}", summary.critical_issues);
```

## Error Handling

The SDK provides structured error types:

```rust
use tavo_ai::Error;

match client.scan_code(code, "rust").await {
    Ok(result) => {
        println!("Scan completed successfully");
    }
    Err(Error::Auth(e)) => {
        eprintln!("Authentication failed: {}", e.message);
    }
    Err(Error::Api(e)) => {
        eprintln!("API error: {} (status: {})", e.message, e.status_code);
    }
    Err(Error::RateLimit(e)) => {
        eprintln!("Rate limit exceeded, retry after: {:?}", e.retry_after);
    }
    Err(Error::Validation(e)) => {
        eprintln!("Validation error: {}", e.message);
        for (field, messages) in &e.field_errors {
            eprintln!("  {}: {:?}", field, messages);
        }
    }
    Err(Error::Network(e)) => {
        eprintln!("Network error: {}", e);
    }
    Err(e) => {
        eprintln!("Unknown error: {}", e);
    }
}
```

## Async and Concurrency

The SDK is built with async/await and supports tokio:

```rust
use tokio::time::{timeout, Duration};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new("your-api-key")?;

    // With timeout
    let result = timeout(
        Duration::from_secs(30),
        client.scan_code(code, "rust")
    ).await??;

    Ok(())
}
```

## Advanced Usage

### Concurrent Scanning

```rust
use futures::future::join_all;
use tokio::fs;

async fn scan_multiple_files(
    client: &Client,
    file_paths: Vec<String>
) -> Result<(), Box<dyn std::error::Error>> {
    let scan_futures = file_paths.into_iter().map(|path| {
        let client = client.clone();
        async move {
            let code = fs::read_to_string(&path).await?;
            let result = client.scan_code(&code, "rust").await?;
            Ok::<_, Box<dyn std::error::Error>>((path, result.total_issues))
        }
    });

    let results = join_all(scan_futures).await;

    for result in results {
        match result {
            Ok((path, issue_count)) => {
                println!("{}: {} issues found", path, issue_count);
            }
            Err(e) => {
                eprintln!("Error scanning file: {}", e);
            }
        }
    }

    Ok(())
}
```

### Streaming Results

```rust
use futures::stream::StreamExt;
use tavo_ai::Scanner;

async fn scan_with_streaming(client: &Client) -> Result<(), Box<dyn std::error::Error>> {
    let mut scanner = client.create_scanner();

    // Process results as they come
    let results_handle = tokio::spawn(async move {
        while let Some(result) = scanner.results.next().await {
            println!("Scanned {}: {} issues", result.file_name, result.total_issues);
        }
    });

    // Process errors
    let errors_handle = tokio::spawn(async move {
        while let Some(error) = scanner.errors.next().await {
            eprintln!("Scan error: {}", error);
        }
    });

    // Start scanning multiple files
    let files = vec!["file1.rs", "file2.rs", "file3.rs"];
    scanner.scan_files(files).await?;

    // Wait for processing to complete
    let (results_result, errors_result) = tokio::try_join!(results_handle, errors_handle)?;
    results_result?;
    errors_result?;

    Ok(())
}
```

### Custom HTTP Client

```rust
use reqwest::Client as HttpClient;

// Use custom HTTP client
let http_client = HttpClient::builder()
    .timeout(Duration::from_secs(30))
    .pool_max_idle_per_host(10)
    .build()?;

let client = Client::with_http_client("your-api-key", http_client)?;
```

### Middleware and Hooks

```rust
use tavo_ai::ClientBuilder;

// Add request/response hooks
let client = ClientBuilder::new("your-api-key")
    .with_request_hook(|req| {
        println!("Making request to: {}", req.url());
        Ok(())
    })
    .with_response_hook(|resp, duration| {
        println!("Response received in {:?}", duration);
        Ok(())
    })
    .build()?;
```

## Integration Examples

### Actix Web Framework

```rust
use actix_web::{web, App, HttpResponse, HttpServer, Result as ActixResult};
use serde::{Deserialize, Serialize};
use tavo_ai::Client;

#[derive(Deserialize)]
struct ScanRequest {
    code: String,
    language: Option<String>,
}

#[derive(Serialize)]
struct ScanResponse {
    total_issues: usize,
    vulnerabilities: Vec<VulnerabilityDto>,
}

#[derive(Serialize)]
struct VulnerabilityDto {
    title: String,
    description: String,
    severity: String,
    location: Option<LocationDto>,
}

#[derive(Serialize)]
struct LocationDto {
    file: String,
    line: usize,
    column: usize,
}

async fn scan_code(
    req: web::Json<ScanRequest>,
    client: web::Data<Client>,
) -> ActixResult<HttpResponse> {
    let language = req.language.as_deref().unwrap_or("rust");

    match client.scan_code(&req.code, language).await {
        Ok(result) => {
            let response = ScanResponse {
                total_issues: result.total_issues,
                vulnerabilities: result.vulnerabilities.into_iter()
                    .map(|v| VulnerabilityDto {
                        title: v.title,
                        description: v.description,
                        severity: v.severity,
                        location: v.location.map(|l| LocationDto {
                            file: l.file,
                            line: l.line,
                            column: l.column,
                        }),
                    })
                    .collect(),
            };

            Ok(HttpResponse::Ok().json(response))
        }
        Err(e) => {
            Ok(HttpResponse::InternalServerError().json(serde_json::json!({
                "error": e.to_string()
            })))
        }
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let client = Client::new("your-api-key")
        .expect("Failed to create Tavo client");

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(client.clone()))
            .route("/scan", web::post().to(scan_code))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
```

### CLI Tool with Clap

```rust
use clap::{Arg, Command};
use std::fs;
use std::io::{self, Read};
use tavo_ai::Client;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = Command::new("tavo-scanner")
        .version("1.0")
        .author("Tavo AI")
        .about("Security scanner using Tavo AI")
        .arg(Arg::new("api-key")
            .long("api-key")
            .help("Tavo AI API key")
            .takes_value(true))
        .arg(Arg::new("language")
            .long("lang")
            .help("Programming language")
            .default_value("rust")
            .takes_value(true))
        .arg(Arg::new("file")
            .long("file")
            .help("File to scan")
            .takes_value(true))
        .get_matches();

    let api_key = matches.value_of("api-key")
        .map(String::from)
        .or_else(|| std::env::var("TAVO_API_KEY").ok())
        .ok_or("API key required. Use --api-key or set TAVO_API_KEY environment variable")?;

    let client = Client::new(&api_key)?;

    let code = if let Some(file_path) = matches.value_of("file") {
        fs::read_to_string(file_path)?
    } else {
        println!("Enter code to scan (press Ctrl+D when done):");
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer)?;
        buffer
    };

    let language = matches.value_of("language").unwrap();

    let result = client.scan_code(&code, language).await?;

    println!("Found {} issues:", result.total_issues);
    for (i, vuln) in result.vulnerabilities.iter().enumerate() {
        println!("{}. {} ({})", i + 1, vuln.title, vuln.severity);
        println!("   {}", vuln.description);
        if let Some(location) = &vuln.location {
            println!("   Location: {}:{}:{}", location.file, location.line, location.column);
        }
    }

    Ok(())
}
```

### Library with Error Propagation

```rust
use tavo_ai::{Client, Error};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum SecurityError {
    #[error("Tavo API error: {0}")]
    Tavo(#[from] Error),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

pub struct SecurityScanner {
    client: Client,
}

impl SecurityScanner {
    pub fn new(api_key: &str) -> Result<Self, Error> {
        Ok(Self {
            client: Client::new(api_key)?,
        })
    }

    pub async fn scan_file(&self, path: &str) -> Result<ScanResult, SecurityError> {
        let code = std::fs::read_to_string(path)?;
        let result = self.client.scan_code(&code, "rust").await?;
        Ok(result)
    }

    pub async fn scan_directory(&self, dir_path: &str) -> Result<Vec<(String, ScanResult)>, SecurityError> {
        let mut results = Vec::new();

        for entry in std::fs::read_dir(dir_path)? {
            let entry = entry?;
            let path = entry.path();

            if path.extension().and_then(|s| s.to_str()) == Some("rs") {
                let result = self.scan_file(path.to_str().unwrap()).await?;
                results.push((path.to_string_lossy().to_string(), result));
            }
        }

        Ok(results)
    }
}
```

### Testing with Tokio

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tavo_ai::Client;

    #[tokio::test]
    async fn test_scan_code_detects_sql_injection() {
        let client = Client::new("test-api-key").unwrap();
        // Use a mock server for testing
        // client.set_base_url("http://localhost:8080");

        let code = r#"
            fn process_user_input(user_input: &str) {
                let query = format!("SELECT * FROM users WHERE id = '{}'", user_input);
                // SQL injection vulnerability
            }
        "#;

        let result = client.scan_code(code, "rust").await.unwrap();

        assert!(result.total_issues > 0, "Expected to find security issues");

        let sql_injection_found = result.vulnerabilities
            .iter()
            .any(|v| v.title.to_lowercase().contains("sql injection"));

        assert!(sql_injection_found, "Expected SQL injection vulnerability to be detected");
    }

    #[tokio::test]
    async fn test_scan_code_handles_timeout() {
        let client = Client::new("test-api-key").unwrap();

        let code = "fn main() {}";

        let result = tokio::time::timeout(
            std::time::Duration::from_millis(1),
            client.scan_code(code, "rust")
        ).await;

        assert!(result.is_err(), "Expected timeout error");
    }
}
```

## Best Practices

1. **Error Handling**: Use structured error types and proper error propagation
2. **Async/Await**: Always use async methods with proper await
3. **Ownership**: Leverage Rust's ownership system for memory safety
4. **Concurrency**: Use tokio for concurrent operations
5. **Timeouts**: Set appropriate timeouts to prevent hanging operations
6. **Rate Limiting**: Implement proper rate limiting and backoff strategies
7. **Resource Management**: Use RAII patterns for resource cleanup

## Performance Considerations

- **Zero-Cost Abstractions**: The SDK uses Rust's zero-cost abstractions
- **Async Runtime**: Built on tokio for efficient async operations
- **Connection Reuse**: HTTP connections are automatically reused
- **Memory Safety**: Compile-time guarantees prevent memory errors
- **Concurrent Operations**: Use futures for parallel scanning
