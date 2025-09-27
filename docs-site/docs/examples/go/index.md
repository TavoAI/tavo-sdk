# Go SDK Examples

This directory contains comprehensive examples for using the Tavo AI Go SDK.

## Installation

```bash
go get github.com/TavoAI/tavo-go-sdk
```

## Basic Usage

### Simple Code Scan

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
    // Initialize client
    client, err := tavo.NewClient("your-api-key")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    // Code to scan
    code := `
        func processUserInput(userInput string) {
            query := fmt.Sprintf("SELECT * FROM users WHERE id = '%s'", userInput)
            // Potential SQL injection vulnerability
            executeQuery(query)
        }
    `

    // Scan the code
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

### Configuration and Error Handling

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
    // Configure client
    client, err := tavo.NewClientWithOptions(&tavo.ClientOptions{
        APIKey:      "your-api-key",
        BaseURL:     "https://api.tavoai.net",
        Timeout:     30 * time.Second,
        MaxRetries:  3,
        RetryDelay:  time.Second,
    })
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    code := "fmt.Println(\"hello\")"

    result, err := client.ScanCode(context.Background(), code, "go")
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

    fmt.Printf("Scan successful: %d issues\n", result.TotalIssues)
}
```

## Advanced Examples

### Concurrent Batch Scanning

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"
    "path/filepath"
    "sync"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

type ScanResult struct {
    FilePath string
    Issues   int
    Error    error
}

func scanDirectory(ctx context.Context, client *tavo.Client, dirPath string, maxConcurrency int) error {
    // Find all Go files
    goFiles, err := findGoFiles(dirPath)
    if err != nil {
        return fmt.Errorf("failed to find Go files: %w", err)
    }

    // Create channels for work and results
    fileChan := make(chan string, len(goFiles))
    resultChan := make(chan ScanResult, len(goFiles))

    // Fill work channel
    for _, file := range goFiles {
        fileChan <- file
    }
    close(fileChan)

    // Start workers
    var wg sync.WaitGroup
    for i := 0; i < maxConcurrency; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            worker(ctx, client, fileChan, resultChan)
        }()
    }

    // Close result channel when all workers are done
    go func() {
        wg.Wait()
        close(resultChan)
    }()

    // Collect results
    totalIssues := 0
    totalFiles := 0
    for result := range resultChan {
        if result.Error != nil {
            log.Printf("Error scanning %s: %v", result.FilePath, result.Error)
            continue
        }

        totalFiles++
        totalIssues += result.Issues
        fmt.Printf("%s: %d issues\n", result.FilePath, result.Issues)
    }

    fmt.Printf("\nScanned %d files, found %d total issues\n", totalFiles, totalIssues)
    return nil
}

func worker(ctx context.Context, client *tavo.Client, files <-chan string, results chan<- ScanResult) {
    for filePath := range files {
        result := ScanResult{FilePath: filePath}

        code, err := os.ReadFile(filePath)
        if err != nil {
            result.Error = fmt.Errorf("failed to read file: %w", err)
            results <- result
            continue
        }

        scanResult, err := client.ScanCode(ctx, string(code), "go")
        if err != nil {
            result.Error = fmt.Errorf("failed to scan: %w", err)
            results <- result
            continue
        }

        result.Issues = scanResult.TotalIssues
        results <- result
    }
}

func findGoFiles(dirPath string) ([]string, error) {
    var files []string

    err := filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
        if err != nil {
            return err
        }

        if !info.IsDir() && filepath.Ext(path) == ".go" {
            files = append(files, path)
        }

        return nil
    })

    return files, err
}

func main() {
    client, err := tavo.NewClient("your-api-key")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    ctx := context.Background()

    if err := scanDirectory(ctx, client, "./", 5); err != nil {
        log.Fatal(err)
    }
}
```

