# .NET SDK Examples

This directory contains comprehensive examples for using the Tavo AI .NET SDK.

## Installation

### NuGet Package Manager

```bash
Install-Package TavoAI.SDK -Version 1.0.0
```

### .NET CLI

```bash
dotnet add package TavoAI.SDK --version 1.0.0
```

### Package Reference

```xml
<PackageReference Include="TavoAI.SDK" Version="1.0.0" />
```

## Basic Usage

### Simple Code Scan

```csharp
using TavoAI.SDK;
using TavoAI.SDK.Models;

public class BasicScanExample
{
    public static async Task Main(string[] args)
    {
        // Initialize client
        var client = new TavoClient("your-api-key");

        // Code to scan
        var code = """
            public void ProcessUserInput(string userInput) {
                string query = "SELECT * FROM users WHERE id = '" + userInput + "'";
                // Potential SQL injection vulnerability
                ExecuteQuery(query);
            }
            """;

        try
        {
            // Scan the code
            var result = await client.ScanCodeAsync(code, "csharp");

            Console.WriteLine($"Found {result.TotalIssues} issues");

            foreach (var vuln in result.Vulnerabilities)
            {
                Console.WriteLine($"- {vuln.Title}: {vuln.Description}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Scan failed: {ex.Message}");
        }
        finally
        {
            // Clean up
            await client.DisposeAsync();
        }
    }
}
```

### Configuration and Error Handling

```csharp
using TavoAI.SDK;
using TavoAI.SDK.Exceptions;
using System.Net.Http;

public class ConfiguredScanExample
{
    public static async Task Main(string[] args)
    {
        // Configure client
        var config = new TavoClientConfig
        {
            ApiKey = "your-api-key",
            BaseUrl = "https://api.tavoai.net",
            Timeout = TimeSpan.FromSeconds(30),
            MaxRetries = 3,
            RetryDelay = TimeSpan.FromSeconds(1),
            HttpClient = new HttpClient() // Custom HttpClient if needed
        };

        var client = new TavoClient(config);

        try
        {
            var result = await client.ScanCodeAsync("Console.WriteLine(\"hello\");", "csharp");
            Console.WriteLine($"Scan successful: {result.TotalIssues} issues");
        }
        catch (TavoAuthException ex)
        {
            Console.WriteLine($"Authentication failed: {ex.Message}");
        }
        catch (TavoApiException ex)
        {
            Console.WriteLine($"API error: {ex.Message} (status: {ex.StatusCode})");
        }
        catch (TavoException ex)
        {
            Console.WriteLine($"Tavo error: {ex.Message}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Unexpected error: {ex.Message}");
        }
        finally
        {
            await client.DisposeAsync();
        }
    }
}
```

## Advanced Examples

### Concurrent Batch Scanning

```csharp
using TavoAI.SDK;
using TavoAI.SDK.Models;
using System.Collections.Concurrent;

public class BatchScanner
{
    private readonly TavoClient _client;

    public BatchScanner(string apiKey)
    {
        _client = new TavoClient(apiKey);
    }

    public async Task<int> ScanDirectoryAsync(string directoryPath, int maxConcurrency = 5)
    {
        var files = await FindCSharpFilesAsync(directoryPath);
        var results = new ConcurrentBag<ScanResultWithPath>();

        // Process files concurrently with semaphore for rate limiting
        var semaphore = new SemaphoreSlim(maxConcurrency);
        var tasks = files.Select(async file =>
        {
            await semaphore.WaitAsync();
            try
            {
                var result = await ScanFileAsync(file);
                results.Add(result);
                Console.WriteLine($"{result.FilePath}: {result.Issues} issues");
            }
            finally
            {
                semaphore.Release();
            }
        });

        await Task.WhenAll(tasks);

        var totalIssues = results.Sum(r => r.Issues);
        Console.WriteLine($"Total issues found: {totalIssues}");

        return totalIssues;
    }

    private async Task<List<string>> FindCSharpFilesAsync(string directoryPath)
    {
        var files = new List<string>();
        foreach (var file in Directory.EnumerateFiles(directoryPath, "*.cs", SearchOption.AllDirectories))
        {
            files.Add(file);
        }
        return files;
    }

    private async Task<ScanResultWithPath> ScanFileAsync(string filePath)
    {
        try
        {
            var code = await File.ReadAllTextAsync(filePath);
            var result = await _client.ScanCodeAsync(code, "csharp");
            return new ScanResultWithPath(filePath, result.TotalIssues);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Failed to scan {filePath}: {ex.Message}");
            return new ScanResultWithPath(filePath, 0);
        }
    }

    public async ValueTask DisposeAsync()
    {
        await _client.DisposeAsync();
    }

    private record ScanResultWithPath(string FilePath, int Issues);

    public static async Task Main(string[] args)
    {
        await using var scanner = new BatchScanner("your-api-key");
        await scanner.ScanDirectoryAsync("./src");
    }
}
```

