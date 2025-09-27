# Tavo AI .NET SDK

The official Tavo AI SDK for .NET applications, providing comprehensive security scanning and AI model analysis capabilities.

## Installation

```bash
dotnet add package TavoAI
```

Or add to your `.csproj` file:

```xml
<PackageReference Include="TavoAI" Version="1.0.0" />
```

## Quick Start

```csharp
using TavoAI;

// Initialize the client
var client = new TavoClient("your-api-key-here");

// Scan code for vulnerabilities
var scanResult = await client.ScanCodeAsync(@"
    using System;
    public class Example {
        public void ProcessUserInput(string input) {
            // Potential SQL injection vulnerability
            var query = ""SELECT * FROM users WHERE id = '"" + input + ""'"";
        }
    }
", "csharp");

Console.WriteLine($"Found {scanResult.TotalIssues} issues");

// Analyze AI model
var modelConfig = new {
    model_type = "transformer",
    parameters = new { layers = 12, heads = 8 }
};

var analysis = await client.AnalyzeModelAsync(modelConfig);
Console.WriteLine($"Model is safe: {analysis.Safe}");
```

## Features

- **Security Scanning**: Comprehensive vulnerability detection for .NET code
- **AI Model Analysis**: Security assessment for machine learning models
- **Async Support**: Full async/await support for all operations
- **Type Safety**: Strongly typed responses and requests
- **Error Handling**: Comprehensive error handling and validation

## API Reference

### TavoClient

#### Constructor

```csharp
public TavoClient(string apiKey, string baseUrl = "https://api.tavoai.net")
```

#### Methods

##### ScanCodeAsync

```csharp
public async Task<ScanResult> ScanCodeAsync(string code, string language = "csharp")
```

Scans code for security vulnerabilities.

**Parameters:**

- `code`: The source code to scan
- `language`: Programming language (default: "csharp")

**Returns:** `ScanResult` with vulnerability information

##### AnalyzeModelAsync

```csharp
public async Task<ModelAnalysisResult> AnalyzeModelAsync(object modelConfig)
```

Analyzes AI model configuration for security risks.

**Parameters:**

- `modelConfig`: Model configuration object

**Returns:** `ModelAnalysisResult` with analysis results

## Configuration

### API Key

Get your API key from [gettavo.com](https://gettavo.com) and set it in your application:

```csharp
// Option 1: Constructor parameter
var client = new TavoClient("your-api-key-here");

// Option 2: Environment variable
var apiKey = Environment.GetEnvironmentVariable("TAVO_API_KEY");
var client = new TavoClient(apiKey);
```

### Custom Base URL

```csharp
var client = new TavoClient("your-api-key", "https://custom-api.tavoai.net");
```

## Error Handling

The SDK throws exceptions for API errors:

```csharp
try
{
    var result = await client.ScanCodeAsync(code);
}
catch (HttpRequestException ex)
{
    Console.WriteLine($"API request failed: {ex.Message}");
}
catch (JsonException ex)
{
    Console.WriteLine($"Response parsing failed: {ex.Message}");
}
```

## Examples

See the `examples/` directory for complete working examples.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
