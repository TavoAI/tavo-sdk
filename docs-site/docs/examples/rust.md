# Rust SDK Examples

This directory contains comprehensive examples for using the Tavo AI Rust SDK.

## Installation

### Cargo.toml

```toml
[dependencies]
tavo-sdk = "1.0"
tokio = { version = "1", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
anyhow = "1.0"
```

## Basic Usage

### Simple Code Scan

```rust
use tavo_sdk::{TavoClient, models::{ScanResult, Vulnerability}};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize client
    let client = TavoClient::new("your-api-key")?;

    // Code to scan
    let code = r#"
        fn process_user_input(user_input: &str) {
            let query = format!("SELECT * FROM users WHERE id = '{}'", user_input);
            // Potential SQL injection vulnerability
            execute_query(&query);
        }
    "#;

    // Scan the code
    match client.scan_code(code, "rust").await {
        Ok(result) => {
            println!("Found {} issues", result.total_issues);

            for vuln in &result.vulnerabilities {
                println!("- {}: {}", vuln.title, vuln.description);
            }
        }
        Err(e) => {
            eprintln!("Scan failed: {}", e);
        }
    }

    Ok(())
}
```

### Configuration and Error Handling

```rust
use tavo_sdk::{TavoClient, TavoClientConfig, error::TavoError};
use std::time::Duration;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Configure client
    let config = TavoClientConfig::builder()
        .api_key("your-api-key")
        .base_url("https://api.tavoai.net")
        .timeout(Duration::from_secs(30))
        .max_retries(3)
        .retry_delay(Duration::from_secs(1))
        .build();

    let client = TavoClient::with_config(config)?;

    match client.scan_code("println!(\"hello\");", "rust").await {
        Ok(result) => {
            println!("Scan successful: {} issues", result.total_issues);
        }
        Err(TavoError::Auth(e)) => {
            eprintln!("Authentication failed: {}", e);
        }
        Err(TavoError::Api { status_code, message }) => {
            eprintln!("API error: {} (status: {})", message, status_code);
        }
        Err(TavoError::Other(e)) => {
            eprintln!("Tavo error: {}", e);
        }
        Err(e) => {
            eprintln!("Unexpected error: {}", e);
        }
    }

    Ok(())
}
```

## Advanced Examples

### Concurrent Batch Scanning

```rust
use tavo_sdk::{TavoClient, models::ScanResult};
use tokio::sync::Semaphore;
use std::collections::HashMap;
use std::sync::Arc;
use anyhow::Result;

struct BatchScanner {
    client: TavoClient,
}

impl BatchScanner {
    fn new(api_key: &str) -> Result<Self> {
        Ok(Self {
            client: TavoClient::new(api_key)?,
        })
    }

    async fn scan_directory(&self, directory_path: &str, max_concurrency: usize) -> Result<i32> {
        let files = self.find_rust_files(directory_path).await?;
        let semaphore = Arc::new(Semaphore::new(max_concurrency));
        let mut tasks = Vec::new();

        for file in files {
            let permit = semaphore.clone().acquire_owned().await?;
            let client = &self.client;

            let task = tokio::spawn(async move {
                let _permit = permit; // Hold permit until task completes
                match Self::scan_file(client, &file).await {
                    Ok(issues) => {
                        println!("{}: {} issues", file, issues);
                        Ok(issues)
                    }
                    Err(e) => {
                        eprintln!("Failed to scan {}: {}", file, e);
                        Ok(0)
                    }
                }
            });

            tasks.push(task);
        }

        let mut total_issues = 0;
        for task in tasks {
            if let Ok(Ok(issues)) = task.await {
                total_issues += issues;
            }
        }

        println!("Total issues found: {}", total_issues);
        Ok(total_issues)
    }

    async fn find_rust_files(&self, directory_path: &str) -> Result<Vec<String>> {
        let mut files = Vec::new();

        for entry in walkdir::WalkDir::new(directory_path)
            .into_iter()
            .filter_map(|e| e.ok())
            .filter(|e| e.file_type().is_file())
        {
            if let Some(ext) = entry.path().extension() {
                if ext == "rs" {
                    files.push(entry.path().to_string_lossy().to_string());
                }
            }
        }

        Ok(files)
    }

    async fn scan_file(client: &TavoClient, file_path: &str) -> Result<i32> {
        let code = tokio::fs::read_to_string(file_path).await?;
        let result = client.scan_code(&code, "rust").await?;
        Ok(result.total_issues)
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let scanner = BatchScanner::new("your-api-key")?;
    scanner.scan_directory("./src", 5).await?;
    Ok(())
}
```

### AI Model Analysis

