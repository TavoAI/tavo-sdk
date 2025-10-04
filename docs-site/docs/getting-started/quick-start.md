---
sidebar_position: 4
---

# Quick Start

Get up and running with the Tavo AI SDK in minutes.

## Prerequisites

- API key from [tavoai.org](https://tavoai.org)
- SDK installed for your language
- Basic programming knowledge

## Basic Usage

### Health Check

Start by verifying your connection to the Tavo AI API:

```python
# Python
from tavo import TavoClient

client = TavoClient()  # Uses TAVO_API_KEY env var
health = client.health_check()
print("API Status:", health)
```

```javascript
// JavaScript/TypeScript
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient();  // Uses process.env.TAVO_API_KEY
const health = await client.healthCheck();
console.log('API Status:', health);
```

```java
// Java
import net.tavoai.TavoClient;

TavoClient client = new TavoClient();  // Uses TAVO_API_KEY env var
Map<String, Object> health = client.healthCheck();
System.out.println("API Status: " + health);
```

```go
// Go
package main

import (
    "fmt"
    "log"
    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
    config := tavo.NewConfig()  // Uses TAVO_API_KEY env var
    client := tavo.NewClient(config)

    health, err := client.HealthCheck()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("API Status:", health)
}
```

### Authentication

Authenticate and get user information:

```python
# Python
auth = client.auth().login("your-email@example.com", "password")
user = client.auth().me()
print("Welcome,", user["name"])
```

```javascript
// JavaScript
const auth = await client.auth().login('your-email@example.com', 'password');
const user = await client.auth().me();
console.log('Welcome,', user.name);
```

```java
// Java
Map<String, Object> auth = client.auth().login("your-email@example.com", "password");
Map<String, Object> user = client.auth().me();
System.out.println("Welcome, " + user.get("name"));
```

```go
// Go
auth, _ := client.Auth().Login("your-email@example.com", "password")
user, _ := client.Auth().Me()
fmt.Println("Welcome,", user["name"])
```

## Scanning Code

### Basic Code Scan

```python
# Python
result = client.scans().create_scan({
    "name": "My First Scan",
    "target": "https://example.com",
    "scan_type": "full"
})
print("Scan created:", result["id"])
```

```javascript
// JavaScript
const result = await client.scans().createScan({
  name: 'My First Scan',
  target: 'https://example.com',
  scanType: 'full'
});
console.log('Scan created:', result.id);
```

```java
// Java
Map<String, Object> scanData = Map.of(
    "name", "My First Scan",
    "target", "https://example.com",
    "scan_type", "full"
);
Map<String, Object> result = client.getScans().createScan(scanData);
System.out.println("Scan created: " + result.get("id"));
```

```go
// Go
scanData := map[string]interface{}{
    "name":      "My First Scan",
    "target":    "https://example.com",
    "scan_type": "full",
}
result, _ := client.Scans().CreateScan(scanData)
fmt.Println("Scan created:", result["id"])
```

### Get Scan Results

```python
# Python
scan_id = result["id"]
results = client.scans().get_scan_results(scan_id)
print("Vulnerabilities found:", len(results.get("vulnerabilities", [])))
```

```javascript
// JavaScript
const scanId = result.id;
const scanResults = await client.scans().getScanResults(scanId);
console.log('Vulnerabilities found:', scanResults.vulnerabilities?.length || 0);
```

```java
// Java
String scanId = (String) result.get("id");
Map<String, Object> scanResults = client.getScans().getScanResults(scanId, null);
List<?> vulnerabilities = (List<?>) scanResults.get("vulnerabilities");
System.out.println("Vulnerabilities found: " + (vulnerabilities != null ? vulnerabilities.size() : 0));
```

```go
// Go
scanId := result["id"].(string)
scanResults, _ := client.Scans().GetScanResults(scanId, nil)
vulnerabilities := scanResults["vulnerabilities"].([]interface{})
fmt.Println("Vulnerabilities found:", len(vulnerabilities))
```

## Working with Jobs

### Create and Monitor a Job

```python
# Python
job = client.jobs().create_job({
    "name": "Security Analysis",
    "type": "scan",
    "config": {"target": "https://myapp.com"}
})

# Check status
status = client.jobs().get_job_status(job["id"])
print("Job status:", status["status"])
```

```javascript
// JavaScript
const job = await client.jobs().createJob({
  name: 'Security Analysis',
  type: 'scan',
  config: { target: 'https://myapp.com' }
});

// Check status
const status = await client.jobs().getJobStatus(job.id);
console.log('Job status:', status.status);
```

```java
// Java
Map<String, Object> jobData = Map.of(
    "name", "Security Analysis",
    "type", "scan",
    "config", Map.of("target", "https://myapp.com")
);
Map<String, Object> job = client.getJobs().createJob(jobData);

// Check status
Map<String, Object> status = client.getJobs().getJobStatus(job.get("id").toString());
System.out.println("Job status: " + status.get("status"));
```

```go
// Go
jobData := map[string]interface{}{
    "name":   "Security Analysis",
    "type":   "scan",
    "config": map[string]interface{}{"target": "https://myapp.com"},
}
job, _ := client.Jobs().CreateJob(jobData)

// Check status
status, _ := client.Jobs().GetJobStatus(job["id"].(string))
fmt.Println("Job status:", status["status"])
```

## Generating Reports

```python
# Python
report = client.reports().generate_report({
    "type": "compliance",
    "format": "pdf",
    "filters": {"severity": "high"}
})
print("Report generated:", report["id"])
```

```javascript
// JavaScript
const report = await client.reports().generateReport({
  type: 'compliance',
  format: 'pdf',
  filters: { severity: 'high' }
});
console.log('Report generated:', report.id);
```

```java
// Java
Map<String, Object> reportData = Map.of(
    "type", "compliance",
    "format", "pdf",
    "filters", Map.of("severity", "high")
);
Map<String, Object> report = client.getReports().generateReport(reportData);
System.out.println("Report generated: " + report.get("id"));
```

```go
// Go
reportData := map[string]interface{}{
    "type":   "compliance",
    "format": "pdf",
    "filters": map[string]interface{}{"severity": "high"},
}
report, _ := client.Reports().GenerateReport(reportData)
fmt.Println("Report generated:", report["id"])
```

## Error Handling

All SDKs provide consistent error handling:

```python
# Python
try:
    result = client.scans().get_scan("invalid-id")
except Exception as e:
    print(f"Error: {e}")
```

```javascript
// JavaScript
try {
  const result = await client.scans().getScan('invalid-id');
} catch (error) {
  console.error('Error:', error.message);
}
```

```java
// Java
try {
    Map<String, Object> result = client.getScans().getScan("invalid-id");
} catch (TavoException e) {
    System.err.println("Error: " + e.getMessage());
}
```

```go
// Go
result, err := client.Scans().GetScan("invalid-id")
if err != nil {
    fmt.Println("Error:", err.Error())
}
```

## Next Steps

- Explore [Framework Examples](../examples/django) for your specific tech stack
- Check the [API Reference](../api-reference/overview) for detailed documentation
- Learn about [Advanced Features](../advanced/error-handling) for production use