# .NET SDK

The Tavo AI .NET SDK provides a modern, async-first interface for integrating with the Tavo AI platform. Built with .NET Standard 2.1+ and C# 8.0+ features.

## Installation

### NuGet Package Manager

```bash
dotnet add package TavoAI
```

### Package Reference

```xml
<PackageReference Include="TavoAI" Version="1.0.0" />
```

## Quick Start

```csharp
using System;
using System.Threading.Tasks;
using TavoAI;

class Program
{
    static async Task Main(string[] args)
    {
        // Initialize the client
        var client = new TavoClient("your-api-key");

        // Scan code for vulnerabilities
        var code = @"
            public void ProcessUserInput(string userInput)
            {
                var query = $""SELECT * FROM users WHERE id = '{userInput}'"";
                // Potential SQL injection vulnerability
                ExecuteQuery(query);
            }
        ";

        var result = await client.ScanCodeAsync(code, "csharp");

        Console.WriteLine($"Found {result.TotalIssues} issues");
        foreach (var vuln in result.Vulnerabilities)
        {
            Console.WriteLine($"- {vuln.Title}: {vuln.Description}");
        }
    }
}
```

## Client Configuration

```csharp
// Basic client
var client = new TavoClient("your-api-key");

// With custom options
var client = new TavoClient(new TavoClientOptions
{
    ApiKey = "your-api-key",
    BaseUrl = "https://api-staging.tavoai.net",
    Timeout = TimeSpan.FromSeconds(30),
    MaxRetries = 3,
    RetryDelay = TimeSpan.FromSeconds(1)
});
```

## Core Operations

### Code Scanning

```csharp
// Basic code scan
var result = await client.ScanCodeAsync(code, "csharp");

// Advanced scan with options
var result = await client.ScanCodeAsync(new ScanOptions
{
    Code = code,
    Language = "csharp",
    Timeout = TimeSpan.FromMinutes(1),
    IncludeMetrics = true
});
```

### AI Model Analysis

```csharp
var modelConfig = new Dictionary<string, object>
{
    ["model_type"] = "transformer",
    ["parameters"] = new Dictionary<string, object>
    {
        ["layers"] = 12,
        ["heads"] = 8,
        ["hidden_size"] = 768
    }
};

var analysis = await client.AnalyzeModelAsync(modelConfig);
Console.WriteLine($"Model is safe: {analysis.Safe}");
```

### User Management

```csharp
// Get current user
var user = await client.GetCurrentUserAsync();

// Update user profile
var updates = new Dictionary<string, object>
{
    ["name"] = "New Name",
    ["email"] = "new@example.com"
};

var updatedUser = await client.UpdateUserAsync(user.Id, updates);

// API Key Management
var apiKeys = await client.ListApiKeysAsync();

// Update API key
var updatedKey = await client.UpdateApiKeyAsync(apiKeyId, new Dictionary<string, object>
{
    ["name"] = "Updated API Key Name",
    ["description"] = "Updated description"
});

// Rotate API key (generates new secret)
var rotatedKey = await client.RotateApiKeyAsync(apiKeyId);

// Delete API key
await client.DeleteApiKeyAsync(apiKeyId);
```

### Organization Management

```csharp
// List organizations
var organizations = await client.ListOrganizationsAsync();

// Create new organization
var newOrg = await client.CreateOrganizationAsync(new Dictionary<string, object>
{
    ["name"] = "My Company",
    ["description"] = "Security scanning service"
});
```

### Scan Jobs

```csharp
// Start a new scan job
var job = await client.CreateScanJobAsync(new Dictionary<string, object>
{
    ["target_url"] = "https://example.com",
    ["scan_type"] = "full_scan"
});

// Get job status
var status = await client.GetScanJobAsync(job.Id);

// List all jobs with pagination
var jobs = await client.ListScanJobsAsync(new ListOptions
{
    Limit = 10,
    Offset = 0
});
```

### Webhooks

```csharp
// Create webhook
var webhook = await client.CreateWebhookAsync(new WebhookConfig
{
    Url = "https://myapp.com/webhook",
    Events = new[] { "scan.completed", "vulnerability.found" }
});

// List webhooks
var webhooks = await client.ListWebhooksAsync();

// Delete webhook
await client.DeleteWebhookAsync(webhook.Id);
```

### Billing & Reports

```csharp
// Get billing information
var billing = await client.GetBillingInfoAsync();

// Generate report
var report = await client.GenerateReportAsync(new ReportConfig
{
    Type = "security_audit",
    DateRange = new DateRange
    {
        Start = "2024-01-01",
        End = "2024-01-31"
    }
});

// Get report summary statistics
var summary = await client.GetReportSummaryAsync();

Console.WriteLine($"Total scans: {summary.TotalScans}");
Console.WriteLine($"Total vulnerabilities: {summary.TotalVulnerabilities}");
Console.WriteLine($"Critical issues: {summary.CriticalIssues}");
```

## Error Handling

The SDK provides structured exception handling:

