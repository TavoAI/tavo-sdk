# Python SDK

The Tavo AI Python SDK provides generated API clients for all platform endpoints plus integrated tavo-scanner execution capabilities. Built with async-first design and full type annotations.

## Installation

```bash
pip install tavo-ai
```

## Architecture

The Python SDK provides a modular, async-first architecture with generated API clients and integrated scanner capabilities.

### Modular API Clients

The SDK provides **26 specialized client classes** for different API endpoint categories, each with full type annotations and async methods:

#### Core Scanning (`tavo.scans`, `tavo.scan_management`, etc.)
```python
# Scan management operations
scan_client = client.scan_management
result = await scan_client.create_scan(repository_url="https://github.com/user/repo")

# Scan tools and rules
tools_client = client.scan_tools
rules_client = client.scan_rules
```

#### AI Analysis (`tavo.ai_analysis`, `tavo.ai_analysis_core`, etc.)
```python
# AI-powered analysis
ai_client = client.ai_analysis
analysis = await ai_client.analyze_code(code="print('hello')", language="python")

# Risk compliance checking
compliance_client = client.ai_risk_compliance
report = await compliance_client.check_compliance(scan_id="123")
```

#### Repository & Registry Management
```python
# Repository operations
repo_client = client.repositories
connections_client = client.repository_connections

# Plugin marketplace
marketplace_client = client.plugin_marketplace
plugins = await marketplace_client.list_plugins()
```

#### Authentication & Device Management
```python
# Device authentication flow
auth_client = client.device_auth
code_result = await auth_client.post_code(client_id="123", client_name="my-app")
```

### Scanner Integration

Built-in tavo-scanner wrapper with advanced capabilities:
- **Async subprocess execution** with timeout handling
- **Plugin and rule management** with validation
- **Automatic binary discovery** (relative paths, PATH, and custom locations)
- **Structured result parsing** with error handling
- **Progress monitoring** and cancellation support

## Quick Start

```python
import asyncio
from tavo import TavoClient, TavoScanner

async def main():
    # Initialize API client with modular architecture
    client = TavoClient(api_key="your-api-key")

    # 1. Device authentication
    auth_client = client.device_auth
    auth_result = await auth_client.post_code(
        client_id="your-client-id",
        client_name="my-security-scanner"
    )
    print(f"Device auth successful: {auth_result}")

    # 2. Create and run a security scan
    scan_client = client.scan_management
    scan_result = await scan_client.create_scan(
        repository_url="https://github.com/your-org/your-repo",
        scan_type="security",
        branch="main"
    )
    print(f"Scan created: {scan_result}")

    # 3. Get scan results with AI analysis
    ai_client = client.ai_analysis
    analysis = await ai_client.analyze_scan(scan_id=scan_result["id"])
    print(f"AI analysis: {len(analysis['vulnerabilities'])} issues found")

    # 4. Alternative: Use integrated scanner
    scanner = TavoScanner()
    local_result = await scanner.scan_directory(
        "./my-project",
        plugins=["security", "performance"],
        rules=["custom-security-rules"]
    )
    print(f"Local scan: {local_result['total_issues']} issues found")

asyncio.run(main())
```

## Client Architecture

The `TavoClient` provides access to all API endpoints through modular client properties:

```python
client = TavoClient(api_key="your-api-key")

# Access different API categories
client.device_auth        # Device authentication
client.scan_management    # Scan lifecycle management
client.ai_analysis        # AI-powered analysis
client.repositories       # Repository operations
client.plugin_marketplace # Plugin management
client.registry          # Registry operations
# ... and 20+ more specialized clients
```

Each client provides fully typed async methods matching the REST API:

```python
# Type hints and IDE completion
result: Dict[str, Any] = await client.scan_management.create_scan(
    repository_url="https://github.com/user/repo",
    scan_type="security"
)
```

## Error Handling

The SDK provides comprehensive error handling with specific exception types:

```python
from tavo import TavoClient, TavoAPIError, AuthenticationError

try:
    client = TavoClient(api_key="invalid-key")
    result = await client.health.get_status()
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except TavoAPIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

## Best Practices

### Connection Management
```python
# Reuse client instances for multiple requests
client = TavoClient(api_key="your-key")

# Client automatically handles connection pooling
results = await asyncio.gather(
    client.scan_management.list_scans(),
    client.repositories.list_repositories(),
    client.ai_analysis.get_models()
)
```

### Timeout Configuration
```python
# Configure timeouts for long-running operations
client = TavoClient(
    api_key="your-key",
    timeout=30.0  # seconds
)
```

### Logging
```python
import logging

# Enable debug logging
logging.getLogger("tavo").setLevel(logging.DEBUG)

client = TavoClient(api_key="your-key")
# All requests now logged with timing and errors
```

## Authentication

The SDK supports multiple authentication methods:

```python
from tavo import TavoClient

# API Key authentication (recommended)
client = TavoClient(api_key="your-api-key")

# JWT Token authentication
client = TavoClient(jwt_token="your-jwt-token")

# Session Token authentication
client = TavoClient(session_token="your-session-token")

# Environment variables (TAVO_API_KEY, TAVO_JWT_TOKEN, TAVO_SESSION_TOKEN)
client = TavoClient()  # Will read from env vars
```

## API Client Usage

Access all platform endpoints through the generated client:

```python
from tavo import TavoClient

client = TavoClient(api_key="your-api-key")