### AI Model Analysis

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func analyzeModel() error {
    client, err := tavo.NewClient("your-api-key")
    if err != nil {
        return err
    }
    defer client.Close()

    modelConfig := map[string]interface{}{
        "model_type": "transformer",
        "architecture": map[string]interface{}{
            "layers":        12,
            "attention_heads": 8,
            "hidden_size":   768,
            "vocab_size":    30000,
        },
        "training": map[string]interface{}{
            "dataset":       "wikipedia",
            "epochs":        10,
            "learning_rate": 0.0001,
        },
    }

    analysis, err := client.AnalyzeModel(context.Background(), modelConfig)
    if err != nil {
        return err
    }

    fmt.Printf("Model safety: %t\n", analysis.Safe)

    if !analysis.Safe {
        fmt.Println("Issues found:")
        for _, issue := range analysis.Issues {
            fmt.Printf("- %s: %s\n", issue.Title, issue.Description)
        }
    }

    return nil
}

func main() {
    if err := analyzeModel(); err != nil {
        log.Fatal(err)
    }
}
```

### Webhook Management

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func manageWebhooks() error {
    client, err := tavo.NewClient("your-api-key")
    if err != nil {
        return err
    }
    defer client.Close()

    ctx := context.Background()

    // Create a webhook
    webhook, err := client.CreateWebhook(ctx, &tavo.WebhookConfig{
        URL:    "https://myapp.com/webhook/scan-complete",
        Events: []string{"scan.completed", "vulnerability.found"},
        Secret: "webhook-secret",
    })
    if err != nil {
        return err
    }

    fmt.Printf("Created webhook: %s\n", webhook.ID)

    // List all webhooks
    webhooks, err := client.ListWebhooks(ctx)
    if err != nil {
        return err
    }

    fmt.Printf("Total webhooks: %d\n", len(webhooks))
    for _, wh := range webhooks {
        fmt.Printf("- %s: %s (%v)\n", wh.ID, wh.URL, wh.Events)
    }

    // Update webhook
    err = client.UpdateWebhook(ctx, webhook.ID, &tavo.WebhookConfig{
        Events: []string{"scan.completed", "vulnerability.found", "scan.failed"},
    })
    if err != nil {
        return err
    }

    fmt.Println("Webhook updated")

    // Delete the webhook
    err = client.DeleteWebhook(ctx, webhook.ID)
    if err != nil {
        return err
    }

    fmt.Println("Webhook deleted")
    return nil
}

func main() {
    if err := manageWebhooks(); err != nil {
        log.Fatal(err)
    }
}
```

## Integration Examples

### Gin Web Framework

```go
package main

import (
    "net/http"
    "time"

    "github.com/gin-gonic/gin"
    "github.com/TavoAI/tavo-go-sdk/tavo"
)

type ScanRequest struct {
    Code     string `json:"code" binding:"required"`
    Language string `json:"language"`
}

type ScanResponse struct {
    TotalIssues     int                      `json:"total_issues"`
    Vulnerabilities []tavo.Vulnerability `json:"vulnerabilities"`
    ScanID          string                  `json:"scan_id,omitempty"`
}

func main() {
    // Initialize Tavo client
    client, err := tavo.NewClientWithOptions(&tavo.ClientOptions{
        APIKey:     "your-api-key",
        Timeout:    60 * time.Second,
        MaxRetries: 3,
    })
    if err != nil {
        panic(err)
    }
    defer client.Close()

    r := gin.Default()

    // Add CORS middleware
    r.Use(func(c *gin.Context) {
        c.Header("Access-Control-Allow-Origin", "*")
        c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        c.Header("Access-Control-Allow-Headers", "Origin, Content-Type, Accept, Authorization")

        if c.Request.Method == "OPTIONS" {
            c.AbortWithStatus(204)
            return
        }

        c.Next()
    })

    // Health check
    r.GET("/health", func(c *gin.Context) {
        c.JSON(200, gin.H{"status": "healthy"})
    })

    // Scan endpoint
    r.POST("/api/scan", func(c *gin.Context) {
        var req ScanRequest
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

        response := ScanResponse{
            TotalIssues:     result.TotalIssues,
            Vulnerabilities: result.Vulnerabilities,
            ScanID:          result.ScanID,
        }

        c.JSON(http.StatusOK, response)
    })

    // Async scan endpoint
    r.POST("/api/scan/async", func(c *gin.Context) {
        var req ScanRequest
        if err := c.ShouldBindJSON(&req); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        if req.Language == "" {
            req.Language = "go"
        }

        scanID := fmt.Sprintf("scan_%d_%s", time.Now().Unix(), randomString(8))

        // Start async scan
        go func() {
            result, err := client.ScanCode(context.Background(), req.Code, req.Language)
            if err != nil {
                log.Printf("Async scan %s failed: %v", scanID, err)
                return
            }

            log.Printf("Async scan %s completed: %d issues", scanID, result.TotalIssues)

            // Here you would typically send results to a webhook or store in database
            // For demo purposes, we'll just log
        }()

        c.JSON(http.StatusAccepted, gin.H{
            "scan_id": scanID,
            "status":  "processing",
            "message": "Scan started. Results will be available via webhook.",
        })
    })

    r.Run(":8080")
}

func randomString(length int) string {
    // Simple random string generator for demo
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    b := make([]byte, length)
    for i := range b {
        b[i] = charset[time.Now().UnixNano()%int64(len(charset))]
    }
    return string(b)
}
```

