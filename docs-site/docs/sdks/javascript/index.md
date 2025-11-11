# TypeScript SDK

The Tavo AI TypeScript SDK provides generated API clients for all platform endpoints plus integrated tavo-scanner execution capabilities. Built with TypeScript for full type safety and modern async patterns.

## Installation

```bash
npm install @tavoai/sdk
```

or

```bash
yarn add @tavoai/sdk
```

## Architecture

The TypeScript SDK provides a modern, modular architecture with generated API clients and integrated scanner capabilities.

### Modular API Clients

The SDK provides **26 specialized client classes** for different API endpoint categories, each with full TypeScript types and async methods:

#### Core Scanning (`client.scans`, `client.scanManagement`, etc.)
```typescript
// Scan management operations
const scanClient = client.scanManagement;
const result = await scanClient.createScan({
  repositoryUrl: "https://github.com/your-org/your-repo",
  scanType: "security",
  branch: "main"
});

// Scan tools and rules
const toolsClient = client.scanTools;
const rulesClient = client.scanRules;
```

#### AI Analysis (`client.aiAnalysis`, `client.aiAnalysisCore`, etc.)
```typescript
// AI-powered analysis
const aiClient = client.aiAnalysis;
const analysis = await aiClient.analyzeCode({
  code: "console.log('hello')",
  language: "javascript"
});

// Risk compliance checking
const complianceClient = client.aiRiskCompliance;
const report = await complianceClient.checkCompliance({ scanId: "123" });
```

#### Repository & Registry Management
```typescript
// Repository operations
const repoClient = client.repositories;
const connectionsClient = client.repositoryConnections;

// Plugin marketplace
const marketplaceClient = client.pluginMarketplace;
const plugins = await marketplaceClient.listPlugins();
```

#### Authentication & Device Management
```typescript
// Device authentication flow
const authClient = client.deviceAuth;
const authResult = await authClient.postCode({
  clientId: "your-client-id",
  clientName: "my-security-scanner"
});
```

### Scanner Integration

Advanced scanner integration with modern async patterns:
- **Promise-based async execution** with proper error handling
- **Plugin and rule management** with TypeScript validation
- **Automatic binary discovery** (relative paths, PATH, and custom locations)
- **Structured result parsing** with comprehensive type safety
- **Progress monitoring** and cancellation support
- **Memory-efficient streaming** for large scan outputs

## Quick Start

```typescript
import { TavoSdk } from '@tavoai/sdk';

async function main() {
  // Initialize API client with modular architecture
  const client = TavoSdk.createClient({ apiKey: 'your-api-key' });

  // 1. Device authentication
  const authClient = client.deviceAuth;
  const authResult = await authClient.postCode({
    clientId: 'your-client-id',
    clientName: 'my-security-scanner'
  });
  console.log('Device auth successful:', authResult);

  // 2. Create and run a security scan
  const scanClient = client.scanManagement;
  const scanResult = await scanClient.createScan({
    repositoryUrl: 'https://github.com/your-org/your-repo',
    scanType: 'security',
    branch: 'main'
  });
  console.log('Scan created:', scanResult);

  // 3. Get AI-powered analysis
  const aiClient = client.aiAnalysis;
  const analysis = await aiClient.analyzeScan({ scanId: scanResult.id });
  console.log('AI analysis found issues:', analysis.vulnerabilities.length);

  // 4. Alternative: Use integrated scanner
  const scanner = TavoSdk.createScanner();
  const localResult = await scanner.scanDirectory('./my-project', {
    plugins: ['security', 'performance'],
    rules: ['custom-security-rules']
  });
  console.log('Local scan found issues:', localResult.totalIssues);
}

main().catch(console.error);
```

## Client Architecture

The `TavoSdk` client provides access to all API endpoints through modular client properties:

```typescript
const client = TavoSdk.createClient({ apiKey: 'your-key' });

// Access different API categories
client.deviceAuth        // Device authentication
client.scanManagement    // Scan lifecycle management
client.aiAnalysis        // AI-powered analysis
client.repositories      // Repository operations
client.pluginMarketplace // Plugin management
client.registry          // Registry operations
// ... and 20+ more specialized clients
```

Each client provides fully typed async methods matching the REST API:

```typescript
// Type hints and IDE completion
const result: ScanResult = await client.scanManagement.createScan({
  repositoryUrl: "https://github.com/user/repo",
  scanType: "security"
});
```

## Error Handling

The SDK provides comprehensive error handling with specific exception types:

```typescript
import { TavoSdk, TavoApiError, AuthenticationError } from '@tavoai/sdk';

try {
  const client = TavoSdk.createClient({ apiKey: 'invalid-key' });
  const result = await client.health.getStatus();
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.log('Auth failed:', error.message);
  } else if (error instanceof TavoApiError) {
    console.log(`API error: ${error.statusCode} - ${error.message}`);
  } else {
    console.error('Unexpected error:', error);
  }
}
```

## Best Practices

### Connection Management
```typescript
// Reuse client instances for multiple requests
const client = TavoSdk.createClient({ apiKey: 'your-key' });

// Client automatically handles connection pooling
const [scans, repos, models] = await Promise.all([
  client.scanManagement.listScans(),
  client.repositories.listRepositories(),
  client.aiAnalysis.getModels()
]);
```