# Authentication operations
auth_result = await client.device_auth.post_code("client_id", "client_name")
token_result = await client.device_auth.post_token("device_code")

# Scanning operations
scan_result = await client.scan_tools.get_scan("scan_id")
bulk_result = await client.scan_bulk_operations.create_bulk_scan([...])

# AI Analysis
analysis = await client.ai_analysis.analyze_code("code", "python")

# Jobs management
jobs = await client.jobs.list_jobs()
job_status = await client.jobs.get_job("job_id")

# Health checks
health = await client.health.health_check()
```

## Scanner Integration

Execute tavo-scanner as a subprocess with full configuration:

```python
from tavo import TavoScanner

# Basic scanning
scanner = TavoScanner()
result = await scanner.scan_directory("./my-project")

# Advanced scanning with plugins
result = await scanner.scan_with_plugins(
    "./my-project",
    plugins=["security", "performance", "accessibility"]
)

# Custom rules and configuration
result = await scanner.scan_with_rules(
    "./my-project",
    rules_path="./custom-rules.json"
)
```

## Available Endpoint Clients

The SDK provides 24+ generated endpoint clients:

| Client | Purpose |
|--------|---------|
| `device_auth` | Device authentication and tokens |
| `scan_tools` | Core scanning operations |
| `scan_management` | Scan lifecycle management |
| `scan_rules` | Scan rule configuration |
| `scan_schedules` | Scheduled scanning |
| `scan_bulk_operations` | Bulk scan operations |
| `scanner_integration` | Scanner integrations |
| `ai_analysis` | AI-powered code analysis |
| `ai_analysis_core` | Core AI analysis operations |
| `ai_bulk_operations` | Bulk AI operations |
| `ai_performance_quality` | Performance analysis |
| `ai_results_export` | Export analysis results |
| `ai_risk_compliance` | Risk and compliance analysis |
| `registry` | Plugin/registry management |
| `plugin_execution` | Plugin execution |
| `plugin_marketplace` | Plugin marketplace |
| `rules` | Rule management |
| `code_submission` | Code submission for analysis |
| `repositories` | Repository management |
| `repository_connections` | Repository connections |
| `repository_providers` | Repository provider integrations |
| `repository_webhooks` | Repository webhooks |
| `jobs` | Background job management |
| `health` | Health check endpoints |

## Scanner Configuration

Configure scanner behavior and plugins:

```python
from tavo import TavoScanner
from tavo.scanner.scanner_config import ScanOptions

# Configure scanner
config = {
    "plugins": ["security", "performance"],
    "rules_path": "./custom-rules.json",
    "timeout": 600,  # 10 minutes
    "output_format": "sarif"
}

scanner = TavoScanner(config)

# Or use ScanOptions
options = ScanOptions(
    static_analysis=True,
    static_plugins=["security"],
    static_rules="./rules.json",
    output_format="json",
    timeout=300
)

result = await scanner.scan_directory("./project", options)
```

## Error Handling

The SDK provides comprehensive error handling:

```python
from tavo import TavoClient, TavoScanner
import asyncio

async def robust_scan():
    client = TavoClient(api_key="your-key")
    scanner = TavoScanner()

    try:
        # API operations with automatic retries
        result = await client.health.health_check()

        # Scanner execution with timeout handling
        scan_result = await scanner.scan_directory("./project")

    except Exception as e:
        print(f"Operation failed: {e}")
        # SDK handles retries, timeouts, and error parsing automatically
```

## Advanced Features

### Async Context Management

```python
from tavo import TavoClient

async with TavoClient(api_key="your-key") as client:
    result = await client.device_auth.post_code("id", "name")
    # Client automatically closes connections
```

### WebSocket Integration

```python
client = TavoClient(api_key="your-key")

# Connect to real-time updates
await client.connect_websocket("client-123")

# Register message handlers
client.on_websocket_message("scan_update", handle_scan_update)

# Send messages
await client.send_websocket_message({
    "type": "subscribe",
    "scan_id": "scan-123"
})
```

### Custom Scanner Configuration

```python
from tavo import TavoScanner

# Custom scanner path
scanner = TavoScanner({
    "scanner_path": "/custom/path/to/tavo-scanner",
    "timeout": 1200,
    "working_directory": "/tmp"
})

# Create temporary config files
plugin_config_path = await scanner.create_plugin_config(
    "security", {"strict_mode": True}
)

result = await scanner.scan_with_rules("./project", plugin_config_path)
```

## Migration Guide

If you're upgrading from a previous version of the SDK:

### Old API (Deprecated)
```python
# Old operation-based API
from tavo_ai import TavoClient
client = TavoClient(api_key="key")
auth_ops = client.auth()
result = await auth_ops.some_method()
```

### New API (Recommended)
```python
# New generated client API
from tavo import TavoClient
client = TavoClient(api_key="key")
result = await client.device_auth.some_method()
```

## Contributing

The Python SDK is generated from the Tavo AI API specification. To contribute:

1. **API Changes**: Modify the API specification in the main Tavo repository
2. **Regeneration**: Run the generation script to update client code
3. **Testing**: Add tests for new functionality
4. **Documentation**: Update this guide for new features

## Support

- 📖 [API Reference](../../api-reference/overview.md)
- 🐛 [GitHub Issues](https://github.com/tavoai/tavo-sdk/issues)
- 💬 [Community Discussions](https://github.com/tavoai/tavo-sdk/discussions)

