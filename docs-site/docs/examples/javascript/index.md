# JavaScript/TypeScript SDK Examples

This directory contains comprehensive examples for using the Tavo AI JavaScript/TypeScript SDK.

## Installation

```bash
npm install tavo-ai
```

or

```bash
yarn add tavo-ai
```

## Basic Usage

### Simple Code Scan

```javascript
const { TavoClient } = require('tavo-ai');

async function main() {
    // Initialize client
    const client = new TavoClient('your-api-key');

    // Code to scan
    const code = `
function processUserInput(userInput) {
    const query = \`SELECT * FROM users WHERE id = '\${userInput}'\`;
    // Potential SQL injection vulnerability
    executeQuery(query);
}
`;

    try {
        // Scan the code
        const result = await client.scanCode(code, 'javascript');

        console.log(`Found ${result.totalIssues} issues`);
        result.vulnerabilities.forEach((vuln, index) => {
            console.log(`${index + 1}. ${vuln.title}: ${vuln.description}`);
        });
    } finally {
        // Clean up
        await client.close();
    }
}

main().catch(console.error);
```

### TypeScript Example

```typescript
import { TavoClient, ScanResult, Vulnerability } from 'tavo-ai';

async function scanTypeScriptCode(): Promise<void> {
    const client = new TavoClient('your-api-key');

    try {
        const code: string = `
function authenticate(username: string, password: string): boolean {
    const query = \`SELECT * FROM users WHERE username='\${username}' AND password='\${password}'\`;
    // SQL injection vulnerability
    return executeQuery(query);
}
`;

        const result: ScanResult = await client.scanCode(code, 'typescript');

        console.log(`Found ${result.totalIssues} issues`);

        result.vulnerabilities.forEach((vuln: Vulnerability, index: number) => {
            console.log(`${index + 1}. ${vuln.title} (${vuln.severity})`);
            console.log(`   ${vuln.description}`);

            if (vuln.location) {
                console.log(`   Location: ${vuln.location.file}:${vuln.location.line}:${vuln.location.column}`);
            }
        });
    } finally {
        await client.close();
    }
}

scanTypeScriptCode().catch(console.error);
```

## Configuration and Error Handling

```typescript
import { TavoClient, TavoClientOptions, TavoError, TavoAuthError, TavoAPIError } from 'tavo-ai';

async function main() {
    // Configure client
    const options: TavoClientOptions = {
        apiKey: 'your-api-key',
        baseUrl: 'https://api.tavoai.net',
        timeout: 30000,
        maxRetries: 3,
        retryDelay: 1000
    };

    const client = new TavoClient(options);

    try {
        const result = await client.scanCode('console.log("hello");', 'javascript');
        console.log(`Scan successful: ${result.totalIssues} issues`);
    } catch (error) {
        if (error instanceof TavoAuthError) {
            console.error(`Authentication failed: ${error.message}`);
        } else if (error instanceof TavoAPIError) {
            console.error(`API error: ${error.message} (status: ${error.statusCode})`);
        } else if (error instanceof TavoError) {
            console.error(`Tavo error: ${error.message}`);
        } else {
            console.error(`Unexpected error: ${error}`);
        }
    } finally {
        await client.close();
    }
}

main().catch(console.error);
```

## Advanced Examples

### Batch Scanning with Streams

```typescript
import { TavoClient } from 'tavo-ai';
import { createReadStream } from 'fs';
import { readdir, stat } from 'fs/promises';
import { join } from 'path';

class BatchScanner {
    private client: TavoClient;

    constructor(apiKey: string) {
        this.client = new TavoClient(apiKey);
    }

    async scanDirectory(directoryPath: string): Promise<void> {
        const files = await this.getJavaScriptFiles(directoryPath);
        const results = await Promise.allSettled(
            files.map(file => this.scanFile(file))
        );

        let totalIssues = 0;
        let totalFiles = 0;

        results.forEach((result, index) => {
            const file = files[index];
            if (result.status === 'fulfilled') {
                const issues = result.value;
                totalIssues += issues;
                totalFiles++;
                console.log(`${file}: ${issues} issues`);
            } else {
                console.error(`Failed to scan ${file}: ${result.reason}`);
            }
        });

        console.log(`\nScanned ${totalFiles} files, found ${totalIssues} total issues`);
    }

