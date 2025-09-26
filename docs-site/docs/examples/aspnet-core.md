---
sidebar_position: 9
---

# ASP.NET Core Integration

Integrate Tavo AI security scanning into your ASP.NET Core applications.

## Installation

```bash
dotnet add package TavoAI.Client
dotnet add package Microsoft.Extensions.Http
dotnet add package Microsoft.Extensions.Configuration
```

## Basic Setup

### Configuration

```csharp
// appsettings.json
{
  "Tavo": {
    "ApiKey": "your-api-key-here",
    "BaseUrl": "https://api.tavoai.net",
    "TimeoutSeconds": 30
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

```csharp
// Program.cs
using TavoAI.Client;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Configure Tavo AI client
builder.Services.AddHttpClient<ITavoClient, TavoClient>((serviceProvider, client) =>
{
    var configuration = serviceProvider.GetRequiredService<IConfiguration>();
    var tavoConfig = configuration.GetSection("Tavo");

    client.BaseAddress = new Uri(tavoConfig["BaseUrl"] ?? "https://api.tavoai.net");
    client.Timeout = TimeSpan.FromSeconds(int.Parse(tavoConfig["TimeoutSeconds"] ?? "30"));

    var apiKey = tavoConfig["ApiKey"];
    if (!string.IsNullOrEmpty(apiKey))
    {
        client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");
    }
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

### Tavo Client Interface

```csharp
// Interfaces/ITavoClient.cs
using System.Threading.Tasks;
using TavoAI.Client.Models;

namespace TavoAI.Client.Interfaces
{
    public interface ITavoClient
    {
        Task<ScanResult> ScanCodeAsync(string code, string language = "csharp", string? name = null);
        Task<ScanResult> ScanUrlAsync(string url, string? name = null);
        Task<ScanResult> GetScanResultsAsync(string scanId);
        Task<ScanResult> GetScanStatusAsync(string scanId);
        Task<ScanListResult> ListScansAsync(int limit = 50, int offset = 0, string? status = null);
        Task<ReportResult> GenerateReportAsync(string[] scanIds, string reportType = "compliance", string format = "pdf");
        Task<ReportResult> GetReportStatusAsync(string reportId);
        Task<byte[]> DownloadReportAsync(string reportId);
    }
}
```

### Tavo Client Implementation

```csharp
// Clients/TavoClient.cs
using System.Net.Http;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using TavoAI.Client.Interfaces;
using TavoAI.Client.Models;

namespace TavoAI.Client.Clients
{
    public class TavoClient : ITavoClient
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<TavoClient> _logger;
        private readonly JsonSerializerOptions _jsonOptions;

        public TavoClient(HttpClient httpClient, ILogger<TavoClient> logger)
        {
            _httpClient = httpClient;
            _logger = logger;
            _jsonOptions = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            };
        }

        public async Task<ScanResult> ScanCodeAsync(string code, string language = "csharp", string? name = null)
        {
            if (string.IsNullOrEmpty(name))
            {
                name = $"Code Scan - {language}";
            }

            var request = new ScanRequest
            {
                Name = name,
                Target = code,
                ScanType = "code",
                Language = language
            };

            return await PostAsync<ScanResult>("/scans", request);
        }

        public async Task<ScanResult> ScanUrlAsync(string url, string? name = null)
        {
            if (string.IsNullOrEmpty(name))
            {
                name = $"URL Scan - {url}";
            }

            var request = new ScanRequest
            {
                Name = name,
                Target = url,
                ScanType = "web"
            };

            return await PostAsync<ScanResult>("/scans", request);
        }

        public async Task<ScanResult> GetScanResultsAsync(string scanId)
        {
            return await GetAsync<ScanResult>($"/scans/{scanId}/results");
        }

        public async Task<ScanResult> GetScanStatusAsync(string scanId)
        {
            return await GetAsync<ScanResult>($"/scans/{scanId}");
        }

        public async Task<ScanListResult> ListScansAsync(int limit = 50, int offset = 0, string? status = null)
        {
            var queryParams = new List<string>
            {
                $"limit={limit}",
                $"offset={offset}"
            };

            if (!string.IsNullOrEmpty(status))
            {
                queryParams.Add($"status={status}");
            }

            var queryString = string.Join("&", queryParams);
            return await GetAsync<ScanListResult>($"/scans?{queryString}");
        }

        public async Task<ReportResult> GenerateReportAsync(string[] scanIds, string reportType = "compliance", string format = "pdf")
        {
            var request = new ReportRequest
            {
                ScanIds = scanIds,
                Type = reportType,
                Format = format
            };

            return await PostAsync<ReportResult>("/reports", request);
        }

        public async Task<ReportResult> GetReportStatusAsync(string reportId)
        {
            return await GetAsync<ReportResult>($"/reports/{reportId}");
        }

        public async Task<byte[]> DownloadReportAsync(string reportId)
        {
            var response = await _httpClient.GetAsync($"/reports/{reportId}/download");
            response.EnsureSuccessStatusCode();

            return await response.Content.ReadAsByteArrayAsync();
        }

        private async Task<T> GetAsync<T>(string endpoint)
        {
            try
            {
                _logger.LogInformation("Making GET request to {Endpoint}", endpoint);

                var response = await _httpClient.GetAsync(endpoint);
                response.EnsureSuccessStatusCode();

                var content = await response.Content.ReadAsStringAsync();
                var result = JsonSerializer.Deserialize<T>(content, _jsonOptions);

                if (result == null)
                {
                    throw new InvalidOperationException("Failed to deserialize response");
                }

                return result;
            }
            catch (HttpRequestException ex)
            {
                _logger.LogError(ex, "HTTP request failed for {Endpoint}", endpoint);
                throw new TavoApiException($"API request failed: {ex.Message}", ex);
            }
            catch (JsonException ex)
            {
                _logger.LogError(ex, "JSON deserialization failed for {Endpoint}", endpoint);
                throw new TavoApiException($"Failed to parse API response: {ex.Message}", ex);
            }
        }

        private async Task<T> PostAsync<T>(string endpoint, object data)
        {
            try
            {
                _logger.LogInformation("Making POST request to {Endpoint}", endpoint);

                var json = JsonSerializer.Serialize(data);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync(endpoint, content);
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                var result = JsonSerializer.Deserialize<T>(responseContent, _jsonOptions);

                if (result == null)
                {
                    throw new InvalidOperationException("Failed to deserialize response");
                }

                return result;
            }
            catch (HttpRequestException ex)
            {
                _logger.LogError(ex, "HTTP request failed for {Endpoint}", endpoint);
                throw new TavoApiException($"API request failed: {ex.Message}", ex);
            }
            catch (JsonException ex)
            {
                _logger.LogError(ex, "JSON deserialization failed for {Endpoint}", endpoint);
                throw new TavoApiException($"Failed to parse API response: {ex.Message}", ex);
            }
        }
    }
}
```

### Models

```csharp
// Models/ScanRequest.cs
namespace TavoAI.Client.Models
{
    public class ScanRequest
    {
        public string Name { get; set; } = string.Empty;
        public string Target { get; set; } = string.Empty;
        public string ScanType { get; set; } = string.Empty;
        public string? Language { get; set; }
    }
}
```

```csharp
// Models/ScanResult.cs
using System.Text.Json.Serialization;

namespace TavoAI.Client.Models
{
    public class ScanResult
    {
        public string Id { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
        public string Name { get; set; } = string.Empty;
        public string ScanType { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; }
        public ScanSummary? Summary { get; set; }
    }

    public class ScanSummary
    {
        [JsonPropertyName("files_scanned")]
        public int FilesScanned { get; set; }

        [JsonPropertyName("vulnerabilities_found")]
        public int VulnerabilitiesFound { get; set; }

        public string Duration { get; set; } = string.Empty;
    }
}
```

```csharp
// Models/ScanListResult.cs
namespace TavoAI.Client.Models
{
    public class ScanListResult
    {
        public ScanResult[] Scans { get; set; } = Array.Empty<ScanResult>();
        public int Total { get; set; }
        public int Limit { get; set; }
        public int Offset { get; set; }
    }
}
```

```csharp
// Models/ReportRequest.cs
namespace TavoAI.Client.Models
{
    public class ReportRequest
    {
        public string[] ScanIds { get; set; } = Array.Empty<string>();
        public string Type { get; set; } = "compliance";
        public string Format { get; set; } = "pdf";
    }
}
```

```csharp
// Models/ReportResult.cs
namespace TavoAI.Client.Models
{
    public class ReportResult
    {
        public string Id { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
        public string Type { get; set; } = string.Empty;
        public string Format { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; }
        public string? DownloadUrl { get; set; }
    }
}
```

```csharp
// Exceptions/TavoApiException.cs
namespace TavoAI.Client.Exceptions
{
    public class TavoApiException : Exception
    {
        public TavoApiException(string message) : base(message)
        {
        }

        public TavoApiException(string message, Exception innerException)
            : base(message, innerException)
        {
        }
    }
}
```

## ASP.NET Core Controllers

### Scans Controller

```csharp
// Controllers/ScansController.cs
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using TavoAI.Client.Interfaces;
using TavoAI.Client.Models;
using TavoAI.Client.Exceptions;

namespace TavoAI.Web.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize] // Add authentication as needed
    public class ScansController : ControllerBase
    {
        private readonly ITavoClient _tavoClient;
        private readonly ILogger<ScansController> _logger;

        public ScansController(ITavoClient tavoClient, ILogger<ScansController> logger)
        {
            _tavoClient = tavoClient;
            _logger = logger;
        }

        [HttpPost]
        [ProducesResponseType(typeof(ScanResult), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> CreateScan([FromBody] ScanRequest request)
        {
            try
            {
                ScanResult result;

                if (request.ScanType == "code")
                {
                    result = await _tavoClient.ScanCodeAsync(
                        request.Target,
                        request.Language ?? "csharp",
                        request.Name
                    );
                }
                else if (request.ScanType == "web")
                {
                    result = await _tavoClient.ScanUrlAsync(request.Target, request.Name);
                }
                else
                {
                    return BadRequest("Invalid scan type. Must be 'code' or 'web'.");
                }

                _logger.LogInformation("Scan created successfully: {ScanId}", result.Id);
                return Ok(result);
            }
            catch (TavoApiException ex)
            {
                _logger.LogError(ex, "Tavo API error during scan creation");
                return StatusCode(500, "Failed to create scan due to API error");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error during scan creation");
                return StatusCode(500, "An unexpected error occurred");
            }
        }

        [HttpGet("{scanId}")]
        [ProducesResponseType(typeof(ScanResult), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> GetScan(string scanId)
        {
            try
            {
                var result = await _tavoClient.GetScanStatusAsync(scanId);

                if (result == null)
                {
                    return NotFound($"Scan with ID {scanId} not found");
                }

                return Ok(result);
            }
            catch (TavoApiException ex)
            {
                _logger.LogError(ex, "Tavo API error getting scan {ScanId}", scanId);
                return StatusCode(500, "Failed to get scan status");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error getting scan {ScanId}", scanId);
                return StatusCode(500, "An unexpected error occurred");
            }
        }

        [HttpGet("{scanId}/results")]
        [ProducesResponseType(typeof(ScanResult), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> GetScanResults(string scanId)
        {
            try
            {
                var result = await _tavoClient.GetScanResultsAsync(scanId);

                if (result == null)
                {
                    return NotFound($"Scan results for ID {scanId} not found");
                }

                return Ok(result);
            }
            catch (TavoApiException ex)
            {
                _logger.LogError(ex, "Tavo API error getting scan results {ScanId}", scanId);
                return StatusCode(500, "Failed to get scan results");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error getting scan results {ScanId}", scanId);
                return StatusCode(500, "An unexpected error occurred");
            }
        }

        [HttpGet]
        [ProducesResponseType(typeof(ScanListResult), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> ListScans(
            [FromQuery] int limit = 50,
            [FromQuery] int offset = 0,
            [FromQuery] string? status = null)
        {
            try
            {
                var result = await _tavoClient.ListScansAsync(limit, offset, status);
                return Ok(result);
            }
            catch (TavoApiException ex)
            {
                _logger.LogError(ex, "Tavo API error listing scans");
                return StatusCode(500, "Failed to list scans");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error listing scans");
                return StatusCode(500, "An unexpected error occurred");
            }
        }
    }
}
```

### Reports Controller

```csharp
// Controllers/ReportsController.cs
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using TavoAI.Client.Interfaces;
using TavoAI.Client.Models;
using TavoAI.Client.Exceptions;

namespace TavoAI.Web.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class ReportsController : ControllerBase
    {
        private readonly ITavoClient _tavoClient;
        private readonly ILogger<ReportsController> _logger;

        public ReportsController(ITavoClient tavoClient, ILogger<ReportsController> logger)
        {
            _tavoClient = tavoClient;
            _logger = logger;
        }

        [HttpPost]
        [ProducesResponseType(typeof(ReportResult), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> GenerateReport([FromBody] ReportRequest request)
        {
            try
            {
                if (request.ScanIds == null || request.ScanIds.Length == 0)
                {
                    return BadRequest("At least one scan ID is required");
                }

                var result = await _tavoClient.GenerateReportAsync(
                    request.ScanIds,
                    request.Type,
                    request.Format
                );

                _logger.LogInformation("Report generated successfully: {ReportId}", result.Id);
                return Ok(result);
            }
            catch (TavoApiException ex)
            {
                _logger.LogError(ex, "Tavo API error during report generation");
                return StatusCode(500, "Failed to generate report due to API error");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error during report generation");
                return StatusCode(500, "An unexpected error occurred");
            }
        }

        [HttpGet("{reportId}")]
        [ProducesResponseType(typeof(ReportResult), StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> GetReportStatus(string reportId)
        {
            try
            {
                var result = await _tavoClient.GetReportStatusAsync(reportId);

                if (result == null)
                {
                    return NotFound($"Report with ID {reportId} not found");
                }

                return Ok(result);
            }
            catch (TavoApiException ex)
            {
                _logger.LogError(ex, "Tavo API error getting report {ReportId}", reportId);
                return StatusCode(500, "Failed to get report status");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error getting report {ReportId}", reportId);
                return StatusCode(500, "An unexpected error occurred");
            }
        }

        [HttpGet("{reportId}/download")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        public async Task<IActionResult> DownloadReport(string reportId)
        {
            try
            {
                var content = await _tavoClient.DownloadReportAsync(reportId);

                // Determine content type based on format
                var contentType = GetContentType("pdf"); // Default to PDF

                // Try to get format from report status
                try
                {
                    var reportStatus = await _tavoClient.GetReportStatusAsync(reportId);
                    contentType = GetContentType(reportStatus.Format);
                }
                catch
                {
                    // Use default content type if we can't get report status
                }

                return File(content, contentType, $"report.{GetFileExtension(contentType)}");
            }
            catch (TavoApiException ex)
            {
                _logger.LogError(ex, "Tavo API error downloading report {ReportId}", reportId);
                return StatusCode(500, "Failed to download report");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error downloading report {ReportId}", reportId);
                return StatusCode(500, "An unexpected error occurred");
            }
        }

        private static string GetContentType(string format)
        {
            return format.ToLower() switch
            {
                "pdf" => "application/pdf",
                "json" => "application/json",
                "html" => "text/html",
                _ => "application/octet-stream"
            };
        }

        private static string GetFileExtension(string contentType)
        {
            return contentType switch
            {
                "application/pdf" => "pdf",
                "application/json" => "json",
                "text/html" => "html",
                _ => "bin"
            };
        }
    }
}
```

## Background Services

### Scan Processing Service

```csharp
// Services/ScanProcessingService.cs
using TavoAI.Client.Interfaces;
using TavoAI.Client.Models;

namespace TavoAI.Web.Services
{
    public class ScanProcessingService : BackgroundService
    {
        private readonly IServiceProvider _serviceProvider;
        private readonly ILogger<ScanProcessingService> _logger;
        private readonly ConcurrentDictionary<string, CancellationTokenSource> _activeScans;

        public ScanProcessingService(
            IServiceProvider serviceProvider,
            ILogger<ScanProcessingService> logger)
        {
            _serviceProvider = serviceProvider;
            _logger = logger;
            _activeScans = new ConcurrentDictionary<string, CancellationTokenSource>();
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _logger.LogInformation("Scan Processing Service is starting.");

            stoppingToken.Register(() =>
                _logger.LogInformation("Scan Processing Service is stopping."));

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    // Process any pending scans
                    await ProcessPendingScansAsync(stoppingToken);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error in scan processing loop");
                }

                await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
            }
        }

        public void StartScanProcessing(string scanId)
        {
            if (_activeScans.ContainsKey(scanId))
            {
                _logger.LogWarning("Scan {ScanId} is already being processed", scanId);
                return;
            }

            var cts = new CancellationTokenSource();
            _activeScans[scanId] = cts;

            Task.Run(() => ProcessScanAsync(scanId, cts.Token));
        }

        private async Task ProcessScanAsync(string scanId, CancellationToken cancellationToken)
        {
            try
            {
                _logger.LogInformation("Starting background processing for scan {ScanId}", scanId);

                using var scope = _serviceProvider.CreateScope();
                var tavoClient = scope.ServiceProvider.GetRequiredService<ITavoClient>();

                // Wait for scan to complete
                while (!cancellationToken.IsCancellationRequested)
                {
                    var status = await tavoClient.GetScanStatusAsync(scanId);

                    if (status.Status == "completed" || status.Status == "failed")
                    {
                        _logger.LogInformation(
                            "Scan {ScanId} finished with status: {Status}",
                            scanId,
                            status.Status);

                        // Here you could send notifications, update database, etc.
                        break;
                    }

                    await Task.Delay(TimeSpan.FromSeconds(10), cancellationToken);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing scan {ScanId}", scanId);
            }
            finally
            {
                _activeScans.TryRemove(scanId, out _);
            }
        }

        private async Task ProcessPendingScansAsync(CancellationToken cancellationToken)
        {
            // This could check a database for pending scans and process them
            // For now, it's a placeholder for future implementation
            await Task.CompletedTask;
        }
    }
}
```

### Update Program.cs for Background Service

```csharp
// Program.cs (updated)
using TavoAI.Web.Services;

var builder = WebApplication.CreateBuilder(args);

// ... existing code ...

// Add background services
builder.Services.AddHostedService<ScanProcessingService>();

// ... rest of the code ...
```

## Middleware

### Rate Limiting Middleware

```csharp
// Middleware/RateLimitingMiddleware.cs
using System.Collections.Concurrent;

namespace TavoAI.Web.Middleware
{
    public class RateLimitingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<RateLimitingMiddleware> _logger;
        private readonly ConcurrentDictionary<string, ClientRequestInfo> _clients;

        public RateLimitingMiddleware(
            RequestDelegate next,
            ILogger<RateLimitingMiddleware> logger)
        {
            _next = next;
            _logger = logger;
            _clients = new ConcurrentDictionary<string, ClientRequestInfo>();
        }

        public async Task InvokeAsync(HttpContext context)
        {
            var clientId = GetClientId(context);
            var clientInfo = _clients.GetOrAdd(clientId, _ => new ClientRequestInfo());

            // Clean old requests
            clientInfo.CleanOldRequests();

            // Check rate limit (100 requests per minute)
            if (clientInfo.RequestCount >= 100)
            {
                _logger.LogWarning("Rate limit exceeded for client {ClientId}", clientId);
                context.Response.StatusCode = StatusCodes.Status429TooManyRequests;
                await context.Response.WriteAsync("Too many requests. Please try again later.");
                return;
            }

            // Add current request
            clientInfo.AddRequest();

            await _next(context);
        }

        private static string GetClientId(HttpContext context)
        {
            // Use IP address as client identifier
            return context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        }
    }

    public class ClientRequestInfo
    {
        private readonly List<DateTime> _requests = new();
        private readonly TimeSpan _window = TimeSpan.FromMinutes(1);

        public int RequestCount => _requests.Count;

        public void AddRequest()
        {
            _requests.Add(DateTime.UtcNow);
        }

        public void CleanOldRequests()
        {
            var cutoff = DateTime.UtcNow - _window;
            _requests.RemoveAll(r => r < cutoff);
        }
    }
}
```

### Exception Handling Middleware

```csharp
// Middleware/ExceptionHandlingMiddleware.cs
using TavoAI.Client.Exceptions;

namespace TavoAI.Web.Middleware
{
    public class ExceptionHandlingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<ExceptionHandlingMiddleware> _logger;

        public ExceptionHandlingMiddleware(
            RequestDelegate next,
            ILogger<ExceptionHandlingMiddleware> logger)
        {
            _next = next;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (TavoApiException ex)
            {
                _logger.LogError(ex, "Tavo API exception");
                await HandleExceptionAsync(context, ex, StatusCodes.Status502BadGateway);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected exception");
                await HandleExceptionAsync(context, ex, StatusCodes.Status500InternalServerError);
            }
        }

        private static async Task HandleExceptionAsync(
            HttpContext context,
            Exception exception,
            int statusCode)
        {
            context.Response.StatusCode = statusCode;
            context.Response.ContentType = "application/json";

            var errorResponse = new
            {
                error = new
                {
                    message = exception.Message,
                    type = exception.GetType().Name
                }
            };

            await context.Response.WriteAsJsonAsync(errorResponse);
        }
    }
}
```

### Update Program.cs for Middleware

```csharp
// Program.cs (updated)
using TavoAI.Web.Middleware;

var builder = WebApplication.CreateBuilder(args);

// ... existing code ...

var app = builder.Build();

// Add custom middleware
app.UseMiddleware<ExceptionHandlingMiddleware>();
app.UseMiddleware<RateLimitingMiddleware>();

// ... rest of the code ...
```

## Testing

### Unit Tests

```csharp
// Tests/TavoClientTests.cs
using Moq;
using System.Net;
using TavoAI.Client.Clients;
using TavoAI.Client.Exceptions;

namespace TavoAI.Client.Tests
{
    public class TavoClientTests
    {
        private readonly Mock<HttpMessageHandler> _httpMessageHandler;
        private readonly HttpClient _httpClient;
        private readonly Mock<ILogger<TavoClient>> _logger;
        private readonly TavoClient _tavoClient;

        public TavoClientTests()
        {
            _httpMessageHandler = new Mock<HttpMessageHandler>();
            _httpClient = new HttpClient(_httpMessageHandler.Object);
            _logger = new Mock<ILogger<TavoClient>>();
            _tavoClient = new TavoClient(_httpClient, _logger.Object);
        }

        [Fact]
        public async Task ScanCodeAsync_ValidRequest_ReturnsScanResult()
        {
            // Arrange
            var expectedResult = new ScanResult
            {
                Id = "test-scan-id",
                Status = "completed",
                Name = "Test Scan"
            };

            SetupHttpResponse(HttpStatusCode.OK, expectedResult);

            // Act
            var result = await _tavoClient.ScanCodeAsync("Console.WriteLine(\"test\");", "csharp");

            // Assert
            Assert.NotNull(result);
            Assert.Equal("test-scan-id", result.Id);
            Assert.Equal("completed", result.Status);
        }

        [Fact]
        public async Task ScanCodeAsync_ApiError_ThrowsTavoApiException()
        {
            // Arrange
            SetupHttpResponse(HttpStatusCode.InternalServerError, "Server error");

            // Act & Assert
            await Assert.ThrowsAsync<TavoApiException>(
                () => _tavoClient.ScanCodeAsync("invalid code", "csharp"));
        }

        private void SetupHttpResponse<T>(HttpStatusCode statusCode, T content)
        {
            var response = new HttpResponseMessage(statusCode);
            response.Content = JsonContent.Create(content);

            _httpMessageHandler
                .Protected()
                .Setup<Task<HttpResponseMessage>>(
                    "SendAsync",
                    ItExpr.IsAny<HttpRequestMessage>(),
                    ItExpr.IsAny<CancellationToken>())
                .ReturnsAsync(response);
        }
    }
}
```

### Integration Tests

```csharp
// Tests/ScansControllerIntegrationTests.cs
using Microsoft.AspNetCore.Mvc.Testing;
using System.Net.Http.Json;

namespace TavoAI.Web.Tests
{
    public class ScansControllerIntegrationTests : IClassFixture<WebApplicationFactory<Program>>
    {
        private readonly WebApplicationFactory<Program> _factory;
        private readonly HttpClient _client;

        public ScansControllerIntegrationTests(WebApplicationFactory<Program> factory)
        {
            _factory = factory;
            _client = _factory.CreateClient();
        }

        [Fact]
        public async Task CreateScan_ValidCodeScan_ReturnsSuccess()
        {
            // Arrange
            var request = new
            {
                name = "Integration Test Scan",
                target = "Console.WriteLine(\"Hello World\");",
                scanType = "code",
                language = "csharp"
            };

            // Act
            var response = await _client.PostAsJsonAsync("/api/scans", request);

            // Assert
            response.EnsureSuccessStatusCode();
            var result = await response.Content.ReadFromJsonAsync<ScanResult>();
            Assert.NotNull(result);
            Assert.NotEmpty(result.Id);
        }

        [Fact]
        public async Task CreateScan_InvalidScanType_ReturnsBadRequest()
        {
            // Arrange
            var request = new
            {
                name = "Invalid Scan",
                target = "test",
                scanType = "invalid"
            };

            // Act
            var response = await _client.PostAsJsonAsync("/api/scans", request);

            // Assert
            Assert.Equal(System.Net.HttpStatusCode.BadRequest, response.StatusCode);
        }
    }
}
```

## Docker Configuration

### Dockerfile

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src
COPY ["TavoAI.Web/TavoAI.Web.csproj", "TavoAI.Web/"]
COPY ["TavoAI.Client/TavoAI.Client.csproj", "TavoAI.Client/"]
RUN dotnet restore "TavoAI.Web/TavoAI.Web.csproj"
COPY . .
WORKDIR "/src/TavoAI.Web"
RUN dotnet build "TavoAI.Web.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "TavoAI.Web.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "TavoAI.Web.dll"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  tavo-aspnet:
    build: .
    ports:
      - "8080:80"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ASPNETCORE_URLS=http://+:80
    volumes:
      - ./appsettings.Production.json:/app/appsettings.Production.json
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add SQL Server for data persistence
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=YourStrong!Passw0rd
    ports:
      - "1433:1433"
    volumes:
      - sqlserver_data:/var/opt/mssql
    restart: unless-stopped

volumes:
  sqlserver_data:
```

### Production appsettings.Production.json

```json
{
  "Tavo": {
    "ApiKey": "your-production-api-key",
    "BaseUrl": "https://api.tavoai.net",
    "TimeoutSeconds": 30
  },
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "Microsoft.AspNetCore": "Warning",
      "TavoAI": "Information"
    }
  },
  "AllowedHosts": "*"
}
```

## Deployment

### Publish Profile

```xml
<!-- Properties/PublishProfiles/FolderProfile.pubxml -->
<Project>
  <PropertyGroup>
    <Configuration>Release</Configuration>
    <Platform>Any CPU</Platform>
    <PublishDir>bin\Release\net7.0\publish\</PublishDir>
    <SelfContained>true</SelfContained>
    <RuntimeIdentifier>linux-x64</RuntimeIdentifier>
    <PublishSingleFile>false</PublishSingleFile>
    <PublishTrimmed>true</PublishTrimmed>
  </PropertyGroup>
</Project>
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure

on:
  push:
    branches: [ main ]

env:
  AZURE_WEBAPP_NAME: tavo-aspnet-webapp
  AZURE_WEBAPP_PACKAGE_PATH: './published'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup .NET
      uses: actions/setup-dotnet@v3
      with:
        dotnet-version: '7.0.x'

    - name: Restore dependencies
      run: dotnet restore

    - name: Build
      run: dotnet build --configuration Release --no-restore

    - name: Test
      run: dotnet test --no-restore --verbosity normal

    - name: Publish
      run: dotnet publish ./TavoAI.Web/TavoAI.Web.csproj -c Release -o ${{ env.AZURE_WEBAPP_PACKAGE_PATH }}

    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: ${{ env.AZURE_WEBAPP_NAME }}
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        package: ${{ env.AZURE_WEBAPP_PACKAGE_PATH }}
```

This ASP.NET Core integration provides a robust, enterprise-ready interface for Tavo AI security scanning with dependency injection, comprehensive error handling, background processing, rate limiting, and production deployment configurations.
