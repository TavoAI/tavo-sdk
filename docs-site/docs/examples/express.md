---
sidebar_position: 2
---

# Express.js Integration

Integrate Tavo AI security scanning into your Express.js applications.

## Installation

```bash
npm install tavo-ai express cors helmet
```

## Basic Setup

### Environment Configuration

```javascript
// .env
TAVO_API_KEY=your-api-key-here
TAVO_BASE_URL=https://api.tavoai.net
TAVO_TIMEOUT=30000
TAVO_MAX_RETRIES=3
```

### Tavo Service Class

```javascript
// services/tavoService.js
const { TavoClient, TavoConfig } = require('tavo-ai');

class TavoService {
    constructor() {
        this.config = new TavoConfig({
            apiKey: process.env.TAVO_API_KEY,
            baseUrl: process.env.TAVO_BASE_URL || 'https://api.tavoai.net',
            timeout: parseInt(process.env.TAVO_TIMEOUT) || 30000,
            maxRetries: parseInt(process.env.TAVO_MAX_RETRIES) || 3,
        });
        this.client = new TavoClient(this.config);
    }

    async scanCode(code, language = 'javascript') {
        try {
            return await this.client.scans().createScan({
                name: `Code Scan - ${language}`,
                target: code,
                scanType: 'code',
                language: language,
            });
        } catch (error) {
            throw new Error(`Code scan failed: ${error.message}`);
        }
    }

    async scanUrl(url) {
        try {
            return await this.client.scans().createScan({
                name: `URL Scan - ${url}`,
                target: url,
                scanType: 'web',
            });
        } catch (error) {
            throw new Error(`URL scan failed: ${error.message}`);
        }
    }

    async getScanResults(scanId) {
        try {
            return await this.client.scans().getScanResults(scanId);
        } catch (error) {
            throw new Error(`Failed to get scan results: ${error.message}`);
        }
    }

    async generateReport(scanIds, format = 'pdf') {
        try {
            return await this.client.reports().generateReport({
                type: 'compliance',
                format: format,
                scanIds: scanIds,
            });
        } catch (error) {
            throw new Error(`Report generation failed: ${error.message}`);
        }
    }
}

module.exports = new TavoService();
```

## Express Routes

### Code Scanning Routes

```javascript
// routes/scan.js
const express = require('express');
const router = express.Router();
const tavoService = require('../services/tavoService');

// POST /api/scan/code
router.post('/code', async (req, res) => {
    try {
        const { code, language = 'javascript' } = req.body;

        if (!code) {
            return res.status(400).json({
                error: 'Code is required',
                code: 'MISSING_CODE'
            });
        }

        const result = await tavoService.scanCode(code, language);

        res.json({
            success: true,
            data: result
        });

    } catch (error) {
        console.error('Code scan error:', error);
        res.status(500).json({
            error: error.message,
            code: 'SCAN_FAILED'
        });
    }
});

// POST /api/scan/url
router.post('/url', async (req, res) => {
    try {
        const { url } = req.body;

        if (!url) {
            return res.status(400).json({
                error: 'URL is required',
                code: 'MISSING_URL'
            });
        }

        // Basic URL validation
        try {
            new URL(url);
        } catch {
            return res.status(400).json({
                error: 'Invalid URL format',
                code: 'INVALID_URL'
            });
        }

        const result = await tavoService.scanUrl(url);

        res.json({
            success: true,
            data: result
        });

    } catch (error) {
        console.error('URL scan error:', error);
        res.status(500).json({
            error: error.message,
            code: 'SCAN_FAILED'
        });
    }
});

// GET /api/scan/:scanId/results
router.get('/:scanId/results', async (req, res) => {
    try {
        const { scanId } = req.params;
        const result = await tavoService.getScanResults(scanId);

        res.json({
            success: true,
            data: result
        });

    } catch (error) {
        console.error('Get scan results error:', error);
        res.status(500).json({
            error: error.message,
            code: 'RESULTS_FAILED'
        });
    }
});

module.exports = router;
```

### Report Routes

```javascript
// routes/reports.js
const express = require('express');
const router = express.Router();
const tavoService = require('../services/tavoService');

// POST /api/reports/generate
router.post('/generate', async (req, res) => {
    try {
        const { scanIds, format = 'pdf' } = req.body;

        if (!scanIds || !Array.isArray(scanIds) || scanIds.length === 0) {
            return res.status(400).json({
                error: 'At least one scan ID is required',
                code: 'MISSING_SCAN_IDS'
            });
        }

        const result = await tavoService.generateReport(scanIds, format);

        res.json({
            success: true,
            data: result
        });

    } catch (error) {
        console.error('Report generation error:', error);
        res.status(500).json({
            error: error.message,
            code: 'REPORT_FAILED'
        });
    }
});

module.exports = router;
```

## Main Application