### CLI Tool with Cobra

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"
    "path/filepath"
    "strings"

    "github.com/spf13/cobra"
    "github.com/TavoAI/tavo-go-sdk/tavo"
)

var (
    apiKey     string
    language   string
    recursive  bool
    verbose    bool
    client     *tavo.Client
)

var rootCmd = &cobra.Command{
    Use:   "tavo-scanner",
    Short: "Tavo AI Security Scanner CLI",
    Long:  `A command-line tool for scanning code for security vulnerabilities using Tavo AI.`,
    PersistentPreRun: func(cmd *cobra.Command, args []string) {
        // Initialize client
        key := apiKey
        if key == "" {
            key = os.Getenv("TAVO_API_KEY")
        }
        if key == "" {
            log.Fatal("API key required. Use --api-key or set TAVO_API_KEY environment variable")
        }

        var err error
        client, err = tavo.NewClient(key)
        if err != nil {
            log.Fatal(err)
        }
    },
    PersistentPostRun: func(cmd *cobra.Command, args []string) {
        if client != nil {
            client.Close()
        }
    },
}

var scanCmd = &cobra.Command{
    Use:   "scan [path]",
    Short: "Scan a file or directory for security vulnerabilities",
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        path := args[0]

        stat, err := os.Stat(path)
        if err != nil {
            log.Fatal(err)
        }

        ctx := context.Background()

        if stat.IsDir() {
            issues, err := scanDirectory(ctx, path)
            if err != nil {
                log.Fatal(err)
            }
            os.Exit(exitCode(issues))
        } else {
            issues, err := scanFile(ctx, path)
            if err != nil {
                log.Fatal(err)
            }
            os.Exit(exitCode(issues))
        }
    },
}

func scanFile(ctx context.Context, filePath string) (int, error) {
    code, err := os.ReadFile(filePath)
    if err != nil {
        return 0, fmt.Errorf("failed to read file: %w", err)
    }

    result, err := client.ScanCode(ctx, string(code), language)
    if err != nil {
        return 0, fmt.Errorf("failed to scan: %w", err)
    }

    printScanResult(filePath, result)
    return result.TotalIssues, nil
}

func scanDirectory(ctx context.Context, dirPath string) (int, error) {
    files, err := findFilesToScan(dirPath, language, recursive)
    if err != nil {
        return 0, fmt.Errorf("failed to find files: %w", err)
    }

    if len(files) == 0 {
        fmt.Println("No files found to scan")
        return 0, nil
    }

    fmt.Printf("Scanning %d files...\n", len(files))

    totalIssues := 0
    for _, file := range files {
        issues, err := scanFile(ctx, file)
        if err != nil {
            log.Printf("Error scanning %s: %v", file, err)
            continue
        }
        totalIssues += issues
    }

    fmt.Printf("\n📊 Summary: %d total issues\n", totalIssues)
    return totalIssues, nil
}

