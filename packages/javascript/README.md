# @tavoai/sdk

JavaScript/TypeScript SDK for Tavo AI API

## Installation

```bash
npm install @tavoai/sdk
# or
yarn add @tavoai/sdk
```

## Usage

### Basic Usage

```javascript
import { TavoClient } from '@tavoai/sdk';

// Initialize client
const client = new TavoClient({
  apiKey: 'your-api-key-here'
});

// Health check
const health = await client.healthCheck();
console.log('API Status:', health.status);
```

### Advanced Usage

```javascript
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient({
  apiKey: process.env.TAVO_API_KEY,
  baseURL: 'https://api.tavoai.net' // optional
});

// Scan a repository
const scan = await client.scans.create({
  repositoryUrl: 'https://github.com/user/repo',
  scanType: 'security'
});

console.log('Scan created:', scan.id);

// Get scan results
const results = await client.scans.getResults(scan.id);
console.log('Vulnerabilities found:', results.vulnerabilities.length);
```

### TypeScript Support

```typescript
import { TavoClient, ScanResult, Vulnerability } from '@tavoai/sdk';

const client = new TavoClient({
  apiKey: 'your-api-key'
});

// Full type safety
const scan: ScanResult = await client.scans.create({
  repositoryUrl: 'https://github.com/user/repo'
});
```

## API Reference

### TavoClient

Main client class for interacting with Tavo AI API.

#### Constructor Options

- `apiKey` (string): Your Tavo AI API key
- `baseURL` (string, optional): API base URL (defaults to production)
- `timeout` (number, optional): Request timeout in milliseconds

#### Methods

- `healthCheck()`: Check API availability
- `scans.create(options)`: Create a new scan
- `scans.getResults(scanId)`: Get scan results
- `scans.list()`: List all scans

## Authentication

Get your API key from [Tavo AI Dashboard](https://app.tavoai.net).

```bash
export TAVO_API_KEY="your-api-key"
```

## Requirements

- Node.js 16+
- npm or yarn

## License

Apache-2.0

## Support

- [Documentation](https://docs.tavoai.net)
- [GitHub Issues](https://github.com/TavoAI/tavo-api/issues)
- [Community Forum](https://community.tavoai.net)