# tavo-sdk

Python SDK for Tavo AI API

## Installation

```bash
pip install tavo-sdk
# or
poetry add tavo-sdk
```

## Usage

### Basic Usage

```python
from tavo import TavoClient

# Initialize client
client = TavoClient(api_key='your-api-key-here')

# Health check
health = client.health_check()
print(f'API Status: {health.status}')
```

### Advanced Usage

```python
from tavo import TavoClient

client = TavoClient(
    api_key='your-api-key',
    base_url='https://api.tavoai.net'  # optional
)

# Scan a repository
scan = client.scans.create(
    repository_url='https://github.com/user/repo',
    scan_type='security'
)

print(f'Scan created: {scan.id}')

# Get scan results
results = client.scans.get_results(scan.id)
print(f'Vulnerabilities found: {len(results.vulnerabilities)}')
```

### Async Support

```python
import asyncio
from tavo import AsyncTavoClient

async def main():
    client = AsyncTavoClient(api_key='your-api-key')

    # Health check
    health = await client.health_check()
    print(f'API Status: {health.status}')

    # Scan repository
    scan = await client.scans.create(
        repository_url='https://github.com/user/repo'
    )
    print(f'Scan created: {scan.id}')

asyncio.run(main())
```

## API Reference

### TavoClient

Main client class for interacting with Tavo AI API.

#### Constructor Options

- `api_key` (str): Your Tavo AI API key
- `base_url` (str, optional): API base URL (defaults to production)
- `timeout` (float, optional): Request timeout in seconds

#### Methods

- `health_check()`: Check API availability
- `scans.create(options)`: Create a new scan
- `scans.get_results(scan_id)`: Get scan results
- `scans.list()`: List all scans

### AsyncTavoClient

Async version of TavoClient with the same interface.

## Authentication

Get your API key from [Tavo AI Dashboard](https://app.tavoai.net).

```bash
export TAVO_API_KEY="your-api-key"
```

## Requirements

- Python 3.8+
- pip or poetry

## License

Apache-2.0

## Support

- [Documentation](https://docs.tavoai.net/python/)
- [GitHub Issues](https://github.com/TavoAI/tavo-sdk/issues)
- [Community Forum](https://community.tavoai.net)