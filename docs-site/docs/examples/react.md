---
sidebar_position: 5
---

# React Integration

Integrate Tavo AI security scanning into your React applications.

## Installation

```bash
npm install tavo-ai axios
```

## Basic Setup

### Environment Configuration

```javascript
// .env
REACT_APP_TAVO_API_KEY=your-api-key-here
REACT_APP_TAVO_BASE_URL=https://api.tavoai.net
REACT_APP_TAVO_TIMEOUT=30000
```

### Tavo Service

```javascript
// services/tavoService.js
import axios from 'axios';

class TavoService {
    constructor() {
        this.client = axios.create({
            baseURL: process.env.REACT_APP_TAVO_BASE_URL || 'https://api.tavoai.net',
            timeout: parseInt(process.env.REACT_APP_TAVO_TIMEOUT) || 30000,
            headers: {
                'Authorization': `Bearer ${process.env.REACT_APP_TAVO_API_KEY}`,
                'Content-Type': 'application/json',
            },
        });
    }

    async scanCode(code, language = 'javascript') {
        try {
            const response = await this.client.post('/scans', {
                name: `Code Scan - ${language}`,
                target: code,
                scan_type: 'code',
                language: language,
            });
            return response.data;
        } catch (error) {
            throw new Error(`Code scan failed: ${error.response?.data?.message || error.message}`);
        }
    }

    async scanUrl(url) {
        try {
            const response = await this.client.post('/scans', {
                name: `URL Scan - ${url}`,
                target: url,
                scan_type: 'web',
            });
            return response.data;
        } catch (error) {
            throw new Error(`URL scan failed: ${error.response?.data?.message || error.message}`);
        }
    }

    async getScanResults(scanId) {
        try {
            const response = await this.client.get(`/scans/${scanId}/results`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get scan results: ${error.response?.data?.message || error.message}`);
        }
    }

    async generateReport(scanIds, format = 'pdf') {
        try {
            const response = await this.client.post('/reports', {
                type: 'compliance',
                format: format,
                scan_ids: scanIds,
            });
            return response.data;
        } catch (error) {
            throw new Error(`Report generation failed: ${error.response?.data?.message || error.message}`);
        }
    }
}

export default new TavoService();
```

## React Hooks

### useTavo Hook

```javascript
// hooks/useTavo.js
import { useState, useCallback } from 'react';
import tavoService from '../services/tavoService';

