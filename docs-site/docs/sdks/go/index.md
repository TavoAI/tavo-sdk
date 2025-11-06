# Go SDK

The Tavo AI Go SDK provides generated API clients for all platform endpoints plus integrated tavo-scanner execution capabilities. Built with Go's context-aware patterns and high performance.

## Installation

```bash
go get github.com/tavo-ai/sdk-go
```

## Architecture

The Go SDK provides two main components:

### API Clients
Generated context-aware clients for all Tavo AI REST API endpoints located in `packages/go/src/endpoints/`:
- `DeviceAuthClient` - Device authentication operations
- `ScanToolsClient` - Core scanning functionality
- And 22+ additional endpoint clients

### Scanner Integration
Built-in tavo-scanner wrapper in `packages/go/src/scanner.go`:
- Subprocess execution of tavo-scanner binary
- Plugin and rule configuration management
- Automatic binary discovery
- Context-based timeout handling

## Quick Start

```go
import "github.com/tavo-ai/sdk-go/sdk"

// API client usage
client := sdk.CreateClientWithAuth("your-api-key", "", "")
result, err := client.DeviceAuth.PostCode("123", "test")

// Scanner usage
scanner := sdk.CreateScanner()
scanResult, err := scanner.ScanDirectory("./my-project", &scanner.ScanOptions{
    Plugins: []string{"security", "performance"},
})
```

## Authentication

```go
import "github.com/tavo-ai/sdk-go/sdk"

// API Key authentication (recommended)
client := sdk.CreateClientWithAuth("your-api-key", "", "")

// JWT Token authentication
client := sdk.CreateClientWithAuth("", "your-jwt-token", "")

// Device token authentication
client := sdk.CreateClientWithAuth("", "", "your-device-token")
```

## API Client Usage

```go
client := sdk.CreateClientWithAuth("your-api-key", "", "")

// Authentication operations
authResult, err := client.DeviceAuth.PostCode("client_id", "client_name")

// Scanning operations
scanResult, err := client.ScanTools.GetScan("scan_id")
bulkResult, err := client.ScanBulkOperations.CreateBulkScan(scanConfigs)

// AI Analysis
analysis, err := client.AiAnalysis.AnalyzeCode("code", "go")

// Jobs management
jobs, err := client.Jobs.ListJobs()
jobStatus, err := client.Jobs.GetJob("job_id")

// Health checks
health, err := client.Health.HealthCheck()
```

## Scanner Integration

```go
import "github.com/tavo-ai/sdk-go/sdk"

// Basic scanning
scanner := sdk.CreateScanner()
result, err := scanner.ScanDirectory("./my-project", nil)

// Advanced scanning with plugins
result, err := scanner.ScanWithPlugins("./my-project", []string{"security", "performance"})

// Custom rules and configuration
result, err := scanner.ScanWithRules("./my-project", "./custom-rules.json")
```

## Contributing & Support

- 📖 [API Reference](../../api-reference/overview.md)
- 🐛 [GitHub Issues](https://github.com/tavoai/tavo-sdk/issues)
