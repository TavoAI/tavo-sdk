# Go SDK

The Tavo AI Go SDK provides a idiomatic, performant interface for integrating with the Tavo AI platform. Built with Go's concurrency patterns and comprehensive error handling.

## Installation

```bash
go get github.com/TavoAI/tavo-go-sdk
```

## Quick Start

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
    // Initialize the client
    client, err := tavo.NewClient("your-api-key")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    // Scan code for vulnerabilities
    code := `
        func processUserInput(userInput string) {
            query := fmt.Sprintf("SELECT * FROM users WHERE id = '%s'", userInput)
            // Potential SQL injection vulnerability
            executeQuery(query)
        }
    `

    result, err := client.ScanCode(context.Background(), code, "go")
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Found %d issues\n", result.TotalIssues)
    for _, vuln := range result.Vulnerabilities {
        fmt.Printf("- %s: %s\n", vuln.Title, vuln.Description)
    }
}
```

## Client Configuration

```go
// Basic client
client, err := tavo.NewClient("your-api-key")

// With custom options
client, err := tavo.NewClientWithOptions(&tavo.ClientOptions{
    APIKey:      "your-api-key",
    BaseURL:     "https://api-staging.tavoai.net",
    Timeout:     30 * time.Second,
    MaxRetries:  3,
    RetryDelay:  time.Second,
})
```

## Core Operations

### Code Scanning

```go
// Basic code scan
result, err := client.ScanCode(ctx, code, "go")
if err != nil {
    log.Fatal(err)
}

// Advanced scan with options
result, err := client.ScanCodeWithOptions(ctx, &tavo.ScanOptions{
    Code:         code,
    Language:     "go",
    Timeout:      60 * time.Second,
    IncludeMetrics: true,
})
```

### AI Model Analysis

```go
modelConfig := map[string]interface{}{
    "model_type": "transformer",
    "parameters": map[string]interface{}{
        "layers":     12,
        "heads":      8,
        "hidden_size": 768,
    },
}

analysis, err := client.AnalyzeModel(ctx, modelConfig)
if err != nil {
    log.Fatal(err)
}

fmt.Printf("Model is safe: %t\n", analysis.Safe)
```

### User Management

```go
// Get current user
user, err := client.GetCurrentUser(ctx)
if err != nil {
    log.Fatal(err)
}

// Update user profile
updates := map[string]interface{}{
    "name":  "New Name",
    "email": "new@example.com",
}

updatedUser, err := client.UpdateUser(ctx, user.ID, updates)
if err != nil {
    log.Fatal(err)
}

// API Key Management
apiKeys, err := client.ListAPIKeys(ctx)
if err != nil {
    log.Fatal(err)
}

// Update API key
updatedKey, err := client.UpdateAPIKey(ctx, apiKeyID, map[string]interface{}{
    "name":        "Updated API Key Name",
    "description": "Updated description",
})
if err != nil {
    log.Fatal(err)
}

// Rotate API key (generates new secret)
rotatedKey, err := client.RotateAPIKey(ctx, apiKeyID)
if err != nil {
    log.Fatal(err)
}

// Delete API key
err = client.DeleteAPIKey(ctx, apiKeyID)
if err != nil {
    log.Fatal(err)
}
```

### Organization Management

```go
// List organizations
orgs, err := client.ListOrganizations(ctx)
if err != nil {
    log.Fatal(err)
}

// Create new organization
newOrg, err := client.CreateOrganization(ctx, map[string]interface{}{
    "name":        "My Company",
    "description": "Security scanning service",
})
if err != nil {
    log.Fatal(err)
}
```

### Scan Jobs

```go
// Start a new scan job
job, err := client.CreateScanJob(ctx, map[string]interface{}{
    "target_url": "https://example.com",
    "scan_type":  "full_scan",
})
if err != nil {
    log.Fatal(err)
}

// Get job status
status, err := client.GetScanJob(ctx, job.ID)
if err != nil {
    log.Fatal(err)
}

// List all jobs with pagination
jobs, err := client.ListScanJobs(ctx, &tavo.ListOptions{
    Limit:  10,
    Offset: 0,
})
if err != nil {
    log.Fatal(err)
}
```

### Webhooks

```go
// Create webhook
webhook, err := client.CreateWebhook(ctx, &tavo.WebhookConfig{
    URL:    "https://myapp.com/webhook",
    Events: []string{"scan.completed", "vulnerability.found"},
})
if err != nil {
    log.Fatal(err)
}