export const useTavo = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const scanCode = useCallback(async (code, language = 'javascript') => {
        setLoading(true);
        setError(null);

        try {
            const result = await tavoService.scanCode(code, language);
            return result;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const scanUrl = useCallback(async (url) => {
        setLoading(true);
        setError(null);

        try {
            const result = await tavoService.scanUrl(url);
            return result;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const getScanResults = useCallback(async (scanId) => {
        setLoading(true);
        setError(null);

        try {
            const result = await tavoService.getScanResults(scanId);
            return result;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const generateReport = useCallback(async (scanIds, format = 'pdf') => {
        setLoading(true);
        setError(null);

        try {
            const result = await tavoService.generateReport(scanIds, format);
            return result;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        loading,
        error,
        scanCode,
        scanUrl,
        getScanResults,
        generateReport,
    };
};
```

### useAsync Hook for Advanced State Management

```javascript
// hooks/useAsync.js
import { useState, useEffect, useCallback } from 'react';

export const useAsync = (asyncFunction, immediate = false) => {
    const [status, setStatus] = useState('idle');
    const [value, setValue] = useState(null);
    const [error, setError] = useState(null);

    const execute = useCallback(() => {
        setStatus('pending');
        setValue(null);
        setError(null);

        return asyncFunction()
            .then((response) => {
                setValue(response);
                setStatus('success');
                return response;
            })
            .catch((error) => {
                setError(error);
                setStatus('error');
                throw error;
            });
    }, [asyncFunction]);

    useEffect(() => {
        if (immediate) {
            execute();
        }
    }, [execute, immediate]);

    return { execute, status, value, error };
};
```

## React Components

### Code Scanner Component

```javascript
// components/CodeScanner.jsx
import React, { useState } from 'react';
import { useTavo } from '../hooks/useTavo';

const CodeScanner = () => {
    const [code, setCode] = useState('');
    const [language, setLanguage] = useState('javascript');
    const [scanResult, setScanResult] = useState(null);
    const { loading, error, scanCode } = useTavo();

    const handleScan = async () => {
        if (!code.trim()) {
            alert('Please enter some code to scan');
            return;
        }

        try {
            const result = await scanCode(code, language);
            setScanResult(result);
        } catch (err) {
            console.error('Scan failed:', err);
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Code Security Scan</h2>

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Programming Language
                </label>
                <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md"
                >
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="python">Python</option>
                    <option value="java">Java</option>
                    <option value="go">Go</option>
                </select>
            </div>

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Code to Scan
                </label>
                <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    rows={10}
                    className="w-full p-2 border border-gray-300 rounded-md font-mono text-sm"
                    placeholder="Paste your code here..."
                />
            </div>

            <button
                onClick={handleScan}
                disabled={loading}
                className="bg-blue-500 hover:bg-blue-700 disabled:bg-blue-300 text-white font-bold py-2 px-4 rounded"
            >
                {loading ? 'Scanning...' : 'Scan Code'}
            </button>

            {error && (
                <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                    Error: {error}
                </div>
            )}

            {scanResult && <ScanResultDisplay result={scanResult} />}
        </div>
    );
};

export default CodeScanner;
```

### URL Scanner Component

```javascript
// components/UrlScanner.jsx
import React, { useState } from 'react';
import { useTavo } from '../hooks/useTavo';

const UrlScanner = () => {
    const [url, setUrl] = useState('');
    const [scanResult, setScanResult] = useState(null);
    const { loading, error, scanUrl } = useTavo();

    const handleScan = async () => {
        if (!url.trim()) {
            alert('Please enter a URL to scan');
            return;
        }

        try {
            const result = await scanUrl(url);
            setScanResult(result);
        } catch (err) {
            console.error('Scan failed:', err);
        }
    };

    const validateUrl = (value) => {
        try {
            new URL(value);
            return true;
        } catch {
            return false;
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">URL Security Scan</h2>

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    URL to Scan
                </label>
                <input
                    type="url"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="https://example.com"
                />
                {url && !validateUrl(url) && (
                    <p className="text-red-500 text-sm mt-1">Please enter a valid URL</p>
                )}
            </div>

            <button
                onClick={handleScan}
                disabled={loading || !validateUrl(url)}
                className="bg-blue-500 hover:bg-blue-700 disabled:bg-blue-300 text-white font-bold py-2 px-4 rounded"
            >
                {loading ? 'Scanning...' : 'Scan URL'}
            </button>

            {error && (
                <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                    Error: {error}
                </div>
            )}

            {scanResult && <ScanResultDisplay result={scanResult} />}
        </div>
    );
};

export default UrlScanner;
```

### Scan Result Display Component

```javascript
// components/ScanResultDisplay.jsx
import React, { useState } from 'react';
import { useTavo } from '../hooks/useTavo';

const ScanResultDisplay = ({ result }) => {
    const [detailedResults, setDetailedResults] = useState(null);
    const [loadingDetails, setLoadingDetails] = useState(false);
    const { getScanResults } = useTavo();

    const handleViewDetails = async () => {
        setLoadingDetails(true);
        try {
            const details = await getScanResults(result.id);
            setDetailedResults(details);
        } catch (error) {
            console.error('Failed to get detailed results:', error);
        } finally {
            setLoadingDetails(false);
        }
    };

    return (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
            <h3 className="text-lg font-semibold text-green-800 mb-2">Scan Successful</h3>

            <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                    <span className="font-medium">Scan ID:</span> {result.id}
                </div>
                <div>
                    <span className="font-medium">Status:</span>
                    <span className={`ml-2 px-2 py-1 rounded text-sm ${
                        result.status === 'completed'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                    }`}>
                        {result.status}
                    </span>
                </div>
            </div>

            {result.summary && (
                <div className="mb-4">
                    <h4 className="font-semibold mb-2">Summary:</h4>
                    <ul className="list-disc list-inside text-sm space-y-1">
                        <li>Files scanned: {result.summary.files_scanned || 0}</li>
                        <li>Vulnerabilities found: {result.summary.vulnerabilities_found || 0}</li>
                        <li>Scan duration: {result.summary.duration || 'N/A'}</li>
                    </ul>
                </div>
            )}

            <button
                onClick={handleViewDetails}
                disabled={loadingDetails}
                className="bg-green-500 hover:bg-green-700 disabled:bg-green-300 text-white font-bold py-2 px-4 rounded"
            >
                {loadingDetails ? 'Loading...' : 'View Detailed Results'}
            </button>

            {detailedResults && (
                <div className="mt-4 p-4 bg-white border border-gray-200 rounded">
                    <h4 className="font-semibold mb-2">Detailed Results</h4>
                    <pre className="text-sm overflow-x-auto">
                        {JSON.stringify(detailedResults, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    );
};

export default ScanResultDisplay;
```

## Context Provider for Global State

### Tavo Context

```javascript
// context/TavoContext.jsx
import React, { createContext, useContext, useReducer } from 'react';

// Initial state
const initialState = {
    scans: [],
    currentScan: null,
    loading: false,
    error: null,
};

// Action types
const SCAN_START = 'SCAN_START';
const SCAN_SUCCESS = 'SCAN_SUCCESS';
const SCAN_ERROR = 'SCAN_ERROR';
const CLEAR_ERROR = 'CLEAR_ERROR';

// Reducer
function tavoReducer(state, action) {
    switch (action.type) {
        case SCAN_START:
            return {
                ...state,
                loading: true,
                error: null,
            };
        case SCAN_SUCCESS:
            return {
                ...state,
                loading: false,
                scans: [...state.scans, action.payload],
                currentScan: action.payload,
            };
        case SCAN_ERROR:
            return {
                ...state,
                loading: false,
                error: action.payload,
            };
        case CLEAR_ERROR:
            return {
                ...state,
                error: null,
            };
        default:
            return state;
    }
}

// Context
const TavoContext = createContext();

// Provider component
export const TavoProvider = ({ children }) => {
    const [state, dispatch] = useReducer(tavoReducer, initialState);

    const startScan = () => dispatch({ type: SCAN_START });
    const scanSuccess = (result) => dispatch({ type: SCAN_SUCCESS, payload: result });
    const scanError = (error) => dispatch({ type: SCAN_ERROR, payload: error });
    const clearError = () => dispatch({ type: CLEAR_ERROR });

    return (
        <TavoContext.Provider value={{
            ...state,
            startScan,
            scanSuccess,
            scanError,
            clearError,
        }}>
            {children}
        </TavoContext.Provider>
    );
};

// Custom hook
export const useTavoContext = () => {
    const context = useContext(TavoContext);
    if (!context) {
        throw new Error('useTavoContext must be used within a TavoProvider');
    }
    return context;
};
```

## Main Application

### App.jsx

```javascript
// App.jsx
import React from 'react';
import { TavoProvider } from './context/TavoContext';
import CodeScanner from './components/CodeScanner';
import UrlScanner from './components/UrlScanner';
import ScanHistory from './components/ScanHistory';

function App() {
    return (
        <TavoProvider>
            <div className="min-h-screen bg-gray-100">
                <header className="bg-blue-600 text-white p-4">
                    <div className="container mx-auto">
                        <h1 className="text-3xl font-bold">Tavo AI Security Scanner</h1>
                        <p className="text-blue-100">Advanced security scanning powered by AI</p>
                    </div>
                </header>

                <main className="container mx-auto px-4 py-8">
                    <div className="grid md:grid-cols-2 gap-8 mb-8">
                        <CodeScanner />
                        <UrlScanner />
                    </div>

                    <ScanHistory />
                </main>
            </div>
        </TavoProvider>
    );
}

export default App;
```

### Scan History Component

```javascript
// components/ScanHistory.jsx
import React from 'react';
import { useTavoContext } from '../context/TavoContext';

const ScanHistory = () => {
    const { scans, loading } = useTavoContext();

    if (scans.length === 0 && !loading) {
        return (
            <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-2xl font-semibold mb-4">Scan History</h2>
                <p className="text-gray-500">No scans performed yet.</p>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4">Scan History</h2>

            <div className="space-y-4">
                {scans.map((scan, index) => (
                    <div key={scan.id || index} className="border border-gray-200 rounded p-4">
                        <div className="flex justify-between items-start mb-2">
                            <div>
                                <h3 className="font-semibold">{scan.name}</h3>
                                <p className="text-sm text-gray-600">ID: {scan.id}</p>
                            </div>
                            <span className={`px-2 py-1 rounded text-sm ${
                                scan.status === 'completed'
                                    ? 'bg-green-100 text-green-800'
                                    : scan.status === 'running'
                                    ? 'bg-yellow-100 text-yellow-800'
                                    : 'bg-red-100 text-red-800'
                            }`}>
                                {scan.status}
                            </span>
                        </div>

                        {scan.summary && (
                            <div className="text-sm text-gray-600">
                                <span>Files: {scan.summary.files_scanned || 0}</span>
                                <span className="ml-4">Vulnerabilities: {scan.summary.vulnerabilities_found || 0}</span>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ScanHistory;
```

## Error Boundaries

### Error Boundary Component

```javascript
// components/ErrorBoundary.jsx
import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error('Error caught by boundary:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="bg-red-50 border border-red-200 rounded-md p-4 m-4">
                    <h2 className="text-red-800 font-semibold mb-2">Something went wrong</h2>
                    <p className="text-red-700 mb-4">
                        An error occurred while processing your request. Please try again.
                    </p>
                    <button
                        onClick={() => this.setState({ hasError: false, error: null })}
                        className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                    >
                        Try Again
                    </button>
                    {process.env.NODE_ENV === 'development' && (
                        <details className="mt-4">
                            <summary className="cursor-pointer text-sm">Error Details</summary>
                            <pre className="text-xs mt-2 p-2 bg-red-100 rounded overflow-x-auto">
                                {this.state.error?.toString()}
                            </pre>
                        </details>
                    )}
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
```

## Testing

### Component Tests with React Testing Library

```javascript
// __tests__/CodeScanner.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import CodeScanner from '../components/CodeScanner';

// Mock the useTavo hook
jest.mock('../hooks/useTavo', () => ({
    useTavo: () => ({
        loading: false,
        error: null,
        scanCode: jest.fn().mockResolvedValue({
            id: 'test-scan-id',
            status: 'completed',
            summary: { files_scanned: 1, vulnerabilities_found: 0 }
        }),
    }),
}));

describe('CodeScanner', () => {
    test('renders code scanner form', () => {
        render(<CodeScanner />);

        expect(screen.getByText('Code Security Scan')).toBeInTheDocument();
        expect(screen.getByLabelText('Programming Language')).toBeInTheDocument();
        expect(screen.getByLabelText('Code to Scan')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Scan Code' })).toBeInTheDocument();
    });

    test('shows validation error for empty code', async () => {
        const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});
        render(<CodeScanner />);

        const scanButton = screen.getByRole('button', { name: 'Scan Code' });
        fireEvent.click(scanButton);

        expect(alertMock).toHaveBeenCalledWith('Please enter some code to scan');
        alertMock.mockRestore();
    });

    test('scans code successfully', async () => {
        render(<CodeScanner />);

        const codeTextarea = screen.getByLabelText('Code to Scan');
        const scanButton = screen.getByRole('button', { name: 'Scan Code' });

        fireEvent.change(codeTextarea, { target: { value: 'console.log("test");' } });
        fireEvent.click(scanButton);

        await waitFor(() => {
            expect(screen.getByText('Scan Successful')).toBeInTheDocument();
        });
    });
});
```

### Hook Tests

```javascript
// __tests__/useTavo.test.js
import { renderHook, act } from '@testing-library/react-hooks';
import { useTavo } from '../hooks/useTavo';

// Mock axios
jest.mock('axios');
import axios from 'axios';

describe('useTavo', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('scanCode success', async () => {
        const mockResponse = { data: { id: 'test-id', status: 'completed' } };
        axios.post.mockResolvedValue(mockResponse);

        const { result } = renderHook(() => useTavo());

        let scanResult;
        await act(async () => {
            scanResult = await result.current.scanCode('test code', 'javascript');
        });

        expect(scanResult).toEqual(mockResponse.data);
        expect(axios.post).toHaveBeenCalledWith('/scans', {
            name: 'Code Scan - javascript',
            target: 'test code',
            scan_type: 'code',
            language: 'javascript',
        });
    });

    test('scanCode error', async () => {
        const mockError = { response: { data: { message: 'API Error' } } };
        axios.post.mockRejectedValue(mockError);

        const { result } = renderHook(() => useTavo());

        await act(async () => {
            try {
                await result.current.scanCode('test code', 'javascript');
            } catch (error) {
                expect(error.message).toContain('Code scan failed');
            }
        });

        expect(result.current.error).toContain('Code scan failed');
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

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  tavo-react:
    build: .
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_TAVO_API_KEY=${TAVO_API_KEY}
      - REACT_APP_TAVO_BASE_URL=https://api.tavoai.net
    restart: unless-stopped
```

## Deployment

### Production Build

```javascript
// package.json (scripts section)
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint src --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint src --ext .js,.jsx,.ts,.tsx --fix"
  }
}
```

### Environment Variables for Production

```bash
# Production environment
REACT_APP_TAVO_API_KEY=your-production-api-key
REACT_APP_TAVO_BASE_URL=https://api.tavoai.net
GENERATE_SOURCEMAP=false
```

### Nginx Configuration for Production

```nginx
# nginx.conf
server {
    listen 80;
    server_name your-domain.com;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass https://api.tavoai.net;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

This React integration provides a modern, user-friendly interface for Tavo AI security scanning with comprehensive state management, error handling, testing, and production deployment configurations.
