# Tavo AI SDK Authentication Guide

This document describes how to authenticate with Tavo AI APIs using the official SDKs.

## Quick Start

### JavaScript SDK

```javascript
import { TavoClient } from '@tavoai/sdk';

// Using API Key (recommended)
const client = new TavoClient({
  apiKey: process.env.TAVO_API_KEY
});

// Basic usage
const health = await client.healthCheck();
console.log('API Status:', health.status);
```

### Python SDK

```python
from tavo import TavoClient

# Using API Key (recommended)
client = TavoClient(api_key=os.getenv('TAVO_API_KEY'))

# Basic usage
async with client:
    health = await client.health_check()
    print(f'API Status: {health.status}')
```

## Authentication Methods

### API Key Authentication (Recommended)

API keys provide secure, programmatic access to Tavo AI APIs.

#### Obtaining an API Key

1. **Via GitHub OAuth** (Fastest):
   - Visit https://app.tavoai.net
   - Sign in with GitHub
   - Copy your automatically generated API key

2. **Via Email/Password**:
   - Register at https://app.tavoai.net
   - Verify your email
   - Access your API key from the dashboard

#### Configuration

```javascript
// JavaScript
const client = new TavoClient({
  apiKey: 'your-api-key-here'
});
```

```python
# Python
client = TavoClient(api_key='your-api-key-here')

# Or use environment variable
client = TavoClient()  # Reads TAVO_API_KEY env var
```

### JWT Token Authentication

For web applications requiring user sessions.

```javascript
const client = new TavoClient({
  jwtToken: 'your-jwt-token-here'
});
```

```python
client = TavoClient(jwt_token='your-jwt-token-here')
```

## Environment Variables

Set these environment variables for easy configuration:

```bash
# API Key (recommended for client tools)
export TAVO_API_KEY=your-api-key

# JWT Token (for web applications)
export TAVO_JWT_TOKEN=your-jwt-token

# Custom API endpoint (for development)
export TAVO_BASE_URL=https://api.tavoai.net
```

## Error Handling

### Authentication Errors

```javascript
try {
  const result = await client.scans.create(request);
} catch (error) {
  if (error.response?.status === 401) {
    console.error('Authentication failed: Check your API key');
  } else if (error.response?.status === 403) {
    console.error('Authorization failed: Insufficient permissions');
  }
}
```

```python
try:
    result = await client.scans.create(request)
except Exception as e:
    if hasattr(e, 'response') and e.response.status_code == 401:
        print('Authentication failed: Check your API key')
    elif hasattr(e, 'response') and e.response.status_code == 403:
        print('Authorization failed: Insufficient permissions')
```

### Rate Limiting

```javascript
try {
  const result = await client.scans.create(request);
} catch (error) {
  if (error.response?.status === 429) {
    const retryAfter = error.response.headers['retry-after'];
    console.log(`Rate limited. Retry after ${retryAfter} seconds`);
    // Implement exponential backoff
  }
}
```

## Testing

### Mock Authentication

For unit testing, use test API keys:

```javascript
const testClient = new TavoClient({
  apiKey: 'test-api-key',
  baseURL: 'http://localhost:8000'  // Test server
});
```

```python
test_client = TavoClient(
    api_key='test-api-key',
    base_url='http://localhost:8000'  # Test server
)
```

### Integration Testing

See the `tests/integration.test.*` files in each SDK package for comprehensive testing examples that mirror the api-server test patterns.

## Security Best Practices

- **Never commit API keys** to version control
- **Use environment variables** for configuration
- **Rotate keys regularly** (monthly recommended)
- **Monitor usage** via dashboard analytics
- **Use different keys** for different environments

## Rate Limits

- **Free Tier**: 100 requests/hour, 10 scans/day
- **Developer Tier**: 1000 requests/hour, 100 scans/day
- **Business Tier**: 5000 requests/hour, 500 scans/day
- **Enterprise Tier**: Custom limits

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check API key validity and format
2. **403 Forbidden**: Verify account permissions and tier limits
3. **429 Rate Limited**: Wait for reset or upgrade plan
4. **Connection errors**: Verify base URL and network connectivity

### Getting Help

- **SDK Documentation**: https://docs.tavoai.net
- **API Reference**: https://api.tavoai.net/docs
- **GitHub Issues**: https://github.com/TavoAI/tavo-sdk/issues
- **Support**: support@tavoai.net