func findFilesToScan(dirPath, language string, recursive bool) ([]string, error) {
    var files []string
    extension := getExtensionForLanguage(language)

    walkFn := func(path string, info os.FileInfo, err error) error {
        if err != nil {
            return err
        }

        if info.IsDir() && !recursive && path != dirPath {
            return filepath.SkipDir
        }

        if !info.IsDir() && strings.HasSuffix(path, extension) {
            files = append(files, path)
        }

        return nil
    }

    err := filepath.Walk(dirPath, walkFn)
    return files, err
}

func getExtensionForLanguage(language string) string {
    switch strings.ToLower(language) {
    case "go":
        return ".go"
    case "python":
        return ".py"
    case "javascript":
        return ".js"
    case "typescript":
        return ".ts"
    case "java":
        return ".java"
    case "rust":
        return ".rs"
    case "csharp":
        return ".cs"
    default:
        return ".go"
    }
}

func printScanResult(filePath string, result *tavo.ScanResult) {
    if result.TotalIssues > 0 {
        fmt.Printf("\n🔴 %s (%d issues):\n", filePath, result.TotalIssues)

        for i, vuln := range result.Vulnerabilities {
            fmt.Printf("  %d. %s (%s)\n", i+1, vuln.Title, vuln.Severity)
            if verbose {
                fmt.Printf("     %s\n", vuln.Description)
                if vuln.Location != nil {
                    fmt.Printf("     📍 %s:%d:%d\n",
                        vuln.Location.File, vuln.Location.Line, vuln.Location.Column)
                }
            }
        }
    } else {
        fmt.Printf("✅ %s (0 issues)\n", filePath)
    }
}

func exitCode(issues int) int {
    if issues > 0 {
        return 1
    }
    return 0
}

func init() {
    rootCmd.PersistentFlags().StringVarP(&apiKey, "api-key", "k", "", "Tavo AI API key")
    rootCmd.PersistentFlags().StringVarP(&language, "language", "l", "go", "Programming language")
    rootCmd.PersistentFlags().BoolVarP(&recursive, "recursive", "r", false, "Scan directories recursively")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "Verbose output")

    rootCmd.AddCommand(scanCmd)
}

