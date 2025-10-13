# tavo-ai

Tavo AI SDK for Rust

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
tavo-ai = "0.4"
```

Or use cargo:

```bash
cargo add tavo-ai
```

## Usage

### Basic Usage

```rust
use tavo_ai::TavoClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize client
    let client = TavoClient::new("your-api-key-here")?;

    // Health check
    let health = client.health_check().await?;
    println!("API Status: {}", health.status);

    Ok(())
}
```

### Advanced Usage

```rust
use tavo_ai::{TavoClient, ScanOptions};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = TavoClient::new("your-api-key")?;

    // Scan a repository
    let scan_options = ScanOptions {
        repository_url: "https://github.com/user/repo".to_string(),
        scan_type: "security".to_string(),
    };

    let scan = client.scans().create(scan_options).await?;
    println!("Scan created: {}", scan.id);

    // Get scan results
    let results = client.scans().get_results(&scan.id).await?;
    println!("Vulnerabilities found: {}", results.vulnerabilities.len());

    Ok(())
}
```

### Custom Configuration

```rust
use tavo_ai::TavoClientBuilder;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = TavoClientBuilder::new("your-api-key")
        .base_url("https://api.tavoai.net")?
        .timeout(std::time::Duration::from_secs(30))
        .build()?;

    // Use client...
    Ok(())
}
```

## API Reference

### TavoClient

Main client struct for interacting with Tavo AI API.

#### Methods

- `new(api_key: &str)`: Create a new client with default configuration
- `health_check()`: Check API availability
- `scans()`: Get scans API client

### TavoClientBuilder

Builder for configuring TavoClient instances.

#### Methods

- `new(api_key: &str)`: Create a new builder
- `base_url(url: &str)`: Set custom base URL
- `timeout(duration: Duration)`: Set request timeout
- `build()`: Build the client

### Scans API Methods

- `create(options: ScanOptions)`: Create a new scan
- `get_results(scan_id: &str)`: Get scan results
- `list()`: List all scans

## Authentication

Get your API key from [Tavo AI Dashboard](https://app.tavoai.net).

```bash
export TAVO_API_KEY="your-api-key"
```

## Requirements

- Rust 1.70+
- Tokio runtime

## Examples

See the `examples/` directory for complete usage examples:

```bash
cargo run --example basic_scan
```

## License

Apache-2.0

## Support

- [Documentation](https://docs.rs/tavo-ai)
- [GitHub Issues](https://github.com/TavoAI/tavo-sdk/issues)
- [Community Forum](https://community.tavoai.net)
