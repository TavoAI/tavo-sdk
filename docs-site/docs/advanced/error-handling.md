# Error Handling

All Tavo AI SDKs provide consistent and comprehensive error handling to help you build robust applications. This guide covers error types, handling strategies, and best practices.

## Error Types

### SDK-Specific Errors

Each SDK defines its own error types while maintaining consistent behavior:

#### Python SDK

```python
from tavo_ai import TavoError, TavoAPIError, TavoAuthError, TavoValidationError

# All errors inherit from TavoError
try:
    result = await client.scan_code(code)
except TavoAuthError:
    print("Authentication failed - check your API key")
except TavoAPIError as e:
    print(f"API error: {e.message} (status: {e.status_code})")
except TavoValidationError as e:
    print(f"Validation error: {e.details}")
except TavoError as e:
    print(f"General error: {e}")
```

#### JavaScript/TypeScript SDK

```javascript
import { TavoError, TavoAPIError, TavoAuthError, TavoValidationError } from '@tavoai/sdk';

try {
  const result = await client.scans().scanCode(code);
} catch (error) {
  if (error instanceof TavoAuthError) {
    console.log('Authentication failed - check your API key');
  } else if (error instanceof TavoAPIError) {
    console.log(`API error: ${error.message} (status: ${error.statusCode})`);
  } else if (error instanceof TavoValidationError) {
    console.log(`Validation error: ${error.details}`);
  } else if (error instanceof TavoError) {
    console.log(`General error: ${error.message}`);
  }
}
```

#### Java SDK

```java
import net.tavoai.TavoException;
import net.tavoai.TavoAPIException;
import net.tavoai.TavoAuthException;
import net.tavoai.TavoValidationException;

try {
    ScanResult result = client.getScans().scanCode(code, language);
} catch (TavoAuthException e) {
    System.err.println("Authentication failed - check your API key");
} catch (TavoAPIException e) {
    System.err.println("API error: " + e.getMessage() + " (status: " + e.getStatusCode() + ")");
} catch (TavoValidationException e) {
    System.err.println("Validation error: " + e.getDetails());
} catch (TavoException e) {
    System.err.println("General error: " + e.getMessage());
}
```

#### Go SDK

```go
package main

import (
    "errors"
    "fmt"
    "github.com/tavoai/tavo-go-sdk/tavo"
)

func main() {
    client := tavo.NewClient(&tavo.Config{APIKey: "your-api-key"})

    result, err := client.Scans().ScanCode(code, language)
    if err != nil {
        var authErr *tavo.AuthError
        var apiErr *tavo.APIError
        var validationErr *tavo.ValidationError

        switch {
        case errors.As(err, &authErr):
            fmt.Println("Authentication failed - check your API key")
        case errors.As(err, &apiErr):
            fmt.Printf("API error: %s (status: %d)\n", apiErr.Message, apiErr.StatusCode)
        case errors.As(err, &validationErr):
            fmt.Printf("Validation error: %v\n", validationErr.Details)
        default:
            fmt.Printf("General error: %s\n", err.Error())
        }
    }
}
```

#### .NET SDK

```csharp
using TavoAI;
using TavoAI.Exceptions;

try
{
    var result = await client.Scans.ScanCodeAsync(code, language);
}
catch (TavoAuthException ex)
{
    Console.WriteLine("Authentication failed - check your API key");
}
catch (TavoAPIException ex)
{
    Console.WriteLine($"API error: {ex.Message} (status: {ex.StatusCode})");
}
catch (TavoValidationException ex)
{
    Console.WriteLine($"Validation error: {ex.Details}");
}
catch (TavoException ex)
{
    Console.WriteLine($"General error: {ex.Message}");
}
```

#### Rust SDK

```rust
use tavo_ai::{TavoError, TavoAPIError, TavoAuthError, TavoValidationError};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = TavoClient::new("your-api-key")?;

    match client.scans().scan_code(code, language).await {
        Ok(result) => {
            println!("Scan completed: {} issues found", result.total_issues);
        }
        Err(TavoError::Auth(e)) => {
            println!("Authentication failed - check your API key: {}", e);
        }
        Err(TavoError::API(e)) => {
            println!("API error: {} (status: {})", e.message, e.status_code);
        }
        Err(TavoError::Validation(e)) => {
            println!("Validation error: {:?}", e.details);
        }
        Err(e) => {
            println!("General error: {}", e);
        }
    }

    Ok(())
}
```

## HTTP Status Codes

The API returns standard HTTP status codes:

| Code  | Description           | Handling Strategy              |
| ----- | --------------------- | ------------------------------ |
| `200` | Success               | No action needed               |
| `201` | Created               | Resource created successfully  |
| `400` | Bad Request           | Check request parameters       |
| `401` | Unauthorized          | Check API key/authentication   |
| `403` | Forbidden             | Check permissions              |
| `404` | Not Found             | Check resource ID/path         |
| `409` | Conflict              | Resource already exists        |
| `422` | Unprocessable Entity  | Validation failed              |
| `429` | Too Many Requests     | Implement backoff/retry        |
| `500` | Internal Server Error | Retry with exponential backoff |
| `502` | Bad Gateway           | Retry with exponential backoff |
| `503` | Service Unavailable   | Retry with exponential backoff |

## Common Error Scenarios

### Authentication Errors

```javascript
// API key missing or invalid
{
  "error": "Unauthorized",
  "message": "Invalid API key",
  "code": "INVALID_API_KEY"
}

// API key expired
{
  "error": "Unauthorized",
  "message": "API key expired",
  "code": "API_KEY_EXPIRED"
}
```

### Validation Errors

