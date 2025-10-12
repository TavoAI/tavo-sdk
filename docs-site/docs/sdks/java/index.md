# Java SDK

The Tavo AI Java SDK provides a robust, enterprise-ready interface for integrating with the Tavo AI platform. Built with modern Java patterns, comprehensive error handling, and full asynchronous support.

## Installation

### Maven

```xml
<dependency>
    <groupId>net.tavoai</groupId>
    <artifactId>sdk</artifactId>
    <version>1.0.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'net.tavoai:sdk:1.0.0'
```

## Quick Start

```java
import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ScanResult;

public class Example {
    public static void main(String[] args) {
        // Initialize the client
        TavoClient client = new TavoClient.Builder()
                .apiKey("your-api-key")
                .build();

        // Scan code for vulnerabilities
        String code = """
            public void processUserInput(String userInput) {
                String query = "SELECT * FROM users WHERE id = '" + userInput + "'";
                // Potential SQL injection vulnerability
                executeQuery(query);
            }
            """;

        try {
            ScanResult result = client.scanCode(code, "java").join();

            System.out.println("Found " + result.getTotalIssues() + " issues");
            result.getVulnerabilities().forEach(vuln ->
                System.out.println("- " + vuln.getTitle() + ": " + vuln.getDescription())
            );
        } catch (Exception e) {
            System.err.println("Scan failed: " + e.getMessage());
        }
    }
}
```

## Asynchronous Operations

The SDK provides both synchronous and asynchronous APIs:

```java
// Asynchronous (recommended)
CompletableFuture<ScanResult> future = client.scanCodeAsync(code, "java");
future.thenAccept(result -> {
    System.out.println("Scan complete: " + result.getTotalIssues() + " issues");
}).exceptionally(throwable -> {
    System.err.println("Scan failed: " + throwable.getMessage());
    return null;
});

// Synchronous (blocking)
ScanResult result = client.scanCode(code, "java");
```

## Authentication

```java
// Basic authentication
TavoClient client = new TavoClient.Builder()
        .apiKey("your-api-key")
        .build();

// With custom configuration
TavoClient client = new TavoClient.Builder()
        .apiKey("your-api-key")
        .baseUrl("https://api-staging.tavoai.net")
        .timeout(Duration.ofSeconds(30))
        .build();
```

## Core Operations

### Code Scanning

```java
// Basic code scan
ScanResult result = client.scanCode(code, "java").join();

// Advanced scan with options
ScanOptions options = ScanOptions.builder()
        .language("java")
        .timeout(Duration.ofSeconds(60))
        .includeMetrics(true)
        .build();

ScanResult result = client.scanCode(code, options).join();
```

### AI Model Analysis

```java
Map<String, Object> modelConfig = Map.of(
    "modelType", "transformer",
    "parameters", Map.of(
        "layers", 12,
        "heads", 8,
        "hiddenSize", 768
    )
);

ModelAnalysisResult analysis = client.analyzeModel(modelConfig).join();
System.out.println("Model is safe: " + analysis.isSafe());
```

### User Management

```java
// Get current user
User user = client.getCurrentUser().join();

// Update user profile
User updatedUser = client.updateUser(user.getId(), Map.of(
    "name", "New Name",
    "email", "new@example.com"
)).join();

// API Key Management
List<ApiKey> apiKeys = client.listApiKeys().join();

// Update API key
ApiKey updatedKey = client.updateApiKey(apiKeyId, Map.of(
    "name", "Updated API Key Name",
    "description", "Updated description"
)).join();

// Rotate API key (generates new secret)
ApiKey rotatedKey = client.rotateApiKey(apiKeyId).join();

// Delete API key
client.deleteApiKey(apiKeyId).join();
```

### Organization Management

```java
// List organizations
List<Organization> organizations = client.listOrganizations().join();

// Create new organization
Organization newOrg = client.createOrganization(Map.of(
    "name", "My Company",
    "description", "Security scanning service"
)).join();
```

### Scan Jobs

