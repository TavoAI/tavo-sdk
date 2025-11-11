# Performance & Optimization Guide

This guide covers API rate limits, performance optimization techniques, and best practices for high-throughput usage of the Tavo AI platform.

## API Rate Limits

The Tavo AI API implements comprehensive rate limiting to ensure fair usage and system stability.

### Rate Limit Tiers

| Tier | Requests/Hour | Requests/Day | Scan Creations | Notes |
|------|---------------|--------------|----------------|-------|
| **Free** | 100 | 1,000 | 10/hour | Basic usage for individuals |
| **Pro** | 1,000 | 10,000 | 50/hour | Small teams and projects |
| **Enterprise** | Custom | Custom | Custom | High-volume enterprise usage |

### Rate Limit Headers

All API responses include rate limit information:

```
X-RateLimit-Limit: 1000        # Maximum requests per hour
X-RateLimit-Remaining: 999     # Remaining requests this hour
X-RateLimit-Reset: 1640995200  # Unix timestamp when limit resets
X-RateLimit-Retry-After: 3600  # Seconds until next request allowed (when exceeded)
```

### Rate Limit Exceeded Response

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded. Please try again later.",
    "details": {
      "limit": 1000,
      "remaining": 0,
      "reset": 1640995200,
      "retry_after": 3600
    }
  }
}
```

## Performance Optimization

### Connection Management

#### Reuse Client Instances
```python
# ✅ Good: Reuse client for multiple requests
client = TavoClient(api_key="your-key")

results = await asyncio.gather(
    client.scan_management.list_scans(),
    client.repositories.list_repositories(),
    client.ai_analysis.get_models()
)
```

```python
# ❌ Bad: Create new client for each request
results = await asyncio.gather(
    TavoClient(api_key="your-key").scan_management.list_scans(),
    TavoClient(api_key="your-key").repositories.list_repositories(),
    TavoClient(api_key="your-key").ai_analysis.get_models()
)
```

#### Connection Pooling
SDKs automatically manage connection pools:
- **HTTP/2** support for multiplexing
- **Connection reuse** to reduce latency
- **Automatic retries** for transient failures
- **DNS caching** for faster lookups

### Request Batching

#### Batch Multiple Operations
```python
# ✅ Good: Batch related operations
async def batch_scan_operations(scan_ids):
    client = TavoClient(api_key="your-key")

    # Batch status checks
    status_tasks = [
        client.scan_management.get_scan_status(scan_id)
        for scan_id in scan_ids
    ]
    statuses = await asyncio.gather(*status_tasks)

    # Process results
    return [s for s in statuses if s['status'] == 'completed']
```

#### Use Bulk Endpoints
```python
# ✅ Good: Use bulk operations when available
client = TavoClient(api_key="your-key")

# Single bulk request instead of multiple individual requests
bulk_result = await client.scan_bulk_operations.create_bulk_scans([
    {"repository_url": "https://github.com/org/repo1", "scan_type": "security"},
    {"repository_url": "https://github.com/org/repo2", "scan_type": "security"},
])
```

### Caching Strategies

#### Cache Static Data
```python
import asyncio
from functools import lru_cache

class CachedTavoClient:
    def __init__(self, api_key):
        self.client = TavoClient(api_key)
        self._cache = {}

    @lru_cache(maxsize=100)
    async def get_repository_info(self, repo_url):
        """Cache repository metadata"""
        return await self.client.repositories.get_repository(repo_url)

    async def cached_scan_rules(self):
        """Cache scan rules for 1 hour"""
        cache_key = "scan_rules"
        if cache_key in self._cache:
            cached_time, rules = self._cache[cache_key]
            if asyncio.get_event_loop().time() - cached_time < 3600:
                return rules

        rules = await self.client.scan_rules.list_rules()
        self._cache[cache_key] = (asyncio.get_event_loop().time(), rules)
        return rules
```

#### HTTP Caching Headers
```python
# SDK respects standard HTTP caching headers
client = TavoClient(api_key="your-key")

# First request - fetches from API
rules = await client.scan_rules.list_rules()

# Subsequent requests within cache window - uses cached response
rules = await client.scan_rules.list_rules()  # Fast cached response
```

### Asynchronous Programming

#### Concurrent Operations
```python
import asyncio

async def analyze_multiple_repos(repo_urls):
    client = TavoClient(api_key="your-key")

    async def analyze_repo(repo_url):
        # Create scan
        scan = await client.scan_management.create_scan({
            "repository_url": repo_url,
            "scan_type": "security"
        })

        # Wait for completion (with timeout)
        timeout = 300  # 5 minutes
        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < timeout:
            status = await client.scan_management.get_scan_status(scan["id"])
            if status["status"] == "completed":
                # Get AI analysis
                analysis = await client.ai_analysis.analyze_scan(scan["id"])
                return analysis
            await asyncio.sleep(5)  # Poll every 5 seconds

        raise TimeoutError(f"Scan timeout for {repo_url}")

    # Analyze all repos concurrently
    results = await asyncio.gather(*[
        analyze_repo(url) for url in repo_urls
    ], return_exceptions=True)

    return results
```

#### Streaming and Pagination

```python
async def process_large_result_set():
    client = TavoClient(api_key="your-key")
    page_size = 100
    page = 0

    while True:
        # Use pagination for large datasets
        scans = await client.scan_management.list_scans({
            "page": page,
            "page_size": page_size,
            "status": "completed"
        })

        if not scans["items"]:
            break

        # Process page
        for scan in scans["items"]:
            await process_scan(scan)

        page += 1

        # Rate limiting: small delay between pages
        await asyncio.sleep(0.1)
