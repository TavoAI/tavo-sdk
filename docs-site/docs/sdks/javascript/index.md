# JavaScript/TypeScript SDK

The Tavo AI JavaScript/TypeScript SDK provides a modern, promise-based interface for integrating with the Tavo AI platform. Built with TypeScript for excellent type safety and developer experience.

## Installation

```bash
npm install @tavoai/sdk
```

or

```bash
yarn add @tavoai/sdk
```

## Quick Start

```typescript
import { TavoClient } from '@tavoai/sdk';

// Initialize the client
const client = new TavoClient({
  apiKey: 'your-api-key'
});

// Scan code for vulnerabilities
async function scanCode() {
  try {
    const result = await client.scanCode({
      code: `
        function processUserInput(userInput) {
          const query = \`SELECT * FROM users WHERE id = '\${userInput}'\`;
          // Potential SQL injection vulnerability
          return executeQuery(query);
        }
      `,
      language: 'javascript'
    });

    console.log(\`Found \${result.totalIssues} issues\`);
    result.vulnerabilities.forEach(vuln => {
      console.log(\`- \${vuln.title}: \${vuln.description}\`);
    });
  } catch (error) {
    console.error('Scan failed:', error);
  }
}

scanCode();
```

## TypeScript Support

The SDK is written in TypeScript and provides full type definitions:

```typescript
import { TavoClient, ScanResult, Vulnerability, ScanOptions } from '@tavoai/sdk';

// Fully typed interfaces
const options: ScanOptions = {
  code: 'const x = 1;',
  language: 'javascript',
  timeout: 30
};

const result: ScanResult = await client.scanCode(options);
```

## Authentication

```typescript
import { TavoClient } from '@tavoai/sdk';

// API Key authentication
const client = new TavoClient({
  apiKey: 'your-api-key'
});

// Or with additional options
const client = new TavoClient({
  apiKey: 'your-api-key',
  baseURL: 'https://api-staging.tavoai.net',
  timeout: 30000
});
```

## Core Operations

### Code Scanning

```typescript
// Basic code scan
const result = await client.scanCode({
  code: codeString,
  language: 'javascript'
});

// Advanced scan with options
const result = await client.scanCode({
  code: codeString,
  language: 'typescript',
  timeout: 60,
  includeMetrics: true
});
```

### AI Model Analysis

```typescript
const modelConfig = {
  modelType: 'transformer',
  parameters: {
    layers: 12,
    heads: 8,
    hiddenSize: 768
  }
};

const analysis = await client.analyzeModel(modelConfig);
console.log(\`Model is safe: \${analysis.safe}\`);
```

### User Management

```typescript
// Get current user
const user = await client.users.getCurrentUser();

// Update user profile
const updatedUser = await client.users.update(user.id, {
  name: 'New Name',
  email: 'new@example.com'
});
```

### Organization Management

```typescript
// List organizations
const organizations = await client.organizations.list();

// Create new organization
const newOrg = await client.organizations.create({
  name: 'My Company',
  description: 'Security scanning service'
});
```

### Scan Jobs

```typescript
// Start a new scan job
const job = await client.jobs.create({
  targetUrl: 'https://example.com',
  scanType: 'full_scan'
});

// Get job status
const status = await client.jobs.get(job.id);

// List all jobs with pagination
const jobs = await client.jobs.list({
  limit: 10,
  offset: 0
});
```

### Webhooks

```typescript
// Create webhook
const webhook = await client.webhooks.create({
  url: 'https://myapp.com/webhook',
  events: ['scan.completed', 'vulnerability.found']
});

// List webhooks
const webhooks = await client.webhooks.list();

// Delete webhook
await client.webhooks.delete(webhook.id);
```

### API Key Management

```typescript
// List your API keys
const apiKeys = await client.apiKeys.list();

// Create a new API key
const newKey = await client.apiKeys.create('My API Key', {
  description: 'For production use'
});

// Update an API key
const updatedKey = await client.apiKeys.update(apiKeyId, 'Updated Name', {
  description: 'Updated description'
});

// Rotate an API key (generates new secret)
const rotatedKey = await client.apiKeys.rotate(apiKeyId);

// Delete an API key
await client.apiKeys.delete(apiKeyId);
```

### Report Management

```typescript
// Create a new report
const report = await client.reports.create({
  scanId: 'scan-uuid',
  reportType: 'scan_summary',
  format: 'pdf',
  title: 'Security Audit Report'
});

// Get report details
const reportDetails = await client.reports.get(reportId);

// List reports with filtering
const reports = await client.reports.list({
  limit: 10,
  reportType: 'scan_summary',
  status: 'completed'
});

// Update report
const updatedReport = await client.reports.update(reportId, {
  title: 'Updated Report Title'
});

// Download report file
const reportBlob = await client.reports.download(reportId);

// Get report summary statistics
const summary = await client.reports.getSummary();
console.log(`Total reports: ${summary.totalReports}`);
console.log(`Reports by type:`, summary.reportsByType);

// Generate reports in different formats
const pdfReport = await client.reports.generatePdf(scanId);
const csvReport = await client.reports.generateCsv(scanId);
const jsonReport = await client.reports.generateJson(scanId);
const sarifReport = await client.reports.generateSarif(scanId);
const htmlReport = await client.reports.generateHtml(scanId);
```

## Error Handling

The SDK provides comprehensive error handling with specific error types:

```typescript
import { TavoClient, TavoError, AuthenticationError, APIError } from '@tavoai/sdk';

const client = new TavoClient({ apiKey: 'your-api-key' });

try {
  const result = await client.scanCode({ code: codeString });
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.error('Authentication failed - check your API key');
  } else if (error instanceof APIError) {
    console.error(\`API error: \${error.message}\`);
  } else if (error instanceof TavoError) {
    console.error(\`General error: \${error.message}\`);
  } else {
    console.error('Unknown error:', error);
  }
}
```

## Configuration

### Custom Base URL

```typescript
const client = new TavoClient({
  apiKey: 'your-api-key',
  baseURL: 'https://api-staging.tavoai.net'
});
```

### Timeout Configuration

```typescript
const client = new TavoClient({
  apiKey: 'your-api-key',
  timeout: 60000 // 60 seconds
});
```

### Retry Configuration

```typescript
const client = new TavoClient({
  apiKey: 'your-api-key',
  retryOptions: {
    maxRetries: 3,
    initialDelay: 1000,
    maxDelay: 10000
  }
});
```

## Advanced Usage

### Request Interceptors

```typescript
const client = new TavoClient({
  apiKey: 'your-api-key',
  interceptors: {
    request: (config) => {
      // Add custom headers
      config.headers['X-Custom-Header'] = 'value';
      return config;
    },
    response: (response) => {
      // Log responses
      console.log('Response:', response);
      return response;
    }
  }
});
```

### Streaming Responses

```typescript
// For large scan results, use streaming
const stream = await client.scanCodeStream({
  code: largeCodeString,
  language: 'javascript'
});

stream.on('data', (chunk) => {
  console.log('Received chunk:', chunk);
});

stream.on('end', () => {
  console.log('Scan complete');
});
```

### Batch Operations

```typescript
// Scan multiple code snippets concurrently
const codeSnippets = [
  { code: 'const x = 1;', language: 'javascript' },
  { code: 'def hello(): pass', language: 'python' },
  { code: 'public class Test {}', language: 'java' }
];

const results = await Promise.all(
  codeSnippets.map(snippet =>
    client.scanCode(snippet)
  )
);

results.forEach((result, index) => {
  console.log(\`Snippet \${index + 1}: \${result.totalIssues} issues\`);
});
```

## Integration Examples

### Express.js Integration

```typescript
import express from 'express';
import { TavoClient } from '@tavoai/sdk';

const app = express();
const client = new TavoClient({ apiKey: process.env.TAVO_API_KEY });

app.use(express.json());

app.post('/scan', async (req, res) => {
  try {
    const { code, language } = req.body;
    const result = await client.scanCode({ code, language });

    res.json({
      success: true,
      totalIssues: result.totalIssues,
      vulnerabilities: result.vulnerabilities
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### React Integration

```tsx
import React, { useState } from 'react';
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient({ apiKey: process.env.REACT_APP_TAVO_API_KEY });

function CodeScanner() {
  const [code, setCode] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleScan = async () => {
    setLoading(true);
    try {
      const scanResult = await client.scanCode({
        code,
        language: 'javascript'
      });
      setResult(scanResult);
    } catch (error) {
      console.error('Scan failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Enter code to scan..."
      />
      <button onClick={handleScan} disabled={loading}>
        {loading ? 'Scanning...' : 'Scan Code'}
      </button>

      {result && (
        <div>
          <h3>Found {result.totalIssues} issues</h3>
          {result.vulnerabilities.map((vuln, index) => (
            <div key={index}>
              <h4>{vuln.title}</h4>
              <p>{vuln.description}</p>
              <span>Severity: {vuln.severity}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CodeScanner;
```

### Next.js API Route

```typescript
// pages/api/scan.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient({
  apiKey: process.env.TAVO_API_KEY
});

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { code, language } = req.body;

    const result = await client.scanCode({
      code,
      language: language || 'javascript'
    });

    res.status(200).json({
      success: true,
      data: result
    });
  } catch (error) {
    console.error('Scan error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
}
```

## Best Practices

1. **Singleton Client**: Create one client instance and reuse it across your application
2. **Error Handling**: Always wrap API calls in try-catch blocks
3. **Type Safety**: Use TypeScript interfaces for better development experience
4. **Timeouts**: Set appropriate timeouts for your use case
5. **Rate Limiting**: Implement proper rate limiting and backoff strategies