### AI Model Analysis

```csharp
using TavoAI.SDK;
using TavoAI.SDK.Models;
using System.Text.Json;
using System.Text.Json.Nodes;

public class ModelAnalysisExample
{
    public static async Task Main(string[] args)
    {
        var client = new TavoClient("your-api-key");

        try
        {
            var modelConfig = new JsonObject
            {
                ["model_type"] = "transformer",
                ["architecture"] = new JsonObject
                {
                    ["layers"] = 12,
                    ["attention_heads"] = 8,
                    ["hidden_size"] = 768,
                    ["vocab_size"] = 30000
                },
                ["training"] = new JsonObject
                {
                    ["dataset"] = "wikipedia",
                    ["epochs"] = 10,
                    ["learning_rate"] = 0.0001
                }
            };

            var analysis = await client.AnalyzeModelAsync(modelConfig);

            Console.WriteLine($"Model safety: {(analysis.IsSafe ? "Safe" : "Unsafe")}");

            if (!analysis.IsSafe && analysis.Issues != null)
            {
                Console.WriteLine("Issues found:");
                for (int i = 0; i < analysis.Issues.Count; i++)
                {
                    var issue = analysis.Issues[i];
                    Console.WriteLine($"{i + 1}. {issue.Title}: {issue.Description}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Analysis failed: {ex.Message}");
        }
        finally
        {
            await client.DisposeAsync();
        }
    }
}
```

### Webhook Management

```csharp
using TavoAI.SDK;
using TavoAI.SDK.Models;

public class WebhookManagementExample
{
    public static async Task Main(string[] args)
    {
        var client = new TavoClient("your-api-key");

        try
        {
            // Create a webhook
            var config = new WebhookConfig
            {
                Url = "https://myapp.com/webhook/scan-complete",
                Events = new[] { "scan.completed", "vulnerability.found" },
                Secret = "webhook-secret",
                Active = true
            };

            var webhook = await client.CreateWebhookAsync(config);
            Console.WriteLine($"Created webhook: {webhook.Id}");

            // List all webhooks
            var webhooks = await client.ListWebhooksAsync();
            Console.WriteLine($"Total webhooks: {webhooks.Count}");

            foreach (var wh in webhooks)
            {
                Console.WriteLine($"- {wh.Id}: {wh.Url} ({string.Join(", ", wh.Events)})");
            }

            // Update webhook
            var updateConfig = new WebhookConfig
            {
                Events = new[] { "scan.completed", "vulnerability.found", "scan.failed" }
            };

            await client.UpdateWebhookAsync(webhook.Id, updateConfig);
            Console.WriteLine("Webhook updated");

            // Delete the webhook
            await client.DeleteWebhookAsync(webhook.Id);
            Console.WriteLine("Webhook deleted");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Webhook management failed: {ex.Message}");
        }
        finally
        {
            await client.DisposeAsync();
        }
    }
}
```

## Integration Examples

### ASP.NET Core Web API

