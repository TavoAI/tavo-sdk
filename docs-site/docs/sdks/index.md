# SDK Guides

Welcome to the Tavo AI SDK documentation. Our SDKs provide comprehensive access to the Tavo AI platform, including REST API clients for all endpoints and integrated tavo-scanner execution capabilities.

## Available SDKs

### [Python SDK](./python/)
Modern Python SDK with async API clients and scanner integration.

**Key Features:**
- Async/await API clients for all endpoints
- Integrated tavo-scanner subprocess execution
- Plugin and rule configuration management
- Full type annotations and error handling
- Automatic scanner binary discovery

### [TypeScript SDK](./javascript/)
TypeScript-first SDK with Promise-based API clients and scanner integration.

**Key Features:**
- Generated API clients for all endpoints
- Integrated tavo-scanner execution
- TypeScript interfaces and type safety
- Plugin/rule configuration support
- Browser and Node.js compatible

### [Java SDK](./java/)
Enterprise Java SDK with async API clients and scanner integration.

**Key Features:**
- Generated API clients for all endpoints
- Integrated tavo-scanner subprocess execution
- CompletableFuture-based async operations
- Plugin and rule management
- Maven/Gradle integration

### [Go SDK](./go/)
High-performance Go SDK with context-aware API clients and scanner integration.

**Key Features:**
- Generated API clients for all endpoints
- Integrated tavo-scanner execution
- Context-based timeout handling
- Plugin/rule configuration
- Go modules support

### [.NET SDK](./dotnet/)
Cross-platform .NET SDK with async API clients and scanner integration.

**Key Features:**
- Generated API clients for all endpoints
- Integrated tavo-scanner execution
- Async/await throughout
- Plugin and rule management
- NuGet package distribution

### [Rust SDK](./rust/)
Memory-safe Rust SDK with async API clients and scanner integration.

**Key Features:**
- Generated API clients for all endpoints
- Integrated tavo-scanner execution
- Tokio async runtime integration
- Plugin/rule configuration
- Cargo package distribution

## Getting Started

1. **Choose your language** from the list above
2. **Install the SDK** using your package manager
3. **Set up authentication** with your API key or device token
4. **Use API clients** to access all platform endpoints
5. **Execute scans** using the integrated scanner wrapper

## SDK Architecture

Each SDK provides two main components:

### API Clients
Generated clients for all Tavo AI REST API endpoints, providing:
- Type-safe method calls
- Automatic authentication
- Error handling and retries
- Request/response serialization

### Scanner Integration
Built-in tavo-scanner execution with:
- Subprocess management
- Plugin and rule configuration
- Result parsing and handling
- Automatic binary discovery

## Quick Examples

### Python
```python
from tavo import TavoClient, TavoScanner

# API client usage
client = TavoClient(api_key="your-api-key")
result = await client.device_auth.post_code(client_id="123", client_name="test")

# Scanner usage
scanner = TavoScanner()
scan_result = await scanner.scan_directory("./my-project", plugins=["security", "performance"])
```

### TypeScript
```typescript
import { TavoSdk } from '@tavoai/sdk';

// API client usage
const client = TavoSdk.CreateClient('your-api-key');
const result = await client.deviceAuth.postCode({ clientId: '123', clientName: 'test' });

// Scanner usage
const scanner = TavoSdk.CreateScanner();
const scanResult = await scanner.scanDirectory('./my-project', {
  plugins: ['security', 'performance']
});
```

### Java
```java
import net.tavoai.sdk.TavoSdk;

// API client usage
TavoClient client = TavoSdk.createClient("your-api-key");
CompletableFuture<ScanResult> result = client.getDeviceAuth()
    .postCodeAsync("123", "test");

// Scanner usage
TavoScanner scanner = TavoSdk.createScanner();
CompletableFuture<ScanResult> scanResult = scanner.scanDirectory("./my-project", scanOptions);
```

### Go
```go
import "github.com/tavo-ai/sdk-go/sdk"

// API client usage
client := sdk.CreateClientWithAuth("your-api-key", "", "")
result, err := client.DeviceAuth.PostCode("123", "test")

// Scanner usage
scanner := sdk.CreateScanner()
scanResult, err := scanner.ScanDirectory("./my-project", &scanner.ScanOptions{
    Plugins: []string{"security", "performance"},
})
```

### .NET
```csharp
using TavoAI;

// API client usage
var client = TavoSdk.CreateClient("your-api-key");
var result = await client.DeviceAuth.PostCodeAsync("123", "test");

// Scanner usage
var scanner = TavoSdk.CreateScanner();
var scanResult = await scanner.ScanDirectoryAsync("./my-project", new ScanOptions {
    Plugins = new[] { "security", "performance" }
});
```

### Rust
```rust
use tavo_sdk::{create_client, create_scanner};

// API client usage
let client = create_client_with_auth(Some("your-api-key".to_string()), None, None);
let result = client.device_auth.post_code("123".to_string(), Some("test".to_string())).await?;

// Scanner usage
let scanner = create_scanner_with_plugins(vec!["security".to_string(), "performance".to_string()]);
let scan_result = scanner.scan_directory("./my-project", None).await?;
```

## Support

- 📖 [API Reference](../api-reference/overview.md)
- 🐛 [GitHub Issues](https://github.com/tavoai/tavo-sdk/issues)
- 💬 [Community Discussions](https://github.com/tavoai/tavo-sdk/discussions)
- 📧 [Support Email](mailto:support@tavoai.org)

## Contributing

We welcome contributions to our SDKs! Please see our [Contributing Guide](https://github.com/tavoai/tavo-sdk/blob/main/CONTRIBUTING.md) for details.