```

## Monitoring and Debugging

### Request Timing
```python
import time

class TimedTavoClient:
    def __init__(self, api_key):
        self.client = TavoClient(api_key)

    async def timed_request(self, method_name, *args, **kwargs):
        start_time = time.time()
        try:
            result = await getattr(self.client, method_name)(*args, **kwargs)
            duration = time.time() - start_time
            print(f"{method_name}: {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            print(f"{method_name} failed after {duration:.2f}s: {e}")
            raise
```

### Error Handling and Retries
```python
import asyncio
from typing import Callable, Any

async def with_retry(func: Callable, max_retries: int = 3, backoff: float = 1.0):
    """Execute function with exponential backoff retry logic"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e

            # Check if error is retryable
            if isinstance(e, (ConnectionError, TimeoutError)):
                wait_time = backoff * (2 ** attempt)
                print(f"Retry {attempt + 1} after {wait_time}s: {e}")
                await asyncio.sleep(wait_time)
            else:
                # Non-retryable error
                raise e

# Usage
client = TavoClient(api_key="your-key")

result = await with_retry(
    lambda: client.scan_management.create_scan({
        "repository_url": "https://github.com/org/repo",
        "scan_type": "security"
    })
)
```

## Resource Optimization

### Memory Management
```python
# For large scan results, process incrementally
async def process_large_scan(scan_id):
    client = TavoClient(api_key="your-key")

    # Get basic scan info first
    scan_info = await client.scan_management.get_scan(scan_id)

    # Process results in chunks
    offset = 0
    chunk_size = 50

    while True:
        results = await client.scan_management.get_scan_results(
            scan_id, offset=offset, limit=chunk_size
        )

        if not results["vulnerabilities"]:
            break

        # Process chunk
        for vuln in results["vulnerabilities"]:
            await process_vulnerability(vuln)

        offset += chunk_size

        # Prevent memory pressure
        if offset % 1000 == 0:
            await asyncio.sleep(0.01)  # Small yield
```

### Compression and Encoding
```python
# SDK automatically handles compression
client = TavoClient(api_key="your-key")

# Requests with large payloads are automatically compressed
large_scan_config = {
    "repository_url": "https://github.com/org/repo",
    "scan_type": "comprehensive",
    "rules": ["rule1", "rule2", "rule3"] * 100,  # Large config
    "exclusions": ["path1", "path2", "path3"] * 100
}

result = await client.scan_management.create_scan(large_scan_config)
# Request automatically compressed with gzip
```

## Enterprise Considerations

### Load Balancing
```python
# For high-throughput applications, consider client-side load balancing
import random

class LoadBalancedTavoClient:
    def __init__(self, api_keys):
        self.clients = [TavoClient(key) for key in api_keys]

    def get_client(self):
        return random.choice(self.clients)

    async def scan_repository(self, repo_url):
        client = self.get_client()
        return await client.scan_management.create_scan({
            "repository_url": repo_url,
            "scan_type": "security"
        })
```

### Circuit Breaker Pattern
```python
class CircuitBreakerTavoClient:
    def __init__(self, api_key, failure_threshold=5, recovery_timeout=60):
        self.client = TavoClient(api_key)
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open

    async def execute_with_circuit_breaker(self, operation):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise CircuitBreakerOpenError("Circuit breaker is open")

        try:
            result = await operation()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        self.failure_count = 0
        self.state = "closed"

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"
```

## SDK-Specific Optimizations

### Python SDK
```python
# Use aiohttp connector configuration for high concurrency
import aiohttp

connector = aiohttp.TCPConnector(
    limit=100,  # Max concurrent connections
    limit_per_host=10,  # Per host limit
    ttl_dns_cache=300,  # DNS cache TTL
    use_dns_cache=True
)

# SDK will use this connector for optimized performance
```

### TypeScript/JavaScript SDK
```typescript
// Configure axios adapter for Node.js optimization
import axios from 'axios';
import httpAdapter from 'axios/lib/adapters/http';

// Use HTTP adapter instead of XHR for Node.js
const client = TavoSdk.createClient({
  apiKey: 'your-key',
  adapter: httpAdapter
});
```

### Java SDK
```java
// Configure HTTP client for high throughput
TavoClient client = TavoSdk.createClientBuilder("your-key")
    .withMaxConnections(50)
    .withConnectionTimeout(Duration.ofSeconds(10))
    .withReadTimeout(Duration.ofSeconds(30))
    .build();
```

## Monitoring Performance

### Metrics Collection
```python
class MetricsTavoClient:
    def __init__(self, api_key):
        self.client = TavoClient(api_key)
        self.metrics = {
            "requests_total": 0,
            "requests_failed": 0,
            "response_times": [],
            "rate_limits_hit": 0
        }

    async def _make_request(self, method, *args, **kwargs):
        import time
        start_time = time.time()

        try:
            self.metrics["requests_total"] += 1
            result = await getattr(self.client, method)(*args, **kwargs)

            response_time = time.time() - start_time
            self.metrics["response_times"].append(response_time)

            return result
        except Exception as e:
            self.metrics["requests_failed"] += 1

            # Check for rate limit errors
            if "rate limit" in str(e).lower():
                self.metrics["rate_limits_hit"] += 1

            raise e

    def get_metrics(self):
        return {
            **self.metrics,
            "avg_response_time": sum(self.metrics["response_times"]) / len(self.metrics["response_times"]) if self.metrics["response_times"] else 0,
            "error_rate": self.metrics["requests_failed"] / self.metrics["requests_total"] if self.metrics["requests_total"] > 0 else 0
        }
```

This comprehensive guide covers the key performance considerations when using the Tavo AI platform at scale.
