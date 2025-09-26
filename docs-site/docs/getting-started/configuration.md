---
sidebar_position: 2
---

# Configuration

Configure the Tavo AI SDK for your environment and use case.

## Environment Variables

The SDK supports configuration through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `TAVO_API_KEY` | Your API key for authentication | Required |
| `TAVO_BASE_URL` | API base URL | `https://api.tavoai.net` |
| `TAVO_API_VERSION` | API version | `v1` |
| `TAVO_TIMEOUT` | Request timeout in seconds | `30` |
| `TAVO_MAX_RETRIES` | Maximum retry attempts | `3` |

## Python Configuration

```python
from tavo import TavoClient, TavoConfig

# Using environment variables (recommended)
client = TavoClient()

# Explicit configuration
config = TavoConfig(
    api_key="your-api-key",
    base_url="https://api.tavoai.net",
    timeout=30.0,
    max_retries=3
)
client = TavoClient(config)
```

## JavaScript/TypeScript Configuration

```javascript
import { TavoClient } from '@tavoai/sdk';

// Using environment variables
const client = new TavoClient();

// Explicit configuration
const client = new TavoClient({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.tavoai.net',
  timeout: 30000, // milliseconds
  maxRetries: 3,
});
```

```typescript
// TypeScript with full type safety
interface TavoConfig {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
  maxRetries?: number;
}

const config: TavoConfig = {
  apiKey: process.env.TAVO_API_KEY,
  baseUrl: process.env.TAVO_BASE_URL,
  timeout: 30000,
  maxRetries: 3,
};

const client = new TavoClient(config);
```

## Java Configuration

```java
import net.tavoai.TavoClient;
import net.tavoai.TavoConfig;

// Using environment variables
TavoClient client = new TavoClient();

// Builder pattern configuration
TavoConfig config = TavoConfig.builder()
    .apiKey("your-api-key")
    .baseUrl("https://api.tavoai.net")
    .timeout(30, TimeUnit.SECONDS)
    .maxRetries(3)
    .build();

TavoClient client = new TavoClient(config);
```

## Go Configuration

```go
package main

import (
    "time"
    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
    // Using environment variables
    config := tavo.NewConfig()
    client := tavo.NewClient(config)

    // Builder pattern configuration
    config := tavo.NewConfig().
        WithAPIKey("your-api-key").
        WithBaseURL("https://api.tavoai.net").
        WithTimeout(30 * time.Second).
        WithMaxRetries(3)

    client := tavo.NewClient(config)
}
```

## Authentication

### API Key Authentication

All SDKs support API key authentication. You can obtain your API key from the Tavo AI dashboard.

```bash
# Set environment variable
export TAVO_API_KEY="your-api-key-here"
```

### JWT Token Authentication (Advanced)

For advanced use cases, JWT tokens are supported:

```python
# Python
config = TavoConfig(jwt_token="your-jwt-token")
```

```javascript
// JavaScript
const client = new TavoClient({
  jwtToken: 'your-jwt-token'
});
```

```java
// Java
TavoConfig config = TavoConfig.builder()
    .jwtToken("your-jwt-token")
    .build();
```

```go
// Go
config := tavo.NewConfig().WithJWTToken("your-jwt-token")
```

## Timeout and Retry Configuration

### Timeout Settings

Configure request timeouts based on your network conditions:

```python
# Python - 60 second timeout
config = TavoConfig(timeout=60.0)
```

```javascript
// JavaScript - 60 second timeout
const client = new TavoClient({
  timeout: 60000, // milliseconds
});
```

```java
// Java - 60 second timeout
TavoConfig config = TavoConfig.builder()
    .timeout(60, TimeUnit.SECONDS)
    .build();
```

```go
// Go - 60 second timeout
config := tavo.NewConfig().WithTimeout(60 * time.Second)
```

### Retry Logic

Configure retry behavior for transient failures:

```python
# Python - 5 retries with exponential backoff
config = TavoConfig(max_retries=5)
```

```javascript
// JavaScript - 5 retries
const client = new TavoClient({
  maxRetries: 5,
});
```

```java
// Java - 5 retries
TavoConfig config = TavoConfig.builder()
    .maxRetries(5)
    .build();
```

```go
// Go - 5 retries
config := tavo.NewConfig().WithMaxRetries(5)
```

## Next Steps

Once configured, proceed to [Authentication](./authentication) to learn about different authentication methods.