func main() {
    if err := rootCmd.Execute(); err != nil {
        log.Fatal(err)
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

    code := `
        func processUserInput(userInput string) {
            query := fmt.Sprintf("SELECT * FROM users WHERE id = '%s'", userInput)
            // SQL injection vulnerability
            executeQuery(query)
        }
    `

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

func TestScanCodeWithTimeout(t *testing.T) {
    client, err := tavo.NewClient("test-api-key")
    if err != nil {
        t.Fatal(err)
    }
    defer client.Close()

    ctx, cancel := context.WithTimeout(context.Background(), 1*time.Millisecond)
    defer cancel()

    code := "fmt.Println(\"test\")"

    _, err = client.ScanCode(ctx, code, "go")
    if err == nil {
        t.Error("Expected timeout error")
    }

    if !strings.Contains(err.Error(), "context deadline exceeded") {
        t.Errorf("Expected timeout error, got: %v", err)
    }
}

func TestScanSafeCode(t *testing.T) {
    client, err := tavo.NewClient("test-api-key")
    if err != nil {
        t.Fatal(err)
    }
    defer client.Close()

    // Safe code using parameterized queries
    code := `
        func authenticate(username, password string) {
            query := "SELECT * FROM users WHERE username = ? AND password = ?"
            executeQuery(query, username, password)
        }
    `

    result, err := client.ScanCode(context.Background(), code, "go")
    if err != nil {
        t.Fatal(err)
    }

    // Should not have high-severity issues
    highSeverityCount := 0
    for _, vuln := range result.Vulnerabilities {
        if vuln.Severity == "high" || vuln.Severity == "critical" {
            highSeverityCount++
        }
    }

    if highSeverityCount > 0 {
        t.Errorf("Expected no high-severity issues in safe code, found %d", highSeverityCount)
    }
}

func BenchmarkScanCode(b *testing.B) {
    client, err := tavo.NewClient("test-api-key")
    if err != nil {
        b.Fatal(err)
    }
    defer client.Close()

    code := `
        package main

        import "fmt"

        func main() {
            userInput := "'; DROP TABLE users; --"
            query := fmt.Sprintf("SELECT * FROM users WHERE id = '%s'", userInput)
            fmt.Println(query)
        }
    `

    ctx := context.Background()

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, err := client.ScanCode(ctx, code, "go")
        if err != nil {
            b.Fatal(err)
        }
    }
}
```

### Integration with Docker

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"
    "path/filepath"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func scanDockerProject() error {
    client, err := tavo.NewClient("your-api-key")
    if err != nil {
        return err
    }
    defer client.Close()

    ctx := context.Background()

    // Find all Go files in the project
    var goFiles []string
    err = filepath.Walk(".", func(path string, info os.FileInfo, err error) error {
        if err != nil {
            return err
        }

        if !info.IsDir() && filepath.Ext(path) == ".go" {
            goFiles = append(goFiles, path)
        }

        return nil
    })
    if err != nil {
        return err
    }

    fmt.Printf("Found %d Go files to scan\n", len(goFiles))

    totalIssues := 0
    for _, file := range goFiles {
        code, err := os.ReadFile(file)
        if err != nil {
            log.Printf("Failed to read %s: %v", file, err)
            continue
        }

        result, err := client.ScanCode(ctx, string(code), "go")
        if err != nil {
            log.Printf("Failed to scan %s: %v", file, err)
            continue
        }

        if result.TotalIssues > 0 {
            fmt.Printf("🔴 %s: %d issues\n", file, result.TotalIssues)
            totalIssues += result.TotalIssues
        } else {
            fmt.Printf("✅ %s: clean\n", file)
        }
    }

    fmt.Printf("\nTotal issues found: %d\n", totalIssues)

    // Exit with error code if issues found
    if totalIssues > 0 {
        os.Exit(1)
    }

    return nil
}

func main() {
    if err := scanDockerProject(); err != nil {
        log.Fatal(err)
    }
}
```

### Middleware Pattern

```go
package middleware

import (
    "context"
    "log"
    "time"

    "github.com/TavoAI/tavo-go-sdk/tavo"
)

type SecurityScanner struct {
    client *tavo.Client
}

func NewSecurityScanner(apiKey string) (*SecurityScanner, error) {
    client, err := tavo.NewClient(apiKey)
    if err != nil {
        return nil, err
    }

    return &SecurityScanner{client: client}, nil
}

func (s *SecurityScanner) Close() {
    s.client.Close()
}

func (s *SecurityScanner) ScanMiddleware(code, language string) (*tavo.ScanResult, error) {
    start := time.Now()

    result, err := s.client.ScanCode(context.Background(), code, language)
    if err != nil {
        log.Printf("Security scan failed: %v", err)
        return nil, err
    }

    duration := time.Since(start)
    log.Printf("Security scan completed in %v: %d issues found", duration, result.TotalIssues)

    // Log high-severity issues
    for _, vuln := range result.Vulnerabilities {
        if vuln.Severity == "critical" || vuln.Severity == "high" {
            log.Printf("🚨 HIGH SEVERITY: %s in %s", vuln.Title, vuln.Location.File)
        }
    }

    return result, nil
}

// HTTP middleware for Gin
func (s *SecurityScanner) GinSecurityMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        // Extract code from request
        var json map[string]interface{}
        if err := c.ShouldBindJSON(&json); err != nil {
            c.Next()
            return
        }

        if code, ok := json["code"].(string); ok {
            language := "go"
            if lang, exists := json["language"].(string); exists {
                language = lang
            }

            result, err := s.ScanMiddleware(code, language)
            if err != nil {
                log.Printf("Middleware scan failed: %v", err)
                c.Next()
                return
            }

            // Add scan results to context
            c.Set("scan_result", result)
        }

        c.Next()
    }
}
```