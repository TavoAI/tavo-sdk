# Python SDK

The Tavo AI Python SDK provides a comprehensive, async-first interface for integrating with the Tavo AI platform. Built with modern Python patterns and full type hints for excellent developer experience.

## Installation

```bash
pip install tavo-ai
```

## Quick Start

```python
import asyncio
from tavo_ai import TavoClient

async def main():
    # Initialize the client
    client = TavoClient(api_key="your-api-key")

    # Scan code for vulnerabilities
    result = await client.scan_code("""
        def process_user_input(user_input):
            query = f"SELECT * FROM users WHERE id = '{user_input}'"
            # Potential SQL injection vulnerability
            return execute_query(query)
    """)

    print(f"Found {result.total_issues} issues")
    for vulnerability in result.vulnerabilities:
        print(f"- {vulnerability.title}: {vulnerability.description}")

asyncio.run(main())
```

## Authentication

The SDK supports API key authentication:

```python
from tavo_ai import TavoClient

# Initialize with API key
client = TavoClient(api_key="your-api-key")

# Or set it later
client = TavoClient()
client.api_key = "your-api-key"
```

## Core Operations

### Code Scanning

Scan source code for security vulnerabilities:

```python
# Basic code scan
result = await client.scan_code(code_string, language="python")

# With custom options
result = await client.scan_code(
    code=code_string,
    language="python",
    timeout=30
)
```

### AI Model Analysis

Analyze AI models for security risks:

```python
model_config = {
    "model_type": "transformer",
    "parameters": {
        "layers": 12,
        "heads": 8,
        "hidden_size": 768
    }
}

analysis = await client.analyze_model(model_config)
print(f"Model is safe: {analysis.safe}")
```

### User Management

```python
# Get current user
user = await client.get_current_user()

# Update user profile
updated_user = await client.update_user(user_id, {
    "name": "New Name",
    "email": "new@example.com"
})
```

### Organization Management

```python
# List organizations
orgs = await client.list_organizations()

# Create new organization
new_org = await client.create_organization({
    "name": "My Company",
    "description": "Security scanning service"
})
```

### Scan Jobs

```python
# Start a new scan job
job = await client.create_scan_job({
    "target_url": "https://example.com",
    "scan_type": "full_scan"
})

# Get job status
status = await client.get_scan_job(job.id)

# List all jobs
jobs = await client.list_scan_jobs(limit=10)
```

### Webhooks

```python
# Create webhook
webhook = await client.create_webhook({
    "url": "https://myapp.com/webhook",
    "events": ["scan.completed", "vulnerability.found"]
})

# List webhooks
webhooks = await client.list_webhooks()

# Delete webhook
await client.delete_webhook(webhook.id)
```

### Billing & Reports

```python
# Get billing information
billing = await client.get_billing_info()

# Generate report
report = await client.generate_report({
    "type": "security_audit",
    "date_range": {
        "start": "2024-01-01",
        "end": "2024-01-31"
    }
})
```

## Error Handling

The SDK provides comprehensive error handling:

```python
from tavo_ai import TavoError, TavoAPIError, TavoAuthError

try:
    result = await client.scan_code(code)
except TavoAuthError:
    print("Authentication failed - check your API key")
except TavoAPIError as e:
    print(f"API error: {e.message}")
except TavoError as e:
    print(f"General error: {e}")
```

## Configuration

### Custom Base URL

```python
# Use custom API endpoint
client = TavoClient(
    api_key="your-api-key",
    base_url="https://api-staging.tavoai.net"
)
```

### Timeout Configuration

```python
# Set custom timeout (in seconds)
client = TavoClient(
    api_key="your-api-key",
    timeout=60
)
```

### Retry Configuration

```python
# Configure retry behavior
client = TavoClient(
    api_key="your-api-key",
    max_retries=3,
    retry_delay=1.0
)
```

## Advanced Usage

### Async Context Manager

```python
async with TavoClient(api_key="your-api-key") as client:
    result = await client.scan_code(code)
    # Client automatically handles cleanup
```

### Batch Operations

```python
# Scan multiple code snippets
import asyncio

async def batch_scan(codes):
    async with TavoClient(api_key="your-api-key") as client:
        tasks = [client.scan_code(code) for code in codes]
        results = await asyncio.gather(*tasks)
        return results

results = await batch_scan(code_list)
```

### Custom Request Headers

```python
# Add custom headers to all requests
client = TavoClient(api_key="your-api-key")
client.session.headers.update({
    "X-Custom-Header": "value",
    "User-Agent": "MyApp/1.0"
})
```

## Type Safety

The SDK is fully typed with Python type hints:

```python
from typing import List, Dict, Any
from tavo_ai import ScanResult, Vulnerability

async def analyze_codebase(files: List[str]) -> Dict[str, List[Vulnerability]]:
    results = {}
    async with TavoClient(api_key="your-api-key") as client:
        for file_path in files:
            with open(file_path, 'r') as f:
                code = f.read()
            result = await client.scan_code(code)
            results[file_path] = result.vulnerabilities
    return results
```

## Integration Examples

### Django Integration

```python
# settings.py
TAVO_API_KEY = os.getenv('TAVO_API_KEY')

# views.py
from django.http import JsonResponse
from tavo_ai import TavoClient

async def scan_code_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        async with TavoClient(api_key=settings.TAVO_API_KEY) as client:
            result = await client.scan_code(code)
            return JsonResponse({
                'total_issues': result.total_issues,
                'vulnerabilities': [
                    {'title': v.title, 'severity': v.severity}
                    for v in result.vulnerabilities
                ]
            })
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from tavo_ai import TavoClient, TavoError

app = FastAPI()
client = TavoClient(api_key=os.getenv('TAVO_API_KEY'))

@app.post("/scan")
async def scan_code(code: str):
    try:
        result = await client.scan_code(code)
        return {
            "success": True,
            "total_issues": result.total_issues,
            "vulnerabilities": result.vulnerabilities
        }
    except TavoError as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Best Practices

1. **Reuse Client Instances**: Create one client instance and reuse it for multiple operations
2. **Handle Errors Appropriately**: Always catch and handle `TavoError` exceptions
3. **Use Async/Await**: Take advantage of async operations for better performance
4. **Set Reasonable Timeouts**: Configure timeouts based on your use case
5. **Monitor Rate Limits**: Be aware of API rate limits and implement backoff strategies

## API Reference

For complete API documentation, see the [Python SDK API Reference](../api/python.md).