```java
// Start a new scan job
ScanJob job = client.createScanJob(Map.of(
    "targetUrl", "https://example.com",
    "scanType", "full_scan"
)).join();

// Get job status
ScanJob status = client.getScanJob(job.getId()).join();

// List all jobs with pagination
List<ScanJob> jobs = client.listScanJobs(10, 0).join();
```

### Webhooks

```java
// Create webhook
Webhook webhook = client.createWebhook(Map.of(
    "url", "https://myapp.com/webhook",
    "events", List.of("scan.completed", "vulnerability.found")
)).join();

// List webhooks
List<Webhook> webhooks = client.listWebhooks().join();

// Delete webhook
client.deleteWebhook(webhook.getId()).join();
```

### Billing & Reports

```java
// Get billing information
BillingInfo billing = client.getBillingInfo().join();

// Generate report
Report report = client.generateReport(Map.of(
    "type", "security_audit",
    "dateRange", Map.of(
        "start", "2024-01-01",
        "end", "2024-01-31"
    )
)).join();

// Get report summary statistics
ReportSummary summary = client.getReportSummary().join();

System.out.println("Total scans: " + summary.getTotalScans());
System.out.println("Total vulnerabilities: " + summary.getTotalVulnerabilities());
System.out.println("Critical issues: " + summary.getCriticalIssues());
```

## Error Handling

The SDK provides comprehensive error handling with specific exception types:

```java
import net.tavoai.sdk.exception.*;

try {
    ScanResult result = client.scanCode(code, "java").join();
} catch (AuthenticationException e) {
    System.err.println("Authentication failed - check your API key");
} catch (ApiException e) {
    System.err.println("API error: " + e.getMessage());
} catch (RateLimitException e) {
    System.err.println("Rate limit exceeded, retry after: " + e.getRetryAfter());
} catch (TavoException e) {
    System.err.println("General error: " + e.getMessage());
} catch (Exception e) {
    System.err.println("Unknown error: " + e.getMessage());
}
```

## Configuration

### Custom Base URL

```java
TavoClient client = new TavoClient.Builder()
        .apiKey("your-api-key")
        .baseUrl("https://api-staging.tavoai.net")
        .build();
```

### Timeout Configuration

```java
TavoClient client = new TavoClient.Builder()
        .apiKey("your-api-key")
        .timeout(Duration.ofSeconds(60))
        .build();
```

### Retry Configuration

```java
TavoClient client = new TavoClient.Builder()
        .apiKey("your-api-key")
        .retryConfig(RetryConfig.builder()
                .maxRetries(3)
                .initialDelay(Duration.ofMillis(1000))
                .maxDelay(Duration.ofSeconds(10))
                .build())
        .build();
```

### HTTP Client Configuration

```java
// Custom HTTP client configuration
TavoClient client = new TavoClient.Builder()
        .apiKey("your-api-key")
        .httpClientBuilder(() -> {
            return HttpClient.newBuilder()
                    .connectTimeout(Duration.ofSeconds(10))
                    .followRedirects(HttpClient.Redirect.NORMAL);
        })
        .build();
```

## Advanced Usage

### Reactive Programming with RxJava

```java
import io.reactivex.rxjava3.core.Single;

Single<ScanResult> scanResult = Single.fromFuture(
    client.scanCodeAsync(code, "java")
);

scanResult.subscribe(
    result -> System.out.println("Scan complete: " + result.getTotalIssues() + " issues"),
    error -> System.err.println("Scan failed: " + error.getMessage())
);
```

### Batch Operations

```java
// Scan multiple code snippets concurrently
List<String> codeSnippets = List.of(
    "public class Test1 { }",
    "public class Test2 { }",
    "public class Test3 { }"
);

List<CompletableFuture<ScanResult>> futures = codeSnippets.stream()
        .map(code -> client.scanCodeAsync(code, "java"))
        .collect(Collectors.toList());

// Wait for all scans to complete
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
        .thenRun(() -> {
            List<ScanResult> results = futures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList());

            results.forEach(result ->
                System.out.println("Found " + result.getTotalIssues() + " issues")
            );
        })
        .join();
```