    private async scanFile(filePath: string): Promise<number> {
        const code = await this.readFile(filePath);
        const result = await this.client.scanCode(code, this.getLanguageFromPath(filePath));
        return result.totalIssues;
    }

    private async getJavaScriptFiles(dirPath: string): Promise<string[]> {
        const files: string[] = [];

        async function scanDir(currentPath: string) {
            const entries = await readdir(currentPath, { withFileTypes: true });

            for (const entry of entries) {
                const fullPath = join(currentPath, entry.name);

                if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
                    await scanDir(fullPath);
                } else if (entry.isFile() && /\.(js|ts|jsx|tsx)$/.test(entry.name)) {
                    files.push(fullPath);
                }
            }
        }

        await scanDir(dirPath);
        return files;
    }

    private async readFile(filePath: string): Promise<string> {
        return new Promise((resolve, reject) => {
            let content = '';
            const stream = createReadStream(filePath, { encoding: 'utf8' });

            stream.on('data', chunk => content += chunk);
            stream.on('end', () => resolve(content));
            stream.on('error', reject);
        });
    }

    private getLanguageFromPath(filePath: string): string {
        if (filePath.endsWith('.ts') || filePath.endsWith('.tsx')) {
            return 'typescript';
        }
        return 'javascript';
    }

    async close(): Promise<void> {
        await this.client.close();
    }
}

// Usage
async function main() {
    const scanner = new BatchScanner('your-api-key');

    try {
        await scanner.scanDirectory('./src');
    } finally {
        await scanner.close();
    }
}

main().catch(console.error);
```

### AI Model Analysis

```typescript
import { TavoClient } from 'tavo-ai';

interface ModelConfig {
    modelType: string;
    architecture: {
        layers: number;
        attentionHeads: number;
        hiddenSize: number;
        vocabSize: number;
    };
    training: {
        dataset: string;
        epochs: number;
        learningRate: number;
    };
}

async function analyzeModel() {
    const client = new TavoClient('your-api-key');

    try {
        const modelConfig: ModelConfig = {
            modelType: 'transformer',
            architecture: {
                layers: 12,
                attentionHeads: 8,
                hiddenSize: 768,
                vocabSize: 30000
            },
            training: {
                dataset: 'wikipedia',
                epochs: 10,
                learningRate: 0.0001
            }
        };

        const analysis = await client.analyzeModel(modelConfig);

        console.log(`Model safety: ${analysis.safe ? 'Safe' : 'Unsafe'}`);

        if (!analysis.safe && analysis.issues) {
            console.log('Issues found:');
            analysis.issues.forEach((issue, index) => {
                console.log(`${index + 1}. ${issue.title}: ${issue.description}`);
            });
        }
    } finally {
        await client.close();
    }
}

analyzeModel().catch(console.error);
```

### Webhook Management

```typescript
import { TavoClient } from 'tavo-ai';

interface WebhookConfig {
    url: string;
    events: string[];
    secret?: string;
    active?: boolean;
}

async function manageWebhooks() {
    const client = new TavoClient('your-api-key');

    try {
        // Create a webhook
        const webhookConfig: WebhookConfig = {
            url: 'https://myapp.com/webhook/scan-complete',
            events: ['scan.completed', 'vulnerability.found'],
            secret: 'webhook-secret',
            active: true
        };

        const webhook = await client.createWebhook(webhookConfig);
        console.log(`Created webhook: ${webhook.id}`);

        // List all webhooks
        const webhooks = await client.listWebhooks();
        console.log(`Total webhooks: ${webhooks.length}`);

        webhooks.forEach(wh => {
            console.log(`- ${wh.id}: ${wh.url} (${wh.events.join(', ')})`);
        });

        // Update webhook
        await client.updateWebhook(webhook.id, {
            events: ['scan.completed', 'vulnerability.found', 'scan.failed']
        });

        // Delete the webhook
        await client.deleteWebhook(webhook.id);
        console.log('Webhook deleted');

    } finally {
        await client.close();
    }
}

