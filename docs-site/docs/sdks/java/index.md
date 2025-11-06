# Java SDK

The Tavo AI Java SDK provides generated API clients for all platform endpoints plus integrated tavo-scanner execution capabilities. Built for enterprise Java development with reactive programming support.

## Installation

### Maven
```xml
<dependency>
    <groupId>net.tavoai</groupId>
    <artifactId>tavo-sdk</artifactId>
    <version>0.1.0</version>
</dependency>
```

### Gradle
```gradle
implementation 'net.tavoai:tavo-sdk:0.1.0'
```

## Architecture

The Java SDK provides two main components:

### API Clients
Generated async clients for all Tavo AI REST API endpoints located in `packages/java/src/endpoints/`:
- `DeviceAuthClient` - Device authentication operations
- `ScanToolsClient` - Core scanning functionality
- And 22+ additional endpoint clients

### Scanner Integration
Built-in tavo-scanner wrapper in `packages/java/src/TavoScanner.java`:
- Process execution of tavo-scanner binary
- Plugin and rule configuration management
- Automatic binary discovery
- CompletableFuture-based async execution

## Quick Start

```java
import net.tavoai.sdk.TavoSdk;

// API client usage
TavoClient client = TavoSdk.createClient("your-api-key");
CompletableFuture<ScanResult> result = client.getDeviceAuth()
    .postCodeAsync("123", "test");

// Scanner usage
TavoScanner scanner = TavoSdk.createScanner();
CompletableFuture<ScanResult> scanResult = scanner.scanDirectory("./my-project", 
    new ScanOptions().setStaticPlugins(Arrays.asList("security", "performance")));
```

## Authentication

```java
import net.tavoai.sdk.TavoSdk;

// API Key authentication (recommended)
TavoClient client = TavoSdk.createClient("your-api-key");

// JWT Token authentication
TavoClient client = TavoSdk.createClient("api-key", "jwt-token", null);

// Device token authentication
TavoClient client = TavoSdk.createClient("api-key", null, "device-token");
```

## API Client Usage

```java
TavoClient client = TavoSdk.createClient("your-api-key");

// Authentication operations
CompletableFuture<ScanResult> authResult = client.getDeviceAuth()
    .postCodeAsync("client_id", "client_name");

// Scanning operations
CompletableFuture<ScanResult> scanResult = client.getScanTools().getScanAsync("scan_id");
CompletableFuture<ScanResult> bulkResult = client.getScanBulkOperations()
    .createBulkScanAsync(scanConfigs);

// AI Analysis
CompletableFuture<ScanResult> analysis = client.getAiAnalysis()
    .analyzeCodeAsync("code", "java");

// Jobs management
CompletableFuture<ScanResult> jobs = client.getJobs().listJobsAsync();
CompletableFuture<ScanResult> jobStatus = client.getJobs().getJobAsync("job_id");

// Health checks
CompletableFuture<ScanResult> health = client.getHealth().healthCheckAsync();
```

## Scanner Integration

```java
import net.tavoai.sdk.TavoSdk;

// Basic scanning
TavoScanner scanner = TavoSdk.createScanner();
CompletableFuture<ScanResult> result = scanner.scanDirectory("./my-project", null);

// Advanced scanning with plugins
ScanOptions options = new ScanOptions()
    .setStaticPlugins(Arrays.asList("security", "performance"));
CompletableFuture<ScanResult> result = scanner.scanDirectory("./my-project", options);

// Custom rules and configuration
CompletableFuture<ScanResult> result = scanner.scanWithRules("./my-project", "./custom-rules.json");
```

## Contributing & Support

- 📖 [API Reference](../../api-reference/overview.md)
- 🐛 [GitHub Issues](https://github.com/tavoai/tavo-sdk/issues)
