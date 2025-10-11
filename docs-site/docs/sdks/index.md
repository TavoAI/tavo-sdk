# SDK Guides

Welcome to the Tavo AI SDK documentation. Choose your programming language to get started with comprehensive guides, examples, and API references.

## Available SDKs

### [Python SDK](./python/)
The official Python SDK for Tavo AI, featuring async-first design, full type hints, and comprehensive security scanning capabilities.

**Key Features:**
- Async/await support
- Full type annotations
- Comprehensive error handling
- Built-in retry logic
- Framework integrations (Django, FastAPI, Flask)

### [JavaScript/TypeScript SDK](./javascript/)
Modern ES6+ SDK for Node.js and browser environments with TypeScript support.

**Key Features:**
- TypeScript definitions included
- Browser and Node.js compatible
- Promise-based API
- Framework integrations (Express, React, Vue)
- Tree-shaking friendly

### [Java SDK](./java/)
Enterprise-grade Java SDK with Spring Boot integration and comprehensive security features.

**Key Features:**
- Spring Boot starter
- Reactive programming support
- Comprehensive error handling
- Maven and Gradle support
- Enterprise security features

### [Go SDK](./go/)
Idiomatic Go SDK with context support and high performance.

**Key Features:**
- Context-aware operations
- High performance
- Comprehensive error handling
- Go modules support
- Built-in concurrency patterns

### [.NET SDK](./dotnet/)
Cross-platform .NET SDK supporting .NET Core, .NET Framework, and .NET 5+.

**Key Features:**
- Cross-platform support
- Async/await throughout
- Dependency injection friendly
- Comprehensive error handling
- NuGet package distribution

### [Rust SDK](./rust/)
High-performance Rust SDK with memory safety and zero-cost abstractions.

**Key Features:**
- Memory safe
- Zero-cost abstractions
- High performance
- Comprehensive error handling
- Cargo package distribution

## Getting Started

1. **Choose your language** from the list above
2. **Install the SDK** using your package manager
3. **Set up authentication** with your API key
4. **Start scanning** code for security vulnerabilities

## Quick Examples

### Python
```python
from tavo_ai import TavoClient

client = TavoClient(api_key="your-api-key")
result = await client.scan_code("print('hello')", language="python")
print(f"Found {result.total_issues} issues")
```

### JavaScript
```javascript
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient({ apiKey: 'your-api-key' });
const result = await client.scans().scanCode("console.log('hello')", 'javascript');
console.log(`Found ${result.totalIssues} issues`);
```

### Java
```java
import net.tavoai.TavoClient;

TavoClient client = new TavoClient("your-api-key");
ScanResult result = client.getScans().scanCode("System.out.println(\"hello\")", "java");
System.out.println("Found " + result.getTotalIssues() + " issues");
```

### Go
```go
client := tavo.NewClient(&tavo.Config{APIKey: "your-api-key"})
result, _ := client.Scans().ScanCode("fmt.Println(\"hello\")", "go")
fmt.Printf("Found %d issues\n", result.TotalIssues)
```

### .NET
```csharp
var client = new TavoClient("your-api-key");
var result = await client.Scans.ScanCodeAsync("Console.WriteLine(\"hello\")", "csharp");
Console.WriteLine($"Found {result.TotalIssues} issues");
```

### Rust
```rust
let client = TavoClient::new("your-api-key")?;
let result = client.scans().scan_code("println!(\"hello\")", "rust").await?;
println!("Found {} issues", result.total_issues);
```

## Support

- 📖 [API Reference](../api-reference/overview.md)
- 🐛 [GitHub Issues](https://github.com/tavoai/tavo-api/issues)
- 💬 [Community Discussions](https://github.com/tavoai/tavo-api/discussions)
- 📧 [Support Email](mailto:support@tavoai.org)

## Contributing

We welcome contributions to our SDKs! Please see our [Contributing Guide](https://github.com/tavoai/tavo-api/blob/main/CONTRIBUTING.md) for details.