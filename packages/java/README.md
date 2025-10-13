# Tavo Java SDK

A Java SDK for integrating with Tavo AI services.

## Installation

### Maven

Add the following dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>net.tavoai</groupId>
    <artifactId>sdk</artifactId>
    <version>0.1.0</version>
</dependency>
```

### Gradle

Add the following to your `build.gradle`:

```gradle
implementation 'net.tavoai:sdk:0.1.0'
```

## Quick Start

```java
import net.tavoai.TavoClient;
import net.tavoai.TavoConfig;

// Create configuration
TavoConfig config = TavoConfig.builder()
    .apiKey("your-api-key-here")
    .baseUrl("https://api.tavoai.net")
    .build();

// Create client
TavoClient client = new TavoClient(config);

// Health check
Map<String, Object> health = client.healthCheck();

// Authenticate
Map<String, Object> auth = client.auth().login(Map.of(
    "email", "user@example.com",
    "password", "password"
));

// Get user profile
Map<String, Object> user = client.users().getCurrentUser();
```

## Configuration

The SDK can be configured using environment variables or the builder pattern:

```java
TavoConfig config = TavoConfig.builder()
    .apiKey(System.getenv("TAVO_API_KEY"))
    .baseUrl(System.getenv("TAVO_BASE_URL")) // Optional, defaults to https://api.tavoai.net
    .maxRetries(3) // Optional, defaults to 3
    .timeout(30000) // Optional, timeout in milliseconds
    .build();
```

Environment variables:
- `TAVO_API_KEY`: Your API key
- `TAVO_BASE_URL`: API base URL (optional)
- `TAVO_MAX_RETRIES`: Maximum retry attempts (optional)
- `TAVO_TIMEOUT`: Request timeout in milliseconds (optional)

## API Operations

The SDK provides access to all Tavo API operations through dedicated operation classes:

### Authentication
```java
client.auth().login(credentials);
client.auth().logout();
client.auth().refreshToken(token);
```

### Users
```java
client.users().getCurrentUser();
client.users().updateProfile(profileData);
client.users().listUsers(params);
```

### Organizations
```java
client.organizations().listOrganizations();
client.organizations().getOrganization(orgId);
client.organizations().createOrganization(data);
```

### Jobs
```java
client.jobs().listJobs(params);
client.jobs().getJob(jobId);
client.jobs().createJob(jobData);
client.jobs().cancelJob(jobId);
```

### Scans
```java
client.scans().listScans(params);
client.scans().getScan(scanId);
client.scans().createScan(scanData);
client.scans().getScanResults(scanId);
```

### Webhooks
```java
client.webhooks().listWebhooks();
client.webhooks().createWebhook(webhookData);
client.webhooks().deleteWebhook(webhookId);
```

### AI Analysis
```java
client.aiAnalysis().analyzeCode(codeData);
client.aiAnalysis().getAnalysisResults(analysisId);
```

### Billing
```java
client.billing().getUsage();
client.billing().getInvoices();
```

### Reports
```java
client.reports().generateReport(params);
client.reports().getReport(reportId);
```

### Scan Rules
```java
client.scanRules().listRules();
client.scanRules().createRule(ruleData);
client.scanRules().updateRule(ruleId, ruleData);
```

## Error Handling

All API methods throw `TavoException` on error:

```java
try {
    Map<String, Object> result = client.scans().getScan(scanId);
} catch (TavoException e) {
    System.err.println("API Error: " + e.getMessage());
    System.err.println("Status Code: " + e.getStatusCode());
}
```

## Building from Source

```bash
git clone <repository-url>
cd tavo-sdk/packages/java
mvn clean install
```

## Testing

```bash
mvn test
```

## Requirements

- Java 11 or higher
- Maven 3.6+ (for building)

## Dependencies

- OkHttp: HTTP client
- Gson: JSON processing
- JUnit 5: Testing framework
- Mockito: Mocking framework (test scope)