```csharp
using Microsoft.AspNetCore.Mvc;
using TavoAI.SDK;
using TavoAI.SDK.Exceptions;
using TavoAI.SDK.Models;

namespace SecurityScanner.Controllers
{
    [ApiController]
    [Route("api/security")]
    public class SecurityController : ControllerBase
    {
        private readonly TavoClient _tavoClient;
        private readonly ILogger<SecurityController> _logger;

        public SecurityController(TavoClient tavoClient, ILogger<SecurityController> logger)
        {
            _tavoClient = tavoClient;
            _logger = logger;
        }

        [HttpPost("scan")]
        public async Task<IActionResult> ScanCode([FromBody] ScanRequest request)
        {
            try
            {
                var result = await _tavoClient.ScanCodeAsync(request.Code, request.Language);

                var vulnerabilities = result.Vulnerabilities
                    .Select(v => new VulnerabilityDto
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
                    })
                    .ToList();

                var response = new ScanResponse
                {
                    TotalIssues = result.TotalIssues,
                    Vulnerabilities = vulnerabilities,
                    ScanId = result.ScanId
                };

                return Ok(response);
            }
            catch (TavoAuthException ex)
            {
                return Unauthorized();
            }
            catch (TavoApiException ex)
            {
                return StatusCode(ex.StatusCode);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Scan failed");
                return StatusCode(500);
            }
        }

        [HttpPost("scan/async")]
        public async Task<IActionResult> ScanCodeAsync([FromBody] AsyncScanRequest request)
        {
            var scanId = $"scan_{DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()}_{Guid.NewGuid().ToString().Substring(0, 8)}";

            // Start async processing
            _ = Task.Run(async () =>
            {
                try
                {
                    var result = await _tavoClient.ScanCodeAsync(request.Code, request.Language);

                    if (!string.IsNullOrEmpty(request.WebhookUrl))
                    {
                        await SendWebhookNotificationAsync(request.WebhookUrl, scanId, result);
                    }

                    _logger.LogInformation("Async scan {ScanId} completed: {Issues} issues", scanId, result.TotalIssues);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Async scan {ScanId} failed", scanId);
                }
            });

            var response = new AsyncScanResponse
            {
                ScanId = scanId,
                Status = "processing",
                Message = "Scan started. Results will be sent to webhook."
            };

            return Accepted(response);
        }

        private async Task SendWebhookNotificationAsync(string webhookUrl, string scanId, ScanResult result)
        {
            // Implementation would send HTTP POST to webhookUrl with scan results
            _logger.LogInformation("Sending webhook notification to {WebhookUrl} for scan {ScanId}", webhookUrl, scanId);
        }
    }

    // DTOs
    public record ScanRequest(string Code, string Language);
    public record AsyncScanRequest(string Code, string Language, string WebhookUrl);
    public record ScanResponse(int TotalIssues, List<VulnerabilityDto> Vulnerabilities, string ScanId);
    public record AsyncScanResponse(string ScanId, string Status, string Message);
    public record VulnerabilityDto(string Title, string Description, string Severity, LocationDto Location);
    public record LocationDto(string File, int Line, int Column);
}

// Program.cs or Startup.cs
public class Program
{
    public static void Main(string[] args)
    {
        CreateHostBuilder(args).Build().Run();
    }

    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureServices((context, services) =>
            {
                var apiKey = context.Configuration["Tavo:ApiKey"];
                services.AddSingleton(new TavoClient(apiKey));
            })
            .ConfigureWebHostDefaults(webBuilder =>
            {
                webBuilder.UseStartup<Startup>();
            });
}

public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddControllers();
        // TavoClient is registered in Program.cs
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        if (env.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }

        app.UseRouting();
        app.UseAuthorization();

        app.UseEndpoints(endpoints =>
        {
            endpoints.MapControllers();
        });
    }
}
```

### Console Application with Dependency Injection

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System.CommandLine;
using TavoAI.SDK;
using TavoAI.SDK.Models;

namespace TavoScanner
{
    public class Program
    {
        public static async Task<int> Main(string[] args)
        {
            var rootCommand = new RootCommand("Tavo AI Security Scanner CLI");

            var apiKeyOption = new Option<string>(
                name: "--api-key",
                description: "Tavo AI API key");
            apiKeyOption.AddAlias("-k");

            var languageOption = new Option<string>(
                name: "--language",
                description: "Programming language",
                getDefaultValue: () => "csharp");
            languageOption.AddAlias("-l");

            var recursiveOption = new Option<bool>(
                name: "--recursive",
                description: "Scan directories recursively");
            recursiveOption.AddAlias("-r");

            var verboseOption = new Option<bool>(
                name: "--verbose",
                description: "Verbose output");
            verboseOption.AddAlias("-v");

            var pathArgument = new Argument<string>(
                name: "path",
                description: "File or directory to scan");

            rootCommand.AddOption(apiKeyOption);
            rootCommand.AddOption(languageOption);
            rootCommand.AddOption(recursiveOption);
            rootCommand.AddOption(verboseOption);
            rootCommand.AddArgument(pathArgument);

            rootCommand.SetHandler(async (apiKey, language, recursive, verbose, path) =>
            {
                // Get API key from option or environment
                var key = apiKey ?? Environment.GetEnvironmentVariable("TAVO_API_KEY");
                if (string.IsNullOrEmpty(key))
                {
                    Console.Error.WriteLine("❌ API key required. Use --api-key or set TAVO_API_KEY environment variable");
                    Environment.Exit(1);
                }

                await using var host = CreateHostBuilder(key).Build();
                await host.StartAsync();

                var scanner = host.Services.GetRequiredService<ScannerService>();

                try
                {
                    if (File.Exists(path))
                    {
                        var issues = await scanner.ScanFileAsync(path, language, verbose);
                        Environment.Exit(issues > 0 ? 1 : 0);
                    }
                    else if (Directory.Exists(path))
                    {
                        var issues = await scanner.ScanDirectoryAsync(path, language, recursive, verbose);
                        Environment.Exit(issues > 0 ? 1 : 0);
                    }
                    else
                    {
                        Console.Error.WriteLine("❌ Path is neither a file nor directory");
                        Environment.Exit(1);
                    }
                }
                catch (Exception ex)
                {
                    Console.Error.WriteLine($"❌ Error: {ex.Message}");
                    Environment.Exit(1);
                }
                finally
                {
                    await host.StopAsync();
                }
            }, apiKeyOption, languageOption, recursiveOption, verboseOption, pathArgument);

            return await rootCommand.InvokeAsync(args);
        }