```csharp
try
{
    var result = await client.ScanCodeAsync(code, "csharp");
}
catch (TavoAuthException ex)
{
    Console.WriteLine($"Authentication failed: {ex.Message}");
}
catch (TavoApiException ex)
{
    Console.WriteLine($"API error: {ex.Message} (status: {ex.StatusCode})");
}
catch (TavoRateLimitException ex)
{
    Console.WriteLine($"Rate limit exceeded, retry after: {ex.RetryAfter}");
}
catch (TavoValidationException ex)
{
    Console.WriteLine($"Validation error: {ex.Message}");
    foreach (var (field, messages) in ex.FieldErrors)
    {
        Console.WriteLine($"  {field}: {string.Join(", ", messages)}");
    }
}
catch (Exception ex)
{
    Console.WriteLine($"Unknown error: {ex.Message}");
}
```

## Cancellation and Timeouts

The SDK supports cancellation tokens:

```csharp
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));

try
{
    var result = await client.ScanCodeAsync(code, "csharp", cancellationToken: cts.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Scan was cancelled or timed out");
}
```

## Advanced Usage

### Concurrent Scanning

```csharp
public async Task ScanMultipleFilesAsync(IEnumerable<string> filePaths)
{
    var tasks = filePaths.Select(async filePath =>
    {
        var code = await File.ReadAllTextAsync(filePath);
        var result = await client.ScanCodeAsync(code, "csharp");
        return (filePath, result.TotalIssues);
    });

    var results = await Task.WhenAll(tasks);

    foreach (var (filePath, issueCount) in results)
    {
        Console.WriteLine($"{filePath}: {issueCount} issues found");
    }
}
```

### Streaming Results

```csharp
// For large codebases, process results as they come
var scanner = client.CreateScanner();

var resultsTask = Task.Run(async () =>
{
    await foreach (var result in scanner.GetResultsAsync())
    {
        Console.WriteLine($"Scanned {result.FileName}: {result.TotalIssues} issues");
    }
});

var errorsTask = Task.Run(async () =>
{
    await foreach (var error in scanner.GetErrorsAsync())
    {
        Console.WriteLine($"Scan error: {error.Message}");
    }
});

// Start scanning multiple files
var files = new[] { "file1.cs", "file2.cs", "file3.cs" };
await scanner.ScanFilesAsync(files);

// Wait for processing to complete
await Task.WhenAll(resultsTask, errorsTask);
```

### Custom HTTP Client

```csharp
// Use custom HTTP client
var httpClient = new HttpClient
{
    Timeout = TimeSpan.FromSeconds(30)
};

var client = new TavoClient("your-api-key", httpClient);
```

### Dependency Injection

```csharp
// Register in DI container
services.AddSingleton<ITavoClient>(sp =>
    new TavoClient(Configuration["TavoApi:ApiKey"]));

// Use in controller
public class SecurityController : ControllerBase
{
    private readonly ITavoClient _tavoClient;

    public SecurityController(ITavoClient tavoClient)
    {
        _tavoClient = tavoClient;
    }

    [HttpPost("scan")]
    public async Task<IActionResult> ScanCode([FromBody] ScanRequest request)
    {
        var result = await _tavoClient.ScanCodeAsync(request.Code, request.Language);
        return Ok(new
        {
            totalIssues = result.TotalIssues,
            vulnerabilities = result.Vulnerabilities
        });
    }
}
```

## Integration Examples

### ASP.NET Core Web API

```csharp
using Microsoft.AspNetCore.Mvc;
using TavoAI;

[ApiController]
[Route("api/security")]
public class SecurityController : ControllerBase
{
    private readonly ITavoClient _tavoClient;

    public SecurityController(ITavoClient tavoClient)
    {
        _tavoClient = tavoClient;
    }

    [HttpPost("scan")]
    public async Task<IActionResult> ScanCode([FromBody] ScanCodeRequest request)
    {
        try
        {
            var result = await _tavoClient.ScanCodeAsync(request.Code, request.Language ?? "csharp");

            return Ok(new ScanResultDto
            {
                TotalIssues = result.TotalIssues,
                Vulnerabilities = result.Vulnerabilities.Select(v => new VulnerabilityDto
                {
                    Title = v.Title,
                    Description = v.Description,
                    Severity = v.Severity,
                    Location = v.Location != null ? new LocationDto
                    {
                        File = v.Location.File,
                        Line = v.Location.Line,
                        Column = v.Location.Column
                    } : null
                }).ToList()
            });
        }
        catch (TavoApiException ex)
        {
            return StatusCode(ex.StatusCode, new { error = ex.Message });
        }
    }
}

public class ScanCodeRequest
{
    public string Code { get; set; }
    public string Language { get; set; }
}

public class ScanResultDto
{
    public int TotalIssues { get; set; }
    public List<VulnerabilityDto> Vulnerabilities { get; set; }
}

public class VulnerabilityDto
{
    public string Title { get; set; }
    public string Description { get; set; }
    public string Severity { get; set; }
    public LocationDto Location { get; set; }
}

public class LocationDto
{
    public string File { get; set; }
    public int Line { get; set; }
    public int Column { get; set; }
}
```

### Console Application

