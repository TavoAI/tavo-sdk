# .NET SDK

The Tavo AI .NET SDK provides generated API clients for all platform endpoints plus integrated tavo-scanner execution capabilities. Built for cross-platform .NET development with async/await support.

## Installation

```bash
dotnet add package TavoAI
```

or via NuGet Package Manager:
```
Install-Package TavoAI
```

## Architecture

The .NET SDK provides two main components:

### API Clients
Generated async clients for all Tavo AI REST API endpoints located in `packages/dotnet/src/endpoints/`:
- `DeviceAuthClient` - Device authentication operations
- `ScanToolsClient` - Core scanning functionality
- And 22+ additional endpoint clients

### Scanner Integration
Built-in tavo-scanner wrapper in `packages/dotnet/src/TavoScanner.cs`:
- Process execution of tavo-scanner binary
- Plugin and rule configuration management
- Automatic binary discovery
- Async execution with cancellation support

## Quick Start

```csharp
using TavoAI;

// API client usage
var client = TavoSdk.CreateClient("your-api-key");
var result = await client.DeviceAuth.PostCodeAsync("123", "test");

// Scanner usage
var scanner = TavoSdk.CreateScanner();
var scanResult = await scanner.ScanDirectoryAsync("./my-project", new ScanOptions {
    Plugins = new[] { "security", "performance" }
});
```

## Authentication

```csharp
using TavoAI;

// API Key authentication (recommended)
var client = TavoSdk.CreateClient("your-api-key");

// JWT Token authentication
var client = TavoSdk.CreateClientWithAuth("your-jwt-token");

// Device token authentication
var client = TavoSdk.CreateClientWithDeviceToken("your-device-token");
```

## API Client Usage

```csharp
var client = TavoSdk.CreateClient("your-api-key");

// Authentication operations
var authResult = await client.DeviceAuth.PostCodeAsync("client_id", "client_name");

// Scanning operations
var scanResult = await client.ScanTools.GetScanAsync("scan_id");
var bulkResult = await client.ScanBulkOperations.CreateBulkScanAsync(scanConfigs);

// AI Analysis
var analysis = await client.AiAnalysis.AnalyzeCodeAsync("code", "csharp");

// Jobs management
var jobs = await client.Jobs.ListJobsAsync();
var jobStatus = await client.Jobs.GetJobAsync("job_id");

// Health checks
var health = await client.Health.HealthCheckAsync();
```

## Scanner Integration

```csharp
using TavoAI;

// Basic scanning
var scanner = TavoSdk.CreateScanner();
var result = await scanner.ScanDirectoryAsync("./my-project");

// Advanced scanning with plugins
var result = await scanner.ScanWithPluginsAsync("./my-project", 
    new[] { "security", "performance" });

// Custom rules and configuration
var result = await scanner.ScanWithRulesAsync("./my-project", "./custom-rules.json");
```

## Contributing & Support

- 📖 [API Reference](../../api-reference/overview.md)
- 🐛 [GitHub Issues](https://github.com/tavoai/tavo-sdk/issues)