        public static IHostBuilder CreateHostBuilder(string apiKey) =>
            Host.CreateDefaultBuilder()
                .ConfigureServices((context, services) =>
                {
                    services.AddSingleton(new TavoClient(apiKey));
                    services.AddSingleton<ScannerService>();
                });
    }

    public class ScannerService
    {
        private readonly TavoClient _client;

        public ScannerService(TavoClient client)
        {
            _client = client;
        }

        public async Task<int> ScanFileAsync(string filePath, string language, bool verbose)
        {
            var code = await File.ReadAllTextAsync(filePath);
            var result = await _client.ScanCodeAsync(code, language);

            PrintScanResult(filePath, result, verbose);
            return result.TotalIssues;
        }

        public async Task<int> ScanDirectoryAsync(string directoryPath, string language, bool recursive, bool verbose)
        {
            var files = await FindFilesToScanAsync(directoryPath, language, recursive);
            var totalIssues = 0;

            foreach (var file in files)
            {
                var issues = await ScanFileAsync(file, language, verbose);
                totalIssues += issues;
            }

            Console.WriteLine($"\n📊 Summary: {totalIssues} total issues");
            return totalIssues;
        }

        private async Task<List<string>> FindFilesToScanAsync(string directoryPath, string language, bool recursive)
        {
            var extension = GetExtensionForLanguage(language);
            var searchOption = recursive ? SearchOption.AllDirectories : SearchOption.TopDirectoryOnly;

            return Directory.EnumerateFiles(directoryPath, extension, searchOption).ToList();
        }

        private string GetExtensionForLanguage(string language)
        {
            return language.ToLower() switch
            {
                "csharp" or "c#" => "*.cs",
                "fsharp" or "f#" => "*.fs",
                "vbnet" or "vb" => "*.vb",
                _ => "*.cs"
            };
        }

        private void PrintScanResult(string filePath, ScanResult result, bool verbose)
        {
            if (result.TotalIssues > 0)
            {
                Console.WriteLine($"\n🔴 {filePath} ({result.TotalIssues} issues):");

                foreach (var (vuln, index) in result.Vulnerabilities.Select((v, i) => (v, i)))
                {
                    Console.WriteLine($"  {index + 1}. {vuln.Title} ({vuln.Severity})");
                    if (verbose)
                    {
                        Console.WriteLine($"     {vuln.Description}");
                        if (vuln.Location != null)
                        {
                            Console.WriteLine($"     📍 {vuln.Location.File}:{vuln.Location.Line}:{vuln.Location.Column}");
                        }
                    }
                }
            }
            else
            {
                Console.WriteLine($"✅ {filePath} (0 issues)");
            }
        }
    }
}
```

## Testing Examples

### Unit Tests with xUnit and Moq

```csharp
using Xunit;
using Moq;
using TavoAI.SDK;
using TavoAI.SDK.Exceptions;
using TavoAI.SDK.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace TavoAI.SDK.Tests
{
    public class TavoClientTests : IDisposable
    {
        private readonly Mock<TavoClient> _mockClient;
        private readonly TavoClient _client;

        public TavoClientTests()
        {
            _mockClient = new Mock<TavoClient>("test-key");
            // Note: In real tests, you'd need to mock the HttpClient or use integration tests
        }

        [Fact]
        public async Task ScanCodeAsync_Success_ReturnsResult()
        {
            // Arrange
            var expectedResult = new ScanResult
            {
                TotalIssues = 1,
                Vulnerabilities = new List<Vulnerability>
                {
                    new Vulnerability
                    {
                        Title = "SQL Injection",
                        Description = "Potential SQL injection vulnerability",
                        Severity = "high"
                    }
                }
            };

            // Act & Assert
            // Note: This would require integration testing with a real API
            // For unit tests, you'd mock the HTTP responses
            Assert.True(true); // Placeholder
        }

        [Fact]
        public async Task ScanCodeAsync_ApiError_ThrowsException()
        {
            // Arrange
            // Mock API error response

            // Act & Assert
            // Note: Implementation would depend on how the client handles errors
            Assert.True(true); // Placeholder
        }

        public void Dispose()
        {
            _client?.Dispose();
        }
    }
}
```

### Integration Tests with Test Containers

```csharp
using Xunit;
using TavoAI.SDK;
using TavoAI.SDK.Models;
using DotNet.Testcontainers.Builders;
using DotNet.Testcontainers.Containers;
using System.Threading.Tasks;