```csharp
using System;
using System.CommandLine;
using System.CommandLine.Invocation;
using System.IO;
using System.Threading.Tasks;
using TavoAI;

class Program
{
    static async Task<int> Main(string[] args)
    {
        var rootCommand = new RootCommand("Tavo AI Security Scanner");

        var apiKeyOption = new Option<string>(
            "--api-key",
            "Tavo AI API key (or set TAVO_API_KEY environment variable)");
        var languageOption = new Option<string>(
            "--lang",
            () => "csharp",
            "Programming language");
        var fileOption = new Option<FileInfo>(
            "--file",
            "File to scan");

        rootCommand.AddOption(apiKeyOption);
        rootCommand.AddOption(languageOption);
        rootCommand.AddOption(fileOption);

        rootCommand.SetHandler(async (string apiKey, string language, FileInfo file) =>
        {
            apiKey ??= Environment.GetEnvironmentVariable("TAVO_API_KEY");
            if (string.IsNullOrEmpty(apiKey))
            {
                Console.Error.WriteLine("API key required. Use --api-key or set TAVO_API_KEY environment variable");
                return;
            }

            var client = new TavoClient(apiKey);

            string code;
            if (file != null)
            {
                code = await File.ReadAllTextAsync(file.FullName);
            }
            else
            {
                Console.WriteLine("Enter code to scan (press Ctrl+Z then Enter when done):");
                code = await Console.In.ReadToEndAsync();
            }

            try
            {
                var result = await client.ScanCodeAsync(code, language);

                Console.WriteLine($"Found {result.TotalIssues} issues:");
                for (int i = 0; i < result.Vulnerabilities.Count; i++)
                {
                    var vuln = result.Vulnerabilities[i];
                    Console.WriteLine($"{i + 1}. {vuln.Title} ({vuln.Severity})");
                    Console.WriteLine($"   {vuln.Description}");
                    if (vuln.Location != null)
                    {
                        Console.WriteLine($"   Location: {vuln.Location.File}:{vuln.Location.Line}:{vuln.Location.Column}");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Scan failed: {ex.Message}");
            }
        }, apiKeyOption, languageOption, fileOption);

        return await rootCommand.InvokeAsync(args);
    }
}
```

### Background Service

```csharp
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using TavoAI;

public class SecurityScanService : BackgroundService
{
    private readonly ILogger<SecurityScanService> _logger;
    private readonly ITavoClient _tavoClient;

    public SecurityScanService(ILogger<SecurityScanService> logger, ITavoClient tavoClient)
    {
        _logger = logger;
        _tavoClient = tavoClient;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Security scan service starting");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // Scan repository periodically
                var result = await _tavoClient.ScanRepositoryAsync("https://github.com/myorg/myrepo");

                if (result.TotalIssues > 0)
                {
                    _logger.LogWarning($"Found {result.TotalIssues} security issues in repository");
                    // Send notification, create issue, etc.
                }

                await Task.Delay(TimeSpan.FromHours(24), stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during security scan");
                await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
            }
        }
    }
}
```

### Testing with xUnit

```csharp
using System.Threading.Tasks;
using Xunit;
using TavoAI;

public class SecurityScanTests
{
    [Fact]
    public async Task ScanCode_DetectsSqlInjection()
    {
        // Arrange
        var client = new TavoClient("test-api-key");
        // Use a mock server for testing
        // client.SetBaseUrl("http://localhost:8080");

        var code = @"
            public void ProcessUserInput(string userInput)
            {
                var query = $""SELECT * FROM users WHERE id = '{userInput}'"";
                // SQL injection vulnerability
            }
        ";

        // Act
        var result = await client.ScanCodeAsync(code, "csharp");

        // Assert
        Assert.True(result.TotalIssues > 0, "Expected to find security issues");

        var sqlInjectionFound = result.Vulnerabilities
            .Any(v => v.Title.Contains("SQL Injection", StringComparison.OrdinalIgnoreCase));

        Assert.True(sqlInjectionFound, "Expected SQL injection vulnerability to be detected");
    }

    [Fact]
    public async Task ScanCode_HandlesCancellation()
    {
        // Arrange
        var client = new TavoClient("test-api-key");
        var code = "public class Test { }";
        using var cts = new CancellationTokenSource();
        cts.Cancel();

        // Act & Assert
        await Assert.ThrowsAsync<OperationCanceledException>(
            () => client.ScanCodeAsync(code, "csharp", cancellationToken: cts.Token));
    }
}
```

## Best Practices

1. **Async/Await**: Always use async methods and await properly
2. **Cancellation Tokens**: Pass cancellation tokens for cancellable operations
3. **Error Handling**: Catch specific Tavo exceptions, not just generic Exception
4. **Resource Management**: Implement proper disposal with using statements
5. **Dependency Injection**: Register clients as singletons in DI containers
6. **Timeouts**: Set appropriate timeouts for your use case
7. **Rate Limiting**: Implement proper rate limiting and backoff strategies

## Performance Considerations

- **Connection Reuse**: The SDK automatically reuses HTTP connections
- **Concurrent Operations**: Use Task.WhenAll for parallel scanning
- **Streaming**: Use streaming APIs for large datasets
- **Memory Management**: Dispose clients properly to free resources
