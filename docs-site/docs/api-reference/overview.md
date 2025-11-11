# API Reference

The Tavo AI API provides comprehensive security scanning and AI model analysis capabilities through multiple SDKs and direct REST API access.

:::info Auto-Generated Documentation
This API reference is automatically generated from the live OpenAPI specification of the Tavo AI API server. The documentation reflects the current state of the API and is updated with each deployment.
:::

## SDKs Overview

### Authentication Methods

All SDKs support multiple authentication methods:

```javascript
// API Key (recommended)
const client = new TavoClient({ apiKey: 'your-api-key' });

// JWT Token
const client = new TavoClient({ jwtToken: 'your-jwt-token' });

// Session Token
const client = new TavoClient({ sessionToken: 'your-session-token' });
```

### Error Handling

All SDKs provide consistent error handling:

```javascript
try {
  const result = await client.scans().getScan('invalid-id');
} catch (error) {
  if (error.code === 'NOT_FOUND') {
    console.log('Scan not found');
  } else if (error.code === 'UNAUTHORIZED') {
    console.log('Authentication required');
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

## REST API

For direct API integration, use the REST endpoints:

```text
Base URL: https://api.tavoai.net/api/v1
```

### Authentication Headers

```bash
# API Key
X-API-Key: your-api-key

# JWT Token
Authorization: Bearer your-jwt-token

# Session Token
X-Session-Token: your-session-token
```

## Core Endpoints

### Health Check

```http
GET /health
```

Check API availability and version information.

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Authentication Endpoints

```http
POST /auth/login
POST /auth/logout
GET /auth/me
```

### Code Scanning Endpoints

```http
POST /scans
GET /scans/{id}
GET /scans/{id}/results
POST /scans/{id}/cancel
```

### AI Model Analysis Endpoints

```http
POST /ai/analyze
GET /ai/models/{id}
GET /ai/models/{id}/analysis
```

### User Management Endpoints

```http
GET /users/me
PUT /users/me
GET /users/me/api-keys
POST /users/me/api-keys
PUT /users/me/api-keys/{id}
DELETE /users/me/api-keys/{id}
```

### Organization Management Endpoints

```http
GET /organizations
POST /organizations
GET /organizations/{id}
PUT /organizations/{id}
DELETE /organizations/{id}
```

### Job Management Endpoints

```http
POST /jobs
GET /jobs/{id}
GET /jobs/{id}/status
POST /jobs/{id}/cancel
GET /jobs
```

### Webhook Endpoints

```http
POST /webhooks
GET /webhooks
GET /webhooks/{id}
PUT /webhooks/{id}
DELETE /webhooks/{id}
GET /webhooks/{id}/deliveries
```

### Report Endpoints

```http
POST /reports
GET /reports/{id}
GET /reports/{id}/download
GET /reports
PUT /reports/{id}
DELETE /reports/{id}
```

## Data Types

### Scan Result

```typescript
interface ScanResult {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  target: string;
  scanType: string;
  createdAt: string;
  completedAt?: string;
  vulnerabilities: Vulnerability[];
  summary: {
    totalFiles: number;
    scannedFiles: number;
    totalVulnerabilities: number;
    bySeverity: Record<string, number>;
    byCategory: Record<string, number>;
  };
}
```

### Vulnerability

```typescript
interface Vulnerability {
  id: string;
  ruleId: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';
  category: string;
  cwe: string;
  message: string;
  file: string;
  line: number;
  column: number;
  code: string;
  confidence: number;
  evidence: Record<string, any>;
}
```

### AI Model Analysis Result

```typescript
interface ModelAnalysis {
  safe: boolean;
  risks: string[];
  recommendations: Record<string, any>;
  confidence: number;
  analysis: {
    modelType: string;
    parameters: Record<string, any>;
    securityScore: number;
  };
}
```

### User

```typescript
interface User {
  id: string;
  email: string;
  name?: string;
  role: string;
  organizationId?: string;
  createdAt: string;
  updatedAt: string;
}
```

### Organization

```typescript
interface Organization {
  id: string;
  name: string;
  description?: string;
  ownerId: string;
  members: User[];
  createdAt: string;
  updatedAt: string;
}
```

### Job

```typescript
interface Job {
  id: string;
  type: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  config: Record<string, any>;
  result?: Record<string, any>;
  createdAt: string;
  startedAt?: string;
  completedAt?: string;
}
```

### Webhook

```typescript
interface Webhook {
  id: string;
  url: string;
  events: string[];
  secret?: string;
  active: boolean;
  createdAt: string;
  updatedAt: string;
}
```

### Report

```typescript
interface Report {
  id: string;
  type: string;
  format: string;
  status: 'generating' | 'completed' | 'failed';
  title: string;
  filters?: Record<string, any>;
  createdAt: string;
  completedAt?: string;
  downloadUrl?: string;
}
```

## Rate Limits

- **Free Tier**: 100 requests/hour, 1000 requests/day
- **Pro Tier**: 1000 requests/hour, 10000 requests/day
- **Enterprise Tier**: Custom limits

Rate limit headers are included in all responses:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Error Codes

| Code  | Description                                    |
| ----- | ---------------------------------------------- |
| `400` | Bad Request - Invalid parameters               |
| `401` | Unauthorized - Authentication required         |
| `403` | Forbidden - Insufficient permissions           |
| `404` | Not Found - Resource doesn't exist             |
| `429` | Too Many Requests - Rate limit exceeded        |
| `500` | Internal Server Error - Server error           |
| `502` | Bad Gateway - Upstream service error           |
| `503` | Service Unavailable - Service temporarily down |

## SDK Examples

### Python

```python
from tavo_ai import TavoClient

client = TavoClient(api_key="your-api-key")

# Scan code
result = await client.scan_code("print('hello')", language="python")
print(f"Found {result.total_issues} issues")
```

### JavaScript

```javascript
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient({ apiKey: 'your-api-key' });

// Scan code
const result = await client.scans().scanCode("console.log('hello')", 'javascript');
console.log(`Found ${result.totalIssues} issues`);
```

### Java

```java
import net.tavoai.TavoClient;

TavoClient client = new TavoClient("your-api-key");

// Scan code
ScanResult result = client.getScans().scanCode("System.out.println(\"hello\")", "java");
System.out.println("Found " + result.getTotalIssues() + " issues");
```

### Go

```go
package main

import (
    "fmt"
    "github.com/tavoai/tavo-go-sdk/tavo"
)

func main() {
    client := tavo.NewClient(&tavo.Config{APIKey: "your-api-key"})

    result, err := client.Scans().ScanCode("fmt.Println(\"hello\")", "go")
    if err != nil {
        panic(err)
    }

    fmt.Printf("Found %d issues\n", result.TotalIssues)
}
```

### .NET

```csharp
using TavoAI;

var client = new TavoClient("your-api-key");

// Scan code
var result = await client.Scans.ScanCodeAsync("Console.WriteLine(\"hello\")", "csharp");
Console.WriteLine($"Found {result.TotalIssues} issues");
```

### Rust

```rust
use tavo_ai::TavoClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = TavoClient::new("your-api-key")?;

    let result = client.scans().scan_code("println!(\"hello\")", "rust").await?;
    println!("Found {} issues", result.total_issues);

    Ok(())
}
```

## Next Steps

- [SDK Installation Guides](../sdks/)
- [Authentication Guide](../getting-started/authentication.md)
- [Error Handling Guide](../advanced/error-handling.md)
- [Integration Examples](../examples/)