```rust
use tavo_sdk::{TavoClient, models::ModelAnalysis};
use serde_json::{json, Value};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = TavoClient::new("your-api-key")?;

    let model_config: Value = json!({
        "model_type": "transformer",
        "architecture": {
            "layers": 12,
            "attention_heads": 8,
            "hidden_size": 768,
            "vocab_size": 30000
        },
        "training": {
            "dataset": "wikipedia",
            "epochs": 10,
            "learning_rate": 0.0001
        }
    });

    match client.analyze_model(model_config).await {
        Ok(analysis) => {
            println!("Model safety: {}", if analysis.is_safe { "Safe" } else { "Unsafe" });

            if !analysis.is_safe {
                if let Some(issues) = &analysis.issues {
                    println!("Issues found:");
                    for (i, issue) in issues.iter().enumerate() {
                        println!("{}. {}: {}", i + 1, issue.title, issue.description);
                    }
                }
            }
        }
        Err(e) => {
            eprintln!("Analysis failed: {}", e);
        }
    }

    Ok(())
}
```

### Webhook Management

```rust
use tavo_sdk::{TavoClient, models::{Webhook, WebhookConfig}};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = TavoClient::new("your-api-key")?;

    // Create a webhook
    let config = WebhookConfig {
        url: "https://myapp.com/webhook/scan-complete".to_string(),
        events: vec!["scan.completed".to_string(), "vulnerability.found".to_string()],
        secret: "webhook-secret".to_string(),
        active: true,
    };

    match client.create_webhook(config).await {
        Ok(webhook) => {
            println!("Created webhook: {}", webhook.id);

            // List all webhooks
            match client.list_webhooks().await {
                Ok(webhooks) => {
                    println!("Total webhooks: {}", webhooks.len());
                    for wh in &webhooks {
                        println!("- {}: {} ({})", wh.id, wh.url, wh.events.join(", "));
                    }
                }
                Err(e) => eprintln!("Failed to list webhooks: {}", e),
            }

            // Update webhook
            let update_config = WebhookConfig {
                events: vec![
                    "scan.completed".to_string(),
                    "vulnerability.found".to_string(),
                    "scan.failed".to_string(),
                ],
                ..Default::default()
            };

            if let Err(e) = client.update_webhook(&webhook.id, update_config).await {
                eprintln!("Failed to update webhook: {}", e);
            } else {
                println!("Webhook updated");
            }

            // Delete the webhook
            if let Err(e) = client.delete_webhook(&webhook.id).await {
                eprintln!("Failed to delete webhook: {}", e);
            } else {
                println!("Webhook deleted");
            }
        }
        Err(e) => {
            eprintln!("Failed to create webhook: {}", e);
        }
    }

    Ok(())
}
```

## Integration Examples

### Axum Web API

```rust
use axum::{
    extract::State,
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tavo_sdk::{TavoClient, error::TavoError, models::{ScanResult, Vulnerability}};
use tower_http::cors::CorsLayer;

#[derive(Clone)]
struct AppState {
    tavo_client: Arc<TavoClient>,
}

#[derive(Deserialize)]
struct ScanRequest {
    code: String,
    language: String,
}

#[derive(Serialize)]
struct ScanResponse {
    total_issues: i32,
    vulnerabilities: Vec<VulnerabilityDto>,
    scan_id: Option<String>,
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
    line: i32,
    column: i32,
}

async fn scan_code(
    State(state): State<AppState>,
    Json(request): Json<ScanRequest>,
) -> Result<Json<ScanResponse>, StatusCode> {
    match state.tavo_client.scan_code(&request.code, &request.language).await {
        Ok(result) => {
            let vulnerabilities = result.vulnerabilities
                .into_iter()
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
                .collect();

            let response = ScanResponse {
                total_issues: result.total_issues,
                vulnerabilities,
                scan_id: result.scan_id,
            };

            Ok(Json(response))
        }
        Err(TavoError::Auth(_)) => Err(StatusCode::UNAUTHORIZED),
        Err(TavoError::Api { status_code, .. }) => Err(StatusCode::from_u16(status_code as u16).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR)),
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let api_key = std::env::var("TAVO_API_KEY")
        .map_err(|_| "TAVO_API_KEY environment variable not set")?;

    let tavo_client = Arc::new(TavoClient::new(&api_key)?);

    let app_state = AppState { tavo_client };

    let app = Router::new()
        .route("/api/security/scan", post(scan_code))
        .layer(CorsLayer::permissive())
        .with_state(app_state);

    let addr = "0.0.0.0:3000".parse()?;
    println!("Server running on {}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await?;

    Ok(())
}
```

### Actix Web API