// List webhooks
webhooks, err := client.ListWebhooks(ctx)
if err != nil {
    log.Fatal(err)
}

// Delete webhook
err = client.DeleteWebhook(ctx, webhook.ID)
if err != nil {
    log.Fatal(err)
}
```

### Billing & Reports

```go
// Get billing information
billing, err := client.GetBillingInfo(ctx)
if err != nil {
    log.Fatal(err)
}

// Generate report
report, err := client.GenerateReport(ctx, &tavo.ReportConfig{
    Type: "security_audit",
    DateRange: &tavo.DateRange{
        Start: "2024-01-01",
        End:   "2024-01-31",
    },
})
if err != nil {
    log.Fatal(err)
}

// Get report summary statistics
summary, err := client.GetReportSummary(ctx)
if err != nil {
    log.Fatal(err)
}

fmt.Printf("Total scans: %d\n", summary.TotalScans)
fmt.Printf("Total vulnerabilities: %d\n", summary.TotalVulnerabilities)
fmt.Printf("Critical issues: %d\n", summary.CriticalIssues)
```

## Error Handling

The SDK provides structured error handling:

```go
import "github.com/TavoAI/tavo-go-sdk/tavo"

result, err := client.ScanCode(ctx, code, "go")
if err != nil {
    switch e := err.(type) {
    case *tavo.AuthError:
        log.Printf("Authentication failed: %s", e.Message)
    case *tavo.APIError:
        log.Printf("API error: %s (status: %d)", e.Message, e.StatusCode)
    case *tavo.RateLimitError:
        log.Printf("Rate limit exceeded, retry after: %v", e.RetryAfter)
    case *tavo.ValidationError:
        log.Printf("Validation error: %s", e.Message)
        for field, messages := range e.FieldErrors {
            log.Printf("  %s: %v", field, messages)
        }
    default:
        log.Printf("Unknown error: %s", err)
    }
    return
}
```

## Context and Cancellation

The SDK supports Go's context package for cancellation and timeouts:

```go
// With timeout
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

result, err := client.ScanCode(ctx, code, "go")
if err != nil {
    if ctx.Err() == context.DeadlineExceeded {
        log.Println("Scan timed out")
    } else {
        log.Printf("Scan failed: %s", err)
    }
}
```

## Advanced Usage

### Concurrent Scanning

```go
func scanMultipleFiles(ctx context.Context, client *tavo.Client, files []string) error {
    var wg sync.WaitGroup
    errChan := make(chan error, len(files))

    for _, file := range files {
        wg.Add(1)
        go func(filename string) {
            defer wg.Done()

            code, err := ioutil.ReadFile(filename)
            if err != nil {
                errChan <- fmt.Errorf("failed to read %s: %w", filename, err)
                return
            }

            result, err := client.ScanCode(ctx, string(code), "go")
            if err != nil {
                errChan <- fmt.Errorf("failed to scan %s: %w", filename, err)
                return
            }

            fmt.Printf("%s: %d issues found\n", filename, result.TotalIssues)
        }(file)
    }

    wg.Wait()
    close(errChan)

    // Collect any errors
    var errors []error
    for err := range errChan {
        errors = append(errors, err)
    }

    if len(errors) > 0 {
        return fmt.Errorf("multiple errors occurred: %v", errors)
    }

    return nil
}
```

### Streaming Results

```go
// For large codebases, process results as they come
scanner := client.NewScanner(ctx)

go func() {
    for result := range scanner.Results() {
        fmt.Printf("Scanned %s: %d issues\n", result.FileName, result.TotalIssues)
    }
}()

go func() {
    for err := range scanner.Errors() {
        log.Printf("Scan error: %s", err)
    }
}()

// Start scanning multiple files
files := []string{"file1.go", "file2.go", "file3.go"}
if err := scanner.ScanFiles(files); err != nil {
    log.Fatal(err)
}

// Wait for completion
scanner.Wait()
```

### Custom HTTP Client

```go
// Use custom HTTP client
httpClient := &http.Client{
    Timeout: 30 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
    },
}

client, err := tavo.NewClientWithHTTPClient("your-api-key", httpClient)
```

### Middleware and Hooks

```go
// Add request/response hooks
client.AddRequestHook(func(req *http.Request) error {
    req.Header.Set("X-Custom-Header", "value")
    log.Printf("Making request to: %s", req.URL)
    return nil
})