### Custom Request Headers

```java
// Add custom headers to all requests
TavoClient client = new TavoClient.Builder()
        .apiKey("your-api-key")
        .headers(Map.of(
                "X-Custom-Header", "value",
                "User-Agent", "MyApp/1.0"
        ))
        .build();
```

### Resource Management

```java
// Proper resource management with try-with-resources
try (TavoClient client = new TavoClient.Builder()
        .apiKey("your-api-key")
        .build()) {

    ScanResult result = client.scanCode(code, "java").join();
    System.out.println("Scan complete");

} // Client automatically closed
```

## Integration Examples

### Spring Boot Integration

```java
import org.springframework.stereotype.Service;
import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ScanResult;

@Service
public class SecurityScanService {

    private final TavoClient tavoClient;

    public SecurityScanService(@Value("${tavo.api.key}") String apiKey) {
        this.tavoClient = new TavoClient.Builder()
                .apiKey(apiKey)
                .build();
    }

    public CompletableFuture<ScanResult> scanCode(String code, String language) {
        return tavoClient.scanCodeAsync(code, language);
    }
}

// Controller
@RestController
@RequestMapping("/api/security")
public class SecurityController {

    @Autowired
    private SecurityScanService securityService;

    @PostMapping("/scan")
    public CompletableFuture<ResponseEntity<?>> scanCode(@RequestBody ScanRequest request) {
        return securityService.scanCode(request.getCode(), request.getLanguage())
                .thenApply(result -> ResponseEntity.ok(Map.of(
                        "totalIssues", result.getTotalIssues(),
                        "vulnerabilities", result.getVulnerabilities()
                )))
                .exceptionally(throwable ->
                        ResponseEntity.status(500).body(Map.of(
                                "error", throwable.getMessage()
                        ))
                );
    }
}
```

### Quarkus Integration

```java
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import net.tavoai.sdk.TavoClient;

@ApplicationScoped
public class SecurityService {

    private final TavoClient tavoClient;

    @Inject
    public SecurityService(@ConfigProperty(name = "tavo.api.key") String apiKey) {
        this.tavoClient = new TavoClient.Builder()
                .apiKey(apiKey)
                .build();
    }

    public Uni<ScanResult> scanCode(String code, String language) {
        return Uni.createFrom().future(tavoClient.scanCodeAsync(code, language));
    }
}
```

### JUnit Testing

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.mockito.Mockito.*;
import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ScanResult;

class SecurityServiceTest {

    private TavoClient mockClient;
    private SecurityService securityService;

    @BeforeEach
    void setUp() {
        mockClient = mock(TavoClient.class);
        securityService = new SecurityService(mockClient);
    }

    @Test
    void testScanCode() {
        // Arrange
        String code = "public class Test {}";
        ScanResult expectedResult = new ScanResult();
        when(mockClient.scanCodeAsync(code, "java"))
                .thenReturn(CompletableFuture.completedFuture(expectedResult));

        // Act
        CompletableFuture<ScanResult> result = securityService.scanCode(code, "java");

        // Assert
        assertEquals(expectedResult, result.join());
        verify(mockClient).scanCodeAsync(code, "java");
    }
}
```

## Best Practices

1. **Resource Management**: Always close clients when done, preferably using try-with-resources
2. **Async Operations**: Use async methods for better performance and scalability
3. **Error Handling**: Implement comprehensive error handling with specific exception types
4. **Timeouts**: Set appropriate timeouts based on your use case
5. **Rate Limiting**: Implement proper rate limiting and backoff strategies
6. **Testing**: Use dependency injection for testable code

## Performance Considerations

- **Connection Pooling**: The SDK automatically manages HTTP connection pooling
- **Async Operations**: Use async methods to avoid blocking threads
- **Batch Processing**: Group multiple operations when possible
- **Caching**: Implement result caching for frequently scanned code