```rust
use actix_web::{
    web, App, HttpResponse, HttpServer, Result as ActixResult,
    middleware::Logger,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tavo_sdk::{TavoClient, error::TavoError, models::{ScanResult, Vulnerability}};

#[derive(Deserialize)]
struct ScanRequest {
    code: String,
    language: String,
}

#[derive(Serialize)]
struct ScanResponse {
    total_issues: i32,
    vulnerabilities: Vec<VulnerabilityDto>,
    scan_id: Option<String>,
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
    line: i32,
    column: i32,
}

async fn scan_code(
    req: web::Json<ScanRequest>,
    data: web::Data<AppState>,
) -> ActixResult<HttpResponse> {
    match data.tavo_client.scan_code(&req.code, &req.language).await {
        Ok(result) => {
            let vulnerabilities = result.vulnerabilities
                .into_iter()
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
                .collect();

            let response = ScanResponse {
                total_issues: result.total_issues,
                vulnerabilities,
                scan_id: result.scan_id,
            };

            Ok(HttpResponse::Ok().json(response))
        }
        Err(TavoError::Auth(_)) => Ok(HttpResponse::Unauthorized().finish()),
        Err(TavoError::Api { status_code, .. }) => Ok(HttpResponse::new(actix_web::http::StatusCode::from_u16(status_code as u16).unwrap_or(actix_web::http::StatusCode::INTERNAL_SERVER_ERROR))),
        Err(_) => Ok(HttpResponse::InternalServerError().finish()),
    }
}

struct AppState {
    tavo_client: Arc<TavoClient>,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();

    let api_key = std::env::var("TAVO_API_KEY")
        .expect("TAVO_API_KEY environment variable not set");

    let tavo_client = Arc::new(TavoClient::new(&api_key).expect("Failed to create Tavo client"));

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(AppState {
                tavo_client: tavo_client.clone(),
            }))
            .wrap(Logger::default())
            .route("/api/security/scan", web::post().to(scan_code))
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}
```

### CLI Tool with Clap

```rust
use clap::{Arg, Command};
use std::path::Path;
use tavo_sdk::{TavoClient, models::ScanResult};
use tokio::fs;
use walkdir::WalkDir;

#[derive(Debug)]
struct ScanResultWithPath {
    file_path: String,
    issues: i32,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = Command::new("tavo-scanner")
        .version("1.0")
        .author("Tavo AI")
        .about("Tavo AI Security Scanner CLI")
        .arg(
            Arg::new("api-key")
                .short('k')
                .long("api-key")
                .value_name("KEY")
                .help("Tavo AI API key")
                .takes_value(true),
        )
        .arg(
            Arg::new("language")
                .short('l')
                .long("language")
                .value_name("LANG")
                .help("Programming language")
                .default_value("rust")
                .takes_value(true),
        )
        .arg(
            Arg::new("recursive")
                .short('r')
                .long("recursive")
                .help("Scan directories recursively"),
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Verbose output"),
        )
        .arg(
            Arg::new("path")
                .help("File or directory to scan")
                .required(true)
                .index(1),
        )
        .get_matches();

    // Get API key from option or environment
    let api_key = matches
        .value_of("api-key")
        .map(|s| s.to_string())
        .or_else(|| std::env::var("TAVO_API_KEY").ok())
        .ok_or("API key required. Use --api-key or set TAVO_API_KEY environment variable")?;

    let language = matches.value_of("language").unwrap();
    let recursive = matches.is_present("recursive");
    let verbose = matches.is_present("verbose");
    let path = matches.value_of("path").unwrap();

    let client = TavoClient::new(&api_key)?;

    let exit_code = if Path::new(path).is_file() {
        let issues = scan_file(&client, path, language, verbose).await?;
        if issues > 0 { 1 } else { 0 }
    } else if Path::new(path).is_dir() {
        let issues = scan_directory(&client, path, language, recursive, verbose).await?;
        if issues > 0 { 1 } else { 0 }
    } else {
        eprintln!("❌ Path is neither a file nor directory");
        1
    };

    std::process::exit(exit_code);
}

async fn scan_file(
    client: &TavoClient,
    file_path: &str,
    language: &str,
    verbose: bool,
) -> Result<i32, Box<dyn std::error::Error>> {
    let code = fs::read_to_string(file_path).await?;
    let result = client.scan_code(&code, language).await?;
    print_scan_result(file_path, &result, verbose);
    Ok(result.total_issues)
}

async fn scan_directory(
    client: &TavoClient,
    dir_path: &str,
    language: &str,
    recursive: bool,
    verbose: bool,
) -> Result<i32, Box<dyn std::error::Error>> {
    let files = find_files_to_scan(dir_path, language, recursive);
    let mut total_issues = 0;

    for file in files {
        match scan_file(client, &file, language, verbose).await {
            Ok(issues) => total_issues += issues,
            Err(e) => eprintln!("❌ Error scanning {}: {}", file, e),
        }
    }

    println!("\n📊 Summary: {} total issues", total_issues);
    Ok(total_issues)
}

fn find_files_to_scan(dir_path: &str, language: &str, recursive: bool) -> Vec<String> {
    let extension = match language {
        "rust" => "rs",
        "python" => "py",
        "javascript" | "typescript" => "js",
        "go" => "go",
        "java" => "java",
        "csharp" => "cs",
        _ => "rs",
    };

    WalkDir::new(dir_path)
        .max_depth(if recursive { usize::MAX } else { 1 })
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| e.file_type().is_file())
        .filter(|e| e.path().extension().map_or(false, |ext| ext == extension))
        .map(|e| e.path().to_string_lossy().to_string())
        .collect()
}

fn print_scan_result(file_path: &str, result: &ScanResult, verbose: bool) {
    if result.total_issues > 0 {
        println!("\n🔴 {} ({} issues):", file_path, result.total_issues);

        for (i, vuln) in result.vulnerabilities.iter().enumerate() {
            println!("  {}. {} ({})", i + 1, vuln.title, vuln.severity);
            if verbose {
                println!("     {}", vuln.description);
                if let Some(location) = &vuln.location {
                    println!("     📍 {}:{}:{}", location.file, location.line, location.column);
                }
            }
        }
    } else {
        println!("✅ {} (0 issues)", file_path);
    }
}
```

