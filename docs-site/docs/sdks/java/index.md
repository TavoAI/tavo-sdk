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

The Java SDK provides an enterprise-grade, modular architecture with generated API clients and integrated scanner capabilities.

### Modular API Clients

The SDK provides **26 specialized client classes** for different API endpoint categories, each with full type safety and reactive programming support:

#### Core Scanning (`client.scanManagement()`, `client.scanTools()`, etc.)
```java
// Scan management operations
ScanManagementClient scanClient = client.scanManagement();
CompletableFuture<ScanResult> result = scanClient.createScanAsync(
    "https://github.com/your-org/your-repo", "security", "main"
);

// Scan tools and rules
ScanToolsClient toolsClient = client.scanTools();
ScanRulesClient rulesClient = client.scanRules();
```

#### AI Analysis (`client.aiAnalysis()`, `client.aiAnalysisCore()`, etc.)
```java
// AI-powered analysis
AiAnalysisClient aiClient = client.aiAnalysis();
CompletableFuture<AiAnalysisResult> analysis = aiClient.analyzeCodeAsync(
    "System.out.println(\"hello\")", "java"
);

// Risk compliance checking
AiRiskComplianceClient complianceClient = client.aiRiskCompliance();
CompletableFuture<ComplianceReport> report = complianceClient.checkComplianceAsync("123");
```

#### Repository & Registry Management
```java
// Repository operations
RepositoriesClient repoClient = client.repositories();
RepositoryConnectionsClient connectionsClient = client.repositoryConnections();

// Plugin marketplace
PluginMarketplaceClient marketplaceClient = client.pluginMarketplace();
CompletableFuture<List<Plugin>> plugins = marketplaceClient.listPluginsAsync();
```

#### Authentication & Device Management
```java
// Device authentication flow
DeviceAuthClient authClient = client.deviceAuth();
CompletableFuture<AuthResult> authResult = authClient.postCodeAsync(
    "your-client-id", "my-security-scanner"
);
```

### Scanner Integration

Enterprise-grade scanner integration with reactive patterns:
- **CompletableFuture-based async execution** with proper error handling
- **Plugin and rule management** with validation
- **Automatic binary discovery** (relative paths, PATH, and custom locations)
- **Structured result parsing** with comprehensive type safety
- **Progress monitoring** and cancellation support
- **Memory-efficient processing** for large scan outputs

## Quick Start

```java
import net.tavoai.sdk.TavoSdk;
import java.util.concurrent.CompletableFuture;
import java.util.Arrays;

public class Example {
    public static void main(String[] args) {
        // Initialize API client with modular architecture
        TavoClient client = TavoSdk.createClient("your-api-key");

        // 1. Device authentication
        DeviceAuthClient authClient = client.deviceAuth();
        CompletableFuture<AuthResult> authFuture = authClient.postCodeAsync(
            "your-client-id", "my-security-scanner"
        );

        authFuture.thenAccept(authResult -> {
            System.out.println("Device auth successful: " + authResult);

            // 2. Create and run a security scan
            ScanManagementClient scanClient = client.scanManagement();
            CompletableFuture<ScanResult> scanFuture = scanClient.createScanAsync(
                "https://github.com/your-org/your-repo", "security", "main"
            );

            scanFuture.thenAccept(scanResult -> {
                System.out.println("Scan created: " + scanResult);

                // 3. Get AI-powered analysis
                AiAnalysisClient aiClient = client.aiAnalysis();
                aiClient.analyzeScanAsync(scanResult.getId())
                    .thenAccept(analysis -> {
                        System.out.println("AI analysis found issues: " +
                            analysis.getVulnerabilities().size());

                        // 4. Alternative: Use integrated scanner
                        TavoScanner scanner = TavoSdk.createScanner();
                        scanner.scanDirectory("./my-project",
                            Arrays.asList("security", "performance"),
                            Arrays.asList("custom-security-rules"))
                            .thenAccept(localResult -> {
                                System.out.println("Local scan found issues: " +
                                    localResult.getTotalIssues());
                            });
                    });
            });
        }).join(); // Wait for completion
    }
}
```

## Client Architecture

The `TavoClient` provides access to all API endpoints through modular client properties:

```java
TavoClient client = TavoSdk.createClient("your-api-key");

// Access different API categories
client.deviceAuth();        // Device authentication
client.scanManagement();    // Scan lifecycle management
client.aiAnalysis();        // AI-powered analysis
client.repositories();      // Repository operations
client.pluginMarketplace(); // Plugin management
client.registry();          // Registry operations
// ... and 20+ more specialized clients
```

Each client provides fully typed async methods matching the REST API:

```java
// Type hints and IDE completion
CompletableFuture<ScanResult> result = client.scanManagement().createScanAsync(
    "https://github.com/user/repo", "security", "main"
);
```

## Error Handling

The SDK provides comprehensive error handling with specific exception types:

```java
import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.exceptions.TavoApiException;
import net.tavoai.sdk.exceptions.AuthenticationException;

try {
    TavoClient client = TavoSdk.createClient("invalid-key");
    client.health().getStatusAsync().join();
} catch (AuthenticationException e) {
    System.out.println("Auth failed: " + e.getMessage());
} catch (TavoApiException e) {
    System.out.println("API error: " + e.getStatusCode() + " - " + e.getMessage());
} catch (Exception e) {
    System.err.println("Unexpected error: " + e.getMessage());
}
```

## Best Practices

### Connection Management
```java
// Reuse client instances for multiple requests
TavoClient client = TavoSdk.createClient("your-key");

// Client automatically handles connection pooling
CompletableFuture<Void> allFutures = CompletableFuture.allOf(
    client.scanManagement().listScansAsync(),
    client.repositories().listRepositoriesAsync(),
    client.aiAnalysis().getModelsAsync()
);

allFutures.join(); // Wait for all to complete
```

### Timeout Configuration
```java
// Configure timeouts for long-running operations
TavoClient client = TavoSdk.createClientBuilder("your-key")
    .withTimeout(Duration.ofSeconds(30))
    .build();
```

### Logging
```java
// Enable debug logging
TavoClient client = TavoSdk.createClientBuilder("your-key")
    .withDebugLogging(true)
    .build();
// All requests now logged with timing and errors
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