manageWebhooks().catch(console.error);
```

## Integration Examples

### Express.js API

```typescript
import express, { Request, Response, NextFunction } from 'express';
import { TavoClient, ScanResult } from 'tavo-ai';
import cors from 'cors';

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Global client instance
let tavoClient: TavoClient;

async function initializeClient() {
    const apiKey = process.env.TAVO_API_KEY;
    if (!apiKey) {
        throw new Error('TAVO_API_KEY environment variable is required');
    }

    tavoClient = new TavoClient({
        apiKey,
        timeout: 60000, // 1 minute timeout
        maxRetries: 3
    });
}

// Request logging middleware
app.use((req: Request, res: Response, next: NextFunction) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Scan endpoint
app.post('/api/scan', async (req: Request, res: Response) => {
    try {
        const { code, language = 'javascript' } = req.body;

        if (!code) {
            return res.status(400).json({ error: 'Code is required' });
        }

        const result: ScanResult = await tavoClient.scanCode(code, language);

        res.json({
            success: true,
            totalIssues: result.totalIssues,
            vulnerabilities: result.vulnerabilities.map(vuln => ({
                title: vuln.title,
                description: vuln.description,
                severity: vuln.severity,
                location: vuln.location ? {
                    file: vuln.location.file,
                    line: vuln.location.line,
                    column: vuln.location.column
                } : null
            })),
            scanId: result.scanId
        });

    } catch (error) {
        console.error('Scan error:', error);

        if (error.name === 'TavoAuthError') {
            res.status(401).json({ error: 'Authentication failed' });
        } else if (error.name === 'TavoAPIError') {
            res.status(error.statusCode || 500).json({ error: error.message });
        } else {
            res.status(500).json({ error: 'Internal server error' });
        }
    }
});

// Async scan endpoint
app.post('/api/scan/async', async (req: Request, res: Response) => {
    try {
        const { code, language = 'javascript', webhookUrl } = req.body;

        if (!code) {
            return res.status(400).json({ error: 'Code is required' });
        }

        // Start async scan
        const scanId = `scan_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        // Process scan in background
        processScanAsync(scanId, code, language, webhookUrl);

        res.json({
            success: true,
            scanId,
            status: 'processing',
            message: 'Scan started. Results will be sent to webhook.'
        });

    } catch (error) {
        console.error('Async scan error:', error);
        res.status(500).json({ error: 'Failed to start scan' });
    }
});

// Health check
app.get('/health', (req: Request, res: Response) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Error handling middleware
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
    console.error('Unhandled error:', error);
    res.status(500).json({ error: 'Internal server error' });
});

async function processScanAsync(scanId: string, code: string, language: string, webhookUrl?: string) {
    try {
        const result = await tavoClient.scanCode(code, language);

        if (webhookUrl) {
            // Send results to webhook
            await fetch(webhookUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    scanId,
                    status: 'completed',
                    result
                })
            });
        }

        console.log(`Async scan ${scanId} completed: ${result.totalIssues} issues`);

    } catch (error) {
        console.error(`Async scan ${scanId} failed:`, error);

        if (webhookUrl) {
            await fetch(webhookUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    scanId,
                    status: 'failed',
                    error: error.message
                })
            });
        }
    }
}

// Graceful shutdown
process.on('SIGTERM', async () => {
    console.log('Shutting down gracefully...');
    if (tavoClient) {
        await tavoClient.close();
    }
    process.exit(0);
});

process.on('SIGINT', async () => {
    console.log('Shutting down gracefully...');
    if (tavoClient) {
        await tavoClient.close();
    }
    process.exit(0);
});

// Start server
async function startServer() {
    try {
        await initializeClient();
        app.listen(port, () => {
            console.log(`Server running on port ${port}`);
        });
    } catch (error) {
        console.error('Failed to start server:', error);
        process.exit(1);
    }
}

startServer();
```

### React Hook for Security Scanning

```typescript
import { useState, useCallback } from 'react';
import { TavoClient, ScanResult, Vulnerability } from 'tavo-ai';

interface UseSecurityScanResult {
    scan: (code: string, language?: string) => Promise<void>;
    result: ScanResult | null;
    loading: boolean;
    error: string | null;
    clearResult: () => void;
}

export function useSecurityScan(apiKey: string): UseSecurityScanResult {
    const [result, setResult] = useState<ScanResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const scan = useCallback(async (code: string, language: string = 'javascript') => {
        if (!code.trim()) {
            setError('Code is required');
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const client = new TavoClient(apiKey);
            const scanResult = await client.scanCode(code, language);
            await client.close();

            setResult(scanResult);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    }, [apiKey]);

    const clearResult = useCallback(() => {
        setResult(null);
        setError(null);
    }, []);

    return {
        scan,
        result,
        loading,
        error,
        clearResult
    };
}
```

### React Component

```tsx
import React, { useState } from 'react';
import { useSecurityScan } from './useSecurityScan';

const SecurityScanner: React.FC = () => {
    const [code, setCode] = useState('');
    const [language, setLanguage] = useState('javascript');
    const { scan, result, loading, error, clearResult } = useSecurityScan(
        process.env.REACT_APP_TAVO_API_KEY || ''
    );

    const handleScan = async () => {
        await scan(code, language);
    };

    return (
        <div className="security-scanner">
            <h2>Security Code Scanner</h2>

            <div className="input-section">
                <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                >
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="python">Python</option>
                    <option value="java">Java</option>
                </select>

                <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="Enter code to scan..."
                    rows={10}
                    cols={80}
                />

                <div className="buttons">
                    <button
                        onClick={handleScan}
                        disabled={loading || !code.trim()}
                    >
                        {loading ? 'Scanning...' : 'Scan Code'}
                    </button>

                    {result && (
                        <button onClick={clearResult}>
                            Clear Results
                        </button>
                    )}
                </div>
            </div>

            {error && (
                <div className="error">
                    <h3>Error</h3>
                    <p>{error}</p>
                </div>
            )}

            {result && (
                <div className="results">
                    <h3>Scan Results</h3>
                    <p>Total Issues: <strong>{result.totalIssues}</strong></p>

                    {result.vulnerabilities.length > 0 && (
                        <div className="vulnerabilities">
                            <h4>Vulnerabilities Found:</h4>
                            <ul>
                                {result.vulnerabilities.map((vuln, index) => (
                                    <li key={index} className={`severity-${vuln.severity}`}>
                                        <strong>{vuln.title}</strong> ({vuln.severity})
                                        <p>{vuln.description}</p>
                                        {vuln.location && (
                                            <small>
                                                Location: {vuln.location.file}:{vuln.location.line}:{vuln.location.column}
                                            </small>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {result.vulnerabilities.length === 0 && (
                        <div className="no-issues">
                            ✅ No security issues found!
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default SecurityScanner;
```

### CLI Tool

```typescript
#!/usr/bin/env ts-node

import { Command } from 'commander';
import { TavoClient } from 'tavo-ai';
import { readFileSync, readdirSync, statSync } from 'fs';
import { join, extname } from 'path';

const program = new Command();

program
    .name('tavo-scanner')
    .description('Tavo AI Security Scanner CLI')
    .version('1.0.0');

program
    .option('-k, --api-key <key>', 'Tavo AI API key')
    .option('-l, --language <lang>', 'programming language', 'javascript')
    .option('-r, --recursive', 'scan directories recursively')
    .option('-v, --verbose', 'verbose output');

program
    .command('scan <path>')
    .description('scan a file or directory for security vulnerabilities')
    .action(async (path: string) => {
        const options = program.opts();

        const apiKey = options.apiKey || process.env.TAVO_API_KEY;
        if (!apiKey) {
            console.error('❌ API key required. Use --api-key or set TAVO_API_KEY environment variable');
            process.exit(1);
        }

        const client = new TavoClient(apiKey);

        try {
            const stats = statSync(path);

            if (stats.isFile()) {
                const issues = await scanFile(client, path, options.language, options.verbose);
                process.exit(issues > 0 ? 1 : 0);
            } else if (stats.isDirectory()) {
                const issues = await scanDirectory(client, path, options.language, options.recursive, options.verbose);
                process.exit(issues > 0 ? 1 : 0);
            } else {
                console.error('❌ Path is neither a file nor directory');
                process.exit(1);
            }
        } catch (error) {
            console.error('❌ Error:', error.message);
            process.exit(1);
        } finally {
            await client.close();
        }
    });

async function scanFile(
    client: TavoClient,
    filePath: string,
    language: string,
    verbose: boolean
): Promise<number> {
    try {
        const code = readFileSync(filePath, 'utf-8');
        const result = await client.scanCode(code, language);

        if (result.totalIssues > 0) {
            console.log(`\n🔴 ${filePath} (${result.totalIssues} issues):`);

            result.vulnerabilities.forEach((vuln, index) => {
                console.log(`  ${index + 1}. ${vuln.title} (${vuln.severity})`);
                if (verbose) {
                    console.log(`     ${vuln.description}`);
                    if (vuln.location) {
                        console.log(`     📍 ${vuln.location.file}:${vuln.location.line}:${vuln.location.column}`);
                    }
                }
            });
        } else {
            console.log(`✅ ${filePath} (0 issues)`);
        }

        return result.totalIssues;
    } catch (error) {
        console.error(`❌ Error scanning ${filePath}:`, error.message);
        return 0;
    }
}

async function scanDirectory(
    client: TavoClient,
    dirPath: string,
    language: string,
    recursive: boolean,
    verbose: boolean
): Promise<number> {
    const files = getFilesToScan(dirPath, language, recursive);

    if (files.length === 0) {
        console.log('No files found to scan');
        return 0;
    }

    console.log(`Scanning ${files.length} files...`);

    const results = await Promise.all(
        files.map(file => scanFile(client, file, language, verbose))
    );

    const totalIssues = results.reduce((sum, issues) => sum + issues, 0);

    console.log(`\n📊 Summary: ${files.length} files scanned, ${totalIssues} total issues`);

    return totalIssues;
}

function getFilesToScan(dirPath: string, language: string, recursive: boolean): string[] {
    const extensions = getExtensionsForLanguage(language);
    const files: string[] = [];

    function scanDir(currentPath: string) {
        const entries = readdirSync(currentPath, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = join(currentPath, entry.name);

            if (entry.isDirectory()) {
                if (recursive && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
                    scanDir(fullPath);
                }
            } else if (entry.isFile() && extensions.includes(extname(entry.name))) {
                files.push(fullPath);
            }
        }
    }

    scanDir(dirPath);
    return files;
}

function getExtensionsForLanguage(language: string): string[] {
    const extensionMap: { [key: string]: string[] } = {
        javascript: ['.js', '.jsx'],
        typescript: ['.ts', '.tsx'],
        python: ['.py'],
        java: ['.java'],
        go: ['.go'],
        rust: ['.rs'],
        csharp: ['.cs']
    };

    return extensionMap[language] || ['.js'];
}

program.parse();
```

## Testing Examples

### Unit Tests with Jest

```typescript
import { TavoClient } from '../src/TavoClient';
import { TavoAPIError } from '../src/errors';

// Mock fetch globally
global.fetch = jest.fn();

describe('TavoClient', () => {
    let client: TavoClient;

    beforeEach(() => {
        client = new TavoClient('test-api-key');
        jest.clearAllMocks();
    });

    afterEach(async () => {
        await client.close();
    });

    describe('scanCode', () => {
        it('should successfully scan code', async () => {
            const mockResponse = {
                totalIssues: 1,
                vulnerabilities: [{
                    title: 'SQL Injection',
                    description: 'Potential SQL injection vulnerability',
                    severity: 'high',
                    location: {
                        file: 'test.js',
                        line: 5,
                        column: 10
                    }
                }]
            };

            (global.fetch as jest.Mock).mockResolvedValueOnce({
                ok: true,
                json: jest.fn().mockResolvedValue(mockResponse)
            });

            const result = await client.scanCode('test code', 'javascript');

            expect(result.totalIssues).toBe(1);
            expect(result.vulnerabilities).toHaveLength(1);
            expect(result.vulnerabilities[0].title).toBe('SQL Injection');
        });

        it('should handle API errors', async () => {
            (global.fetch as jest.Mock).mockResolvedValueOnce({
                ok: false,
                status: 400,
                json: jest.fn().mockResolvedValue({ error: 'Invalid request' })
            });

            await expect(client.scanCode('test code', 'javascript'))
                .rejects
                .toThrow(TavoAPIError);
        });

        it('should handle network errors', async () => {
            (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

            await expect(client.scanCode('test code', 'javascript'))
                .rejects
                .toThrow('Network error');
        });
    });

    describe('analyzeModel', () => {
        it('should analyze AI model successfully', async () => {
            const mockResponse = {
                safe: false,
                issues: [{
                    title: 'Data Poisoning',
                    description: 'Model may be vulnerable to data poisoning attacks'
                }]
            };

            (global.fetch as jest.Mock).mockResolvedValueOnce({
                ok: true,
                json: jest.fn().mockResolvedValue(mockResponse)
            });

            const modelConfig = { modelType: 'transformer' };
            const result = await client.analyzeModel(modelConfig);

            expect(result.safe).toBe(false);
            expect(result.issues).toHaveLength(1);
        });
    });
});
```

### Integration Tests

```typescript
import { TavoClient } from '../src/TavoClient';

describe('TavoClient Integration Tests', () => {
    let client: TavoClient;
    const apiKey = process.env.TAVO_API_KEY;

    beforeAll(() => {
        if (!apiKey) {
            throw new Error('TAVO_API_KEY environment variable is required for integration tests');
        }
        client = new TavoClient(apiKey);
    });

    afterAll(async () => {
        await client.close();
    });

    describe('scanCode', () => {
        it('should detect SQL injection in vulnerable code', async () => {
            const vulnerableCode = `
function authenticate(username, password) {
    const query = \`SELECT * FROM users WHERE username='\${username}' AND password='\${password}'\`;
    // SQL injection vulnerability
    return executeQuery(query);
}
`;

            const result = await client.scanCode(vulnerableCode, 'javascript');

            expect(result.totalIssues).toBeGreaterThan(0);

            const sqlInjectionFound = result.vulnerabilities.some(vuln =>
                vuln.title.toLowerCase().includes('sql') &&
                vuln.title.toLowerCase().includes('injection')
            );

            expect(sqlInjectionFound).toBe(true);
        });

        it('should not flag safe parameterized queries', async () => {
            const safeCode = `
function authenticate(username, password) {
    const query = 'SELECT * FROM users WHERE username=? AND password=?';
    return executeQuery(query, [username, password]);
}
`;

            const result = await client.scanCode(safeCode, 'javascript');

            // Should not have critical or high severity issues
            const highSeverityIssues = result.vulnerabilities.filter(vuln =>
                vuln.severity === 'critical' || vuln.severity === 'high'
            );

            expect(highSeverityIssues).toHaveLength(0);
        });
    });

    describe('webhooks', () => {
        it('should create and manage webhooks', async () => {
            const webhookConfig = {
                url: 'https://example.com/webhook',
                events: ['scan.completed']
            };

            const webhook = await client.createWebhook(webhookConfig);
            expect(webhook.id).toBeDefined();
            expect(webhook.url).toBe(webhookConfig.url);

            const webhooks = await client.listWebhooks();
            expect(webhooks.length).toBeGreaterThan(0);

            // Clean up
            await client.deleteWebhook(webhook.id);
        });
    });
});
```