## Testing Examples

### Unit Tests with Tokio Test

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tavo_sdk::error::TavoError;
    use tavo_sdk::models::{ScanResult, Vulnerability};

    #[tokio::test]
    async fn test_scan_code_success() {
        // Note: This would require mocking the HTTP client
        // For real tests, you'd use integration tests with a test server
        assert!(true); // Placeholder
    }

    #[tokio::test]
    async fn test_scan_code_api_error() {
        // Note: This would require mocking API errors
        assert!(true); // Placeholder
    }
}
```

### Integration Tests

```rust
#[cfg(test)]
mod integration_tests {
    use super::*;
    use std::env;
    use tavo_sdk::models::ScanResult;

    #[tokio::test]
    async fn test_scan_vulnerable_code_detects_sql_injection() {
        let api_key = env::var("TAVO_API_KEY")
            .expect("TAVO_API_KEY environment variable required");

        let client = TavoClient::new(&api_key).unwrap();

        let vulnerable_code = r#"
            fn authenticate(username: &str, password: &str) {
                let query = format!("SELECT * FROM users WHERE username='{}' AND password='{}'",
                                   username, password);
                // SQL injection vulnerability
                execute_query(&query);
            }
        "#;

        let result = client.scan_code(vulnerable_code, "rust").await.unwrap();

        assert!(result.total_issues > 0);
        assert!(result.vulnerabilities.iter().any(|v|
            v.title.to_lowercase().contains("sql") &&
            v.title.to_lowercase().contains("injection")
        ));
    }

    #[tokio::test]
    async fn test_scan_safe_code_no_high_severity_issues() {
        let api_key = env::var("TAVO_API_KEY")
            .expect("TAVO_API_KEY environment variable required");

        let client = TavoClient::new(&api_key).unwrap();

        let safe_code = r#"
            fn authenticate(username: &str, password: &str) {
                let query = "SELECT * FROM users WHERE username=? AND password=?";
                execute_query(&query, &[username, password]);
            }
        "#;

        let result = client.scan_code(safe_code, "rust").await.unwrap();

        let high_severity_count = result.vulnerabilities.iter()
            .filter(|v| v.severity == "critical" || v.severity == "high")
            .count();

        assert_eq!(high_severity_count, 0);
    }
}
```

### Performance Tests with Criterion

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use tavo_sdk::TavoClient;

fn scan_code_benchmark(c: &mut Criterion) {
    let client = TavoClient::new("benchmark-api-key").unwrap();

    let test_code = r#"
        fn test_function(user_id: i32, user_input: &str) {
            let sql = format!("SELECT * FROM users WHERE id = {}", user_id);
            execute_query(&sql);

            let cmd = format!("ls {}", user_input);
            execute_command(&cmd);

            let xpath = format!("//users[@id='{}']", user_id);
            evaluate_xpath(&xpath);
        }
    "#;

    c.bench_function("scan_code", |b| {
        b.iter(|| {
            let _result = black_box(client.scan_code(test_code, "rust"));
        })
    });
}

criterion_group!(benches, scan_code_benchmark);
criterion_main!(benches);
```
