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

The TypeScript SDK provides two main components:

### API Clients
Generated Promise-based clients for all Tavo AI REST API endpoints located in `packages/typescript/src/endpoints/`:
- `DeviceAuthClient` - Device authentication operations  
- `ScanToolsClient` - Core scanning functionality
- `AiAnalysisClient` - AI-powered code analysis
- And 21+ additional endpoint clients

### Scanner Integration
Built-in tavo-scanner wrapper in `packages/typescript/src/scanner.ts`:
- Child process execution of tavo-scanner binary
- Plugin and rule configuration management
- Automatic binary discovery
- Promise-based async execution

## Quick Start

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