```javascript
// app.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const scanRoutes = require('./routes/scan');
const reportRoutes = require('./routes/reports');

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());
app.use(cors({
    origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
    credentials: true
}));

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Routes
app.use('/api/scan', scanRoutes);
app.use('/api/reports', reportRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'tavo-express-integration'
    });
});

// Error handling middleware
app.use((error, req, res, next) => {
    console.error('Unhandled error:', error);
    res.status(500).json({
        error: 'Internal server error',
        code: 'INTERNAL_ERROR'
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        error: 'Route not found',
        code: 'NOT_FOUND'
    });
});

app.listen(PORT, () => {
    console.log(`Tavo AI Express server running on port ${PORT}`);
});

module.exports = app;
```

## Middleware for Automatic Scanning

### Request Security Middleware

```javascript
// middleware/security.js
const tavoService = require('../services/tavoService');

const securityMiddleware = {
    // Scan incoming code in requests
    scanRequestBody: async (req, res, next) => {
        try {
            // Only scan requests with code content
            if (req.body && req.body.code) {
                const language = req.body.language || 'javascript';

                // Perform scan asynchronously (don't block the request)
                tavoService.scanCode(req.body.code, language)
                    .then(scanResult => {
                        console.log(`Security scan completed for request: ${scanResult.id}`);
                        // Store scan result for later retrieval
                        req.scanResult = scanResult;
                    })
                    .catch(error => {
                        console.error('Background security scan failed:', error);
                    });
            }

            next();
        } catch (error) {
            console.error('Security middleware error:', error);
            next(); // Don't block the request due to scan failure
        }
    },

    // Rate limiting for scan endpoints
    scanRateLimit: (req, res, next) => {
        // Simple in-memory rate limiting (use Redis in production)
        const clientId = req.ip;
        const now = Date.now();
        const windowMs = 15 * 60 * 1000; // 15 minutes
        const maxRequests = 100;

        if (!global.rateLimit) {
            global.rateLimit = new Map();
        }

        const clientRequests = global.rateLimit.get(clientId) || [];
        const recentRequests = clientRequests.filter(time => now - time < windowMs);

        if (recentRequests.length >= maxRequests) {
            return res.status(429).json({
                error: 'Too many requests',
                code: 'RATE_LIMIT_EXCEEDED'
            });
        }

        recentRequests.push(now);
        global.rateLimit.set(clientId, recentRequests);

        next();
    }
};

module.exports = securityMiddleware;
```

### Apply Middleware

```javascript
// app.js (continued)
const securityMiddleware = require('./middleware/security');

// Apply security middleware to scan routes
app.use('/api/scan', securityMiddleware.scanRateLimit);
app.use('/api/scan/code', securityMiddleware.scanRequestBody);
```

## Frontend Integration

### HTML Interface

```html
<!-- public/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tavo AI Security Scanner</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">
            Tavo AI Security Scanner
        </h1>

        <!-- Code Scanner -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 class="text-2xl font-semibold mb-4">Code Security Scan</h2>

            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Programming Language
                </label>
                <select id="language" class="w-full p-2 border border-gray-300 rounded-md">
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="python">Python</option>
                    <option value="java">Java</option>
                    <option value="go">Go</option>
                </select>
            </div>

            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Code to Scan
                </label>
                <textarea
                    id="code"
                    rows="10"
                    class="w-full p-2 border border-gray-300 rounded-md font-mono text-sm"
                    placeholder="Paste your code here..."
                ></textarea>
            </div>

            <button
                id="scanCodeBtn"
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
                Scan Code
            </button>
        </div>

        <!-- URL Scanner -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 class="text-2xl font-semibold mb-4">URL Security Scan</h2>

            <div class="mb-4">
                <input
                    type="url"
                    id="url"
                    class="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="https://example.com"
                >
            </div>

            <button
                id="scanUrlBtn"
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
                Scan URL
            </button>
        </div>

        <!-- Results -->
        <div id="results" class="bg-white rounded-lg shadow-md p-6 hidden">
            <h2 class="text-2xl font-semibold mb-4">Scan Results</h2>
            <div id="resultsContent"></div>
        </div>
    </div>

    <script>
        const API_BASE = '/api';

        // Code scanning
        document.getElementById('scanCodeBtn').addEventListener('click', async () => {
            const code = document.getElementById('code').value;
            const language = document.getElementById('language').value;
            const btn = document.getElementById('scanCodeBtn');

            if (!code.trim()) {
                alert('Please enter some code to scan');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Scanning...';

            try {
                const response = await fetch(`${API_BASE}/scan/code`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code, language })
                });

                const result = await response.json();
                displayResults(result);

            } catch (error) {
                displayResults({ error: error.message });
            } finally {
                btn.disabled = false;
                btn.textContent = 'Scan Code';
            }
        });

        // URL scanning
        document.getElementById('scanUrlBtn').addEventListener('click', async () => {
            const url = document.getElementById('url').value;
            const btn = document.getElementById('scanUrlBtn');

            if (!url.trim()) {
                alert('Please enter a URL to scan');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Scanning...';

            try {
                const response = await fetch(`${API_BASE}/scan/url`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url })
                });

                const result = await response.json();
                displayResults(result);

            } catch (error) {
                displayResults({ error: error.message });
            } finally {
                btn.disabled = false;
                btn.textContent = 'Scan URL';
            }
        });

        function displayResults(result) {
            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');

            if (result.success) {
                const data = result.data;
                resultsContent.innerHTML = `
                    <div class="mb-4">
                        <h3 class="text-lg font-semibold text-green-600">Scan Successful</h3>
                        <p class="text-sm text-gray-600">Scan ID: ${data.id}</p>
                        <p class="text-sm text-gray-600">Status: ${data.status}</p>
                    </div>
                    ${data.summary ? `
                    <div class="mb-4">
                        <h4 class="font-semibold">Summary:</h4>
                        <ul class="list-disc list-inside text-sm">
                            <li>Files scanned: ${data.summary.files_scanned || 0}</li>
                            <li>Vulnerabilities found: ${data.summary.vulnerabilities_found || 0}</li>
                            <li>Scan duration: ${data.summary.duration || 'N/A'}</li>
                        </ul>
                    </div>
                    ` : ''}
                    <button
                        onclick="viewDetailedResults('${data.id}')"
                        class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                    >
                        View Detailed Results
                    </button>
                `;
            } else {
                resultsContent.innerHTML = `
                    <div class="text-red-600">
                        <h3 class="text-lg font-semibold">Scan Failed</h3>
                        <p>${result.error}</p>
                    </div>
                `;
            }

            resultsDiv.classList.remove('hidden');
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }

        async function viewDetailedResults(scanId) {
            try {
                const response = await fetch(`${API_BASE}/scan/${scanId}/results`);
                const result = await response.json();

                if (result.success) {
                    // Display detailed results (implement as needed)
                    console.log('Detailed results:', result.data);
                }
            } catch (error) {
                console.error('Failed to get detailed results:', error);
            }
        }
    </script>
</body>
</html>
```