```javascript
// Invalid request parameters
{
  "error": "Bad Request",
  "message": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "code": ["Code cannot be empty"],
    "language": ["Language must be one of: python, javascript, java, go, rust, csharp"]
  }
}
```

### Rate Limiting

```javascript
// Rate limit exceeded
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

### Resource Not Found

```javascript
// Scan not found
{
  "error": "Not Found",
  "message": "Scan not found",
  "code": "SCAN_NOT_FOUND"
}
```

## Retry Strategies

### Exponential Backoff

```python
import asyncio
import random

async def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return await func()
        except TavoAPIError as e:
            if e.status_code >= 500:  # Server errors
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                await asyncio.sleep(delay)
            else:
                raise  # Don't retry client errors
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half-open

    async def call(self, func):
        if self.state == 'open':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'half-open'
            else:
                raise CircuitBreakerError("Circuit breaker is open")

        try:
            result = await func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        self.state = 'closed'

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = 'open'
```

## Best Practices

### 1. Always Handle Errors

```python
# ❌ Bad - Unhandled errors
result = await client.scan_code(code)
print(f"Found {result.total_issues} issues")

# ✅ Good - Proper error handling
try:
    result = await client.scan_code(code)
    print(f"Found {result.total_issues} issues")
except TavoAuthError:
    print("Please check your API key")
except TavoAPIError as e:
    print(f"API error: {e.message}")
except TavoError as e:
    print(f"Unexpected error: {e}")
```

### 2. Use Specific Error Types

```python
# ❌ Bad - Generic error handling
try:
    result = await client.scan_code(code)
except Exception as e:
    print(f"Something went wrong: {e}")

# ✅ Good - Specific error handling
try:
    result = await client.scan_code(code)
except TavoAuthError:
    print("Authentication failed - check your API key")
except TavoValidationError as e:
    print(f"Invalid input: {e.details}")
except TavoAPIError as e:
    if e.status_code == 429:
        print("Rate limit exceeded, please try again later")
    else:
        print(f"API error: {e.message}")
```

### 3. Implement Retry Logic for Transient Errors

```python
async def scan_with_retry(client, code, language, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await client.scan_code(code, language)
        except TavoAPIError as e:
            if e.status_code >= 500 and attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
```

### 4. Log Errors Appropriately

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = await client.scan_code(code)
except TavoAuthError as e:
    logger.error("Authentication failed: %s", e)
    # Handle auth error (e.g., prompt for new API key)
except TavoAPIError as e:
    logger.warning("API error: %s (status: %d)", e.message, e.status_code)
    # Handle API error (e.g., retry)
except TavoError as e:
    logger.error("Unexpected Tavo error: %s", e)
    # Handle unexpected error
```

### 5. Provide User-Friendly Error Messages

```python
def format_error_message(error):
    if isinstance(error, TavoAuthError):
        return "Please check your API key and try again."
    elif isinstance(error, TavoValidationError):
        return f"Invalid input: {', '.join(error.details)}"
    elif isinstance(error, TavoAPIError):
        if error.status_code == 429:
            return "Too many requests. Please wait a moment and try again."
        elif error.status_code >= 500:
            return "Service temporarily unavailable. Please try again later."
        else:
            return f"Request failed: {error.message}"
    else:
        return "An unexpected error occurred. Please try again."

try:
    result = await client.scan_code(code)
except TavoError as e:
    user_message = format_error_message(e)
    print(user_message)
```

### 6. Handle Rate Limits Gracefully

```python
async def scan_with_rate_limit_handling(client, code, language):
    try:
        return await client.scan_code(code, language)
    except TavoAPIError as e:
        if e.status_code == 429:
            retry_after = getattr(e, 'retry_after', 60)
            print(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
            await asyncio.sleep(retry_after)
            return await client.scan_code(code, language)
        raise
```

## Error Monitoring

### Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log errors with context
try:
    result = await client.scan_code(code)
except TavoError as e:
    logger.error("Scan failed", extra={
        'error_type': type(e).__name__,
        'code_length': len(code) if code else 0,
        'language': language,
        'user_id': current_user.id
    })
    raise
```

### Metrics and Monitoring

```python
from dataclasses import dataclass
from typing import Dict, Any
import time

@dataclass
class ErrorMetrics:
    total_errors: int = 0
    errors_by_type: Dict[str, int] = None
    errors_by_status_code: Dict[int, int] = None

    def __post_init__(self):
        self.errors_by_type = {}
        self.errors_by_status_code = {}

    def record_error(self, error: TavoError):
        self.total_errors += 1
        error_type = type(error).__name__
        self.errors_by_type[error_type] = self.errors_by_type.get(error_type, 0) + 1

        if hasattr(error, 'status_code'):
            self.errors_by_status_code[error.status_code] = \
                self.errors_by_status_code.get(error.status_code, 0) + 1

# Global metrics
error_metrics = ErrorMetrics()

async def monitored_scan(client, code, language):
    start_time = time.time()
    try:
        result = await client.scan_code(code, language)
        # Record success metrics
        return result
    except TavoError as e:
        error_metrics.record_error(e)
        # Send to monitoring system
        monitoring_client.increment_counter('tavo.scan.errors', {
            'error_type': type(e).__name__,
            'language': language
        })
        raise
    finally:
        duration = time.time() - start_time
        monitoring_client.record_histogram('tavo.scan.duration', duration, {
            'language': language
        })
```

## Next Steps

- [API Reference](../api-reference/overview.md) - Complete API documentation
- [SDK Guides](../sdks/) - Language-specific SDK documentation
- [Rate Limits](../api-reference/overview.md#rate-limits) - Understanding rate limiting
- [Authentication](../getting-started/authentication.md) - Setting up authentication