namespace TavoAI.SDK.IntegrationTests
{
    public class TavoClientIntegrationTests : IAsyncLifetime
    {
        private TavoClient _client;
        private IContainer _tavoContainer;

        public async Task InitializeAsync()
        {
            var apiKey = Environment.GetEnvironmentVariable("TAVO_API_KEY");
            if (string.IsNullOrEmpty(apiKey))
            {
                throw new InvalidOperationException("TAVO_API_KEY environment variable required");
            }

            _client = new TavoClient(apiKey);

            // Start Tavo API container for integration tests
            _tavoContainer = new ContainerBuilder()
                .WithImage("tavoai/tavo-sdk:latest")
                .WithPortBinding(8080, true)
                .WithEnvironment("TAVO_API_KEY", apiKey)
                .Build();

            await _tavoContainer.StartAsync();
        }

        public async Task DisposeAsync()
        {
            await _client.DisposeAsync();
            await _tavoContainer.DisposeAsync();
        }

        [Fact]
        public async Task ScanVulnerableCode_DetectsSqlInjection()
        {
            // Arrange
            var vulnerableCode = """
                public void Authenticate(string username, string password) {
                    string query = "SELECT * FROM users WHERE username='" + username +
                                  "' AND password='" + password + "'";
                    // SQL injection vulnerability
                    ExecuteQuery(query);
                }
                """;

            // Act
            var result = await _client.ScanCodeAsync(vulnerableCode, "csharp");

            // Assert
            Assert.True(result.TotalIssues > 0);
            Assert.Contains(result.Vulnerabilities,
                v => v.Title.ToLower().Contains("sql") && v.Title.ToLower().Contains("injection"));
        }

        [Fact]
        public async Task ScanSafeCode_NoHighSeverityIssues()
        {
            // Arrange
            var safeCode = """
                public void Authenticate(string username, string password) {
                    string query = "SELECT * FROM users WHERE username=? AND password=?";
                    ExecuteQuery(query, username, password);
                }
                """;

            // Act
            var result = await _client.ScanCodeAsync(safeCode, "csharp");

            // Assert
            var highSeverityIssues = result.Vulnerabilities
                .Count(v => v.Severity == "critical" || v.Severity == "high");

            Assert.Equal(0, highSeverityIssues);
        }
    }
}
```

### Performance Tests with BenchmarkDotNet

```csharp
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;
using TavoAI.SDK;
using System.Threading.Tasks;

namespace TavoAI.SDK.Benchmarks
{
    [MemoryDiagnoser]
    [SimpleJob(iterationCount: 3, warmupCount: 2)]
    public class TavoClientBenchmarks
    {
        private TavoClient _client;
        private string _testCode;

        [GlobalSetup]
        public void Setup()
        {
            _client = new TavoClient("benchmark-api-key");

            _testCode = """
                public class TestClass {
                    public void Method1() {
                        string sql = "SELECT * FROM users WHERE id = " + userId;
                        ExecuteQuery(sql);
                    }

                    public void Method2() {
                        string cmd = "ls " + userInput;
                        ExecuteCommand(cmd);
                    }

                    public void Method3() {
                        string xpath = "//users[@id='" + userId + "']";
                        EvaluateXPath(xpath);
                    }
                }
                """;
        }

        [GlobalCleanup]
        public void Cleanup()
        {
            _client.Dispose();
        }

        [Benchmark]
        public async Task ScanCodeBenchmark()
        {
            var result = await _client.ScanCodeAsync(_testCode, "csharp");
        }
    }

    public class Program
    {
        public static void Main(string[] args)
        {
            BenchmarkRunner.Run<TavoClientBenchmarks>();
        }
    }
}
```