client.AddResponseHook(func(resp *http.Response, duration time.Duration) error {
    log.Printf("Response received in %v", duration)
    return nil
})
```

## Integration Examples

### Gin Web Framework

```go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
    client, err := tavo.NewClient("your-api-key")
    if err != nil {
        panic(err)
    }
    defer client.Close()

    r := gin.Default()

    r.POST("/scan", func(c *gin.Context) {
        var req struct {
            Code     string `json:"code" binding:"required"`
            Language string `json:"language"`
        }

        if err := c.ShouldBindJSON(&req); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        if req.Language == "" {
            req.Language = "go"
        }

        result, err := client.ScanCode(c.Request.Context(), req.Code, req.Language)
        if err != nil {
            c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
            return
        }

        c.JSON(http.StatusOK, gin.H{
            "total_issues": result.TotalIssues,
            "vulnerabilities": result.Vulnerabilities,
        })
    })

    r.Run(":8080")
}
```

### CLI Tool

```go
package main

import (
    "bufio"
    "context"
    "flag"
    "fmt"
    "os"
    "strings"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
    apiKey := flag.String("api-key", "", "Tavo AI API key")
    language := flag.String("lang", "go", "Programming language")
    file := flag.String("file", "", "File to scan")
    flag.Parse()

    if *apiKey == "" {
        *apiKey = os.Getenv("TAVO_API_KEY")
    }
    if *apiKey == "" {
        fmt.Println("API key required. Use -api-key or set TAVO_API_KEY environment variable")
        os.Exit(1)
    }

    client, err := tavo.NewClient(*apiKey)
    if err != nil {
        fmt.Printf("Failed to create client: %s\n", err)
        os.Exit(1)
    }
    defer client.Close()

    var code string
    if *file != "" {
        content, err := os.ReadFile(*file)
        if err != nil {
            fmt.Printf("Failed to read file: %s\n", err)
            os.Exit(1)
        }
        code = string(content)
    } else {
        fmt.Println("Enter code to scan (press Ctrl+D when done):")
        scanner := bufio.NewScanner(os.Stdin)
        var lines []string
        for scanner.Scan() {
            lines = append(lines, scanner.Text())
        }
        code = strings.Join(lines, "\n")
    }

    result, err := client.ScanCode(context.Background(), code, *language)
    if err != nil {
        fmt.Printf("Scan failed: %s\n", err)
        os.Exit(1)
    }

    fmt.Printf("Found %d issues:\n", result.TotalIssues)
    for i, vuln := range result.Vulnerabilities {
        fmt.Printf("%d. %s (%s)\n", i+1, vuln.Title, vuln.Severity)
        fmt.Printf("   %s\n", vuln.Description)
        if vuln.Location != nil {
            fmt.Printf("   Location: %s:%d:%d\n",
                vuln.Location.File, vuln.Location.Line, vuln.Location.Column)
        }
    }
}
```

### Testing with Go

```go
package main

import (
    "context"
    "testing"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func TestScanCode(t *testing.T) {
    client, err := tavo.NewClient("test-api-key")
    if err != nil {
        t.Fatal(err)
    }
    defer client.Close()

    // Use a mock server for testing
    // client.SetBaseURL("http://localhost:8080")

    code := `package main

func main() {
    userInput := "'; DROP TABLE users; --"
    query := "SELECT * FROM users WHERE id = '" + userInput + "'"
    // SQL injection vulnerability
}`

    result, err := client.ScanCode(context.Background(), code, "go")
    if err != nil {
        t.Fatal(err)
    }

    if result.TotalIssues == 0 {
        t.Error("Expected to find SQL injection vulnerability")
    }

    // Check for specific vulnerability
    found := false
    for _, vuln := range result.Vulnerabilities {
        if strings.Contains(vuln.Title, "SQL Injection") {
            found = true
            break
        }
    }

    if !found {
        t.Error("Expected SQL injection vulnerability not found")
    }
}
```

## Best Practices

1. **Context Usage**: Always pass context for cancellation and timeouts
2. **Error Handling**: Check for specific error types, not just generic errors
3. **Resource Management**: Always close clients when done
4. **Concurrency**: Use goroutines for concurrent operations
5. **Timeouts**: Set appropriate timeouts for your use case
6. **Rate Limiting**: Implement proper rate limiting and backoff strategies

## Performance Considerations

- **Connection Reuse**: The SDK automatically reuses HTTP connections
- **Concurrent Operations**: Use goroutines for parallel scanning
- **Streaming**: Use streaming APIs for large datasets
- **Timeouts**: Set reasonable timeouts to prevent hanging operations