### Timeout Configuration
```typescript
// Configure timeouts for long-running operations
const client = TavoSdk.createClient({
  apiKey: 'your-key',
  timeout: 30000  // milliseconds
});
```

### Logging
```typescript
// Enable debug logging
const client = TavoSdk.createClient({
  apiKey: 'your-key',
  debug: true
});
// All requests now logged with timing and errors
```

## Authentication

```typescript
import { TavoSdk } from '@tavoai/sdk';

// API Key authentication (recommended)
const client = TavoSdk.CreateClient('your-api-key');

// JWT Token authentication  
const client = TavoSdk.CreateClientWithAuth('your-jwt-token');

// Device token authentication
const client = TavoSdk.CreateClientWithDeviceToken('your-device-token');
```

## API Client Usage

Access all platform endpoints through the generated client:

```typescript
const client = TavoSdk.CreateClient('your-api-key');

// Authentication operations
const authResult = await client.deviceAuth.postCode({
  clientId: '123',
  clientName: 'my-app'
});

// Scanning operations
const scanResult = await client.scanTools.getScan('scan-id');
const bulkResult = await client.scanBulkOperations.createBulkScan(scanConfigs);

// AI Analysis
const analysis = await client.aiAnalysis.analyzeCode('code', 'typescript');

// Jobs management
const jobs = await client.jobs.listJobs();
const jobStatus = await client.jobs.getJob('job-id');

// Health checks
const health = await client.health.healthCheck();
```

## Scanner Integration

Execute tavo-scanner as a subprocess with full configuration:

```typescript
import { TavoSdk } from '@tavoai/sdk';

// Basic scanning
const scanner = TavoSdk.CreateScanner();
const result = await scanner.scanDirectory('./my-project');

// Advanced scanning with plugins
const result = await scanner.scanWithPlugins('./my-project', ['security', 'performance']);

// Custom rules and configuration
const result = await scanner.scanWithRules('./my-project', './custom-rules.json');
```

## Available Endpoint Clients

The SDK provides 24+ generated endpoint clients:

| Client | Purpose |
|--------|---------|
| `deviceAuth` | Device authentication and tokens |
| `scanTools` | Core scanning operations |
| `scanManagement` | Scan lifecycle management |
| `scanRules` | Scan rule configuration |
| `scanSchedules` | Scheduled scanning |
| `scanBulkOperations` | Bulk scan operations |
| `scannerIntegration` | Scanner integrations |
| `aiAnalysis` | AI-powered code analysis |
| `aiBulkOperations` | Bulk AI operations |
| `aiPerformanceQuality` | Performance analysis |
| `aiResultsExport` | Export analysis results |
| `aiRiskCompliance` | Risk and compliance analysis |
| `registry` | Plugin/registry management |
| `pluginExecution` | Plugin execution |
| `pluginMarketplace` | Plugin marketplace |
| `rules` | Rule management |
| `codeSubmission` | Code submission for analysis |
| `repositories` | Repository management |
| `repositoryConnections` | Repository connections |
| `repositoryProviders` | Repository provider integrations |
| `repositoryWebhooks` | Repository webhooks |
| `jobs` | Background job management |
| `health` | Health check endpoints |

## Scanner Configuration

Configure scanner behavior and plugins:

```typescript
import { TavoSdk, ScannerConfig } from '@tavoai/sdk';

// Configure scanner
const config: Partial<ScannerConfig> = {
  plugins: ['security', 'performance'],
  rulesPath: './custom-rules.json',
  timeout: 600, // 10 minutes
  outputFormat: 'sarif'
};

const scanner = new TavoSdk.TavoScanner(config);

// Or use factory methods
const scanner = TavoSdk.CreateScannerWithPlugins('security', 'performance');
const scanner = TavoSdk.CreateScannerWithRules('./rules.json');
```

## Error Handling

The SDK provides comprehensive error handling:

```typescript
import { TavoSdk } from '@tavoai/sdk';

async function robustScan() {
  const client = TavoSdk.CreateClient('your-api-key');
  const scanner = TavoSdk.CreateScanner();

  try {
    // API operations with automatic retries
    const result = await client.health.healthCheck();

    // Scanner execution with timeout handling
    const scanResult = await scanner.scanDirectory('./project');

  } catch (error) {
    console.error('Operation failed:', error);
    // SDK handles retries, timeouts, and error parsing automatically
  }
}
```

## Type Definitions

The SDK includes comprehensive TypeScript definitions in `packages/typescript/src/types/`:

```typescript
import { 
  ScanResult, 
  ScanOptions, 
  PaginationInfo,
  ListResponse 
} from '@tavoai/sdk';

// All API responses are fully typed
const result: ScanResult = await client.scanTools.getScan('scan-id');
const list: ListResponse<ScanResult> = await client.scanTools.listScans();
```

## Contributing

The TypeScript SDK is generated from the Tavo AI API specification. To contribute:

1. **API Changes**: Modify the API specification in the main Tavo repository
2. **Regeneration**: Run the generation script to update client code
3. **Testing**: Add tests for new functionality  
4. **Documentation**: Update this guide for new features

## Support

- 📖 [API Reference](../../api-reference/overview.md)
- 🐛 [GitHub Issues](https://github.com/tavoai/tavo-sdk/issues)
- 💬 [Community Discussions](https://github.com/tavoai/tavo-sdk/discussions)