## Testing

### Unit Tests with Jest

```javascript
// tests/tavoService.test.js
const { TavoClient } = require('tavo-ai');
const TavoService = require('../services/tavoService');

jest.mock('tavo-ai');

describe('TavoService', () => {
    let tavoService;

    beforeEach(() => {
        tavoService = new TavoService();
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    test('should scan code successfully', async () => {
        const mockScanResult = {
            id: 'test-scan-id',
            status: 'completed',
            summary: { vulnerabilities_found: 0 }
        };

        TavoClient.prototype.scans = jest.fn().mockReturnValue({
            createScan: jest.fn().mockResolvedValue(mockScanResult)
        });

        const result = await tavoService.scanCode('console.log("test");', 'javascript');

        expect(result).toEqual(mockScanResult);
    });

    test('should handle scan errors', async () => {
        TavoClient.prototype.scans = jest.fn().mockReturnValue({
            createScan: jest.fn().mockRejectedValue(new Error('Scan failed'))
        });

        await expect(tavoService.scanCode('invalid code')).rejects.toThrow('Code scan failed: Scan failed');
    });
});
```

### API Tests with Supertest

```javascript
// tests/routes.test.js
const request = require('supertest');
const app = require('../app');
const tavoService = require('../services/tavoService');

jest.mock('../services/tavoService');

describe('Scan Routes', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('POST /api/scan/code - success', async () => {
        const mockResult = { id: 'test-id', status: 'completed' };
        tavoService.scanCode.mockResolvedValue(mockResult);

        const response = await request(app)
            .post('/api/scan/code')
            .send({
                code: 'console.log("hello");',
                language: 'javascript'
            })
            .expect(200);

        expect(response.body.success).toBe(true);
        expect(response.body.data).toEqual(mockResult);
    });

    test('POST /api/scan/code - missing code', async () => {
        const response = await request(app)
            .post('/api/scan/code')
            .send({})
            .expect(400);

        expect(response.body.error).toBe('Code is required');
    });
});
```

## Docker Configuration

### Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Change ownership
RUN chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 3000

CMD ["node", "app.js"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  tavo-express:
    build: .
    ports:
      - "3000:3000"
    environment:
      - TAVO_API_KEY=${TAVO_API_KEY}
      - TAVO_BASE_URL=https://api.tavoai.net
      - NODE_ENV=production
    restart: unless-stopped
```

## Deployment

### Environment Variables for Production

```bash
# Production environment
TAVO_API_KEY=your-production-api-key
TAVO_BASE_URL=https://api.tavoai.net
NODE_ENV=production
PORT=3000
CORS_ORIGIN=https://yourdomain.com
```

### PM2 Process Management

```json
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'tavo-express',
    script: 'app.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development',
      PORT: 3000
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000
    }
  }]
};
```

This Express.js integration provides a robust, scalable solution for incorporating Tavo AI security scanning into Node.js applications with comprehensive error handling, testing, and deployment configurations.
