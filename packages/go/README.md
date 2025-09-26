# Tavo Go SDK

A Go SDK for integrating with Tavo AI services.

## Installation

```bash
go get github.com/TavoAI/tavo-go-sdk
```

## Quick Start

```go
package main

import (
    "fmt"
    "log"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
    // Create configuration
    config := tavo.NewConfig().
        WithAPIKey("your-api-key-here").
        WithBaseURL("https://api.tavo.ai")

    // Create client
    client := tavo.NewClient(config)

    // Health check
    health, err := client.HealthCheck()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("Health: %+v\n", health)

    // Authenticate
    auth, err := client.Auth().Login("username", "password")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("Auth: %+v\n", auth)
}
```

## Configuration

The SDK can be configured using environment variables or the builder pattern:

```go
config := tavo.NewConfig().
    WithAPIKey("your-api-key").
    WithBaseURL("https://api.tavo.ai").
    WithTimeout(30 * time.Second).
    WithMaxRetries(3)
```

Environment variables:
- `TAVO_API_KEY`: Your API key
- `TAVO_BASE_URL`: API base URL (optional)
- `TAVO_API_VERSION`: API version (optional, defaults to "v1")

## API Operations

The SDK provides access to all Tavo API operations through dedicated operation clients:

### Authentication
```go
// Login
auth, err := client.Auth().Login("username", "password")

// Register new user
user, err := client.Auth().Register(map[string]interface{}{
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123",
})

// Get current user info
me, err := client.Auth().Me()
```

### Users
```go
// Get current user
user, err := client.Users().GetCurrentUser()

// Update profile
updated, err := client.Users().UpdateProfile(map[string]interface{}{
    "name": "New Name",
    "email": "new@example.com",
})

// List users (admin)
users, err := client.Users().ListUsers(map[string]interface{}{
    "limit": 10,
    "offset": 0,
})
```

### Organizations
```go
// List organizations
orgs, err := client.Organizations().ListOrganizations(nil)

// Get specific organization
org, err := client.Organizations().GetOrganization("org-id")

// Create organization
newOrg, err := client.Organizations().CreateOrganization(map[string]interface{}{
    "name": "My Organization",
    "description": "Description",
})
```

### Scans
```go
// List scans
scans, err := client.Scans().ListScans(map[string]interface{}{
    "status": "completed",
    "limit": 20,
})

// Create scan
scan, err := client.Scans().CreateScan(map[string]interface{}{
    "name": "My Scan",
    "target": "https://example.com",
    "scan_type": "full",
})

// Get scan results
results, err := client.Scans().GetScanResults("scan-id", nil)
```

### Jobs
```go
// List jobs
jobs, err := client.Jobs().ListJobs(map[string]interface{}{
    "status": "running",
})

// Create job
job, err := client.Jobs().CreateJob(map[string]interface{}{
    "name": "My Job",
    "type": "scan",
    "config": map[string]interface{}{},
})

// Start job
started, err := client.Jobs().StartJob("job-id")
```

### AI Analysis
```go
// Analyze code
analysis, err := client.AIAnalysis().AnalyzeCode(map[string]interface{}{
    "code": "def hello(): print('world')",
    "language": "python",
})

// Get analysis results
results, err := client.AIAnalysis().GetAnalysisResults("analysis-id")
```

### Webhooks
```go
// List webhooks
webhooks, err := client.Webhooks().ListWebhooks(nil)

// Create webhook
webhook, err := client.Webhooks().CreateWebhook(map[string]interface{}{
    "url": "https://example.com/webhook",
    "events": []string{"scan.completed", "job.finished"},
})
```

### Billing
```go
// Get usage
usage, err := client.Billing().GetUsage()

// Get invoices
invoices, err := client.Billing().GetInvoices(map[string]interface{}{
    "limit": 10,
})
```

### Reports
```go
// Generate report
report, err := client.Reports().GenerateReport(map[string]interface{}{
    "type": "security",
    "format": "pdf",
    "filters": map[string]interface{}{},
})

// Get report
reportData, err := client.Reports().GetReport("report-id")
```

### Scan Rules
```go
// List rules
rules, err := client.ScanRules().ListRules(map[string]interface{}{
    "enabled": true,
})

// Create rule
rule, err := client.ScanRules().CreateRule(map[string]interface{}{
    "name": "Custom Rule",
    "pattern": ".*",
    "severity": "high",
})
```

## Error Handling

All API methods return errors that should be handled:

```go
result, err := client.Scans().GetScan("scan-id")
if err != nil {
    if tavoErr, ok := err.(*tavo.TavoError); ok {
        fmt.Printf("API Error (%d): %s\n", tavoErr.StatusCode, tavoErr.Message)
    } else {
        fmt.Printf("Network Error: %v\n", err)
    }
    return
}
```

## Requirements

- Go 1.25 or higher

## Dependencies

- `github.com/go-resty/resty/v2`: HTTP client library

## Testing

```bash
go test ./...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run tests: `go test ./...`
6. Submit a pull request