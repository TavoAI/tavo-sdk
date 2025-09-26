# Python SDK Examples

This directory contains comprehensive examples for using the Tavo AI Python SDK.

## Basic Usage

### Simple Code Scan

```python
import asyncio
from tavo import TavoClient

async def main():
    # Initialize client
    client = TavoClient("your-api-key")

    # Code to scan
    code = '''
def process_user_input(user_input):
    query = f"SELECT * FROM users WHERE id = '{user_input}'"
    # Potential SQL injection vulnerability
    execute_query(query)
'''

    # Scan the code
    result = await client.scan_code(code, "python")

    print(f"Found {result.total_issues} issues")
    for vuln in result.vulnerabilities:
        print(f"- {vuln.title}: {vuln.description}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Configuration and Error Handling

```python
import asyncio
from tavo import TavoClient, TavoConfig
from tavo.exceptions import TavoAuthError, TavoAPIError

async def main():
    # Configure client
    config = TavoConfig(
        api_key="your-api-key",
        base_url="https://api.tavo.ai",
        timeout=30.0,
        max_retries=3
    )

    async with TavoClient(config) as client:
        try:
            result = await client.scan_code("print('hello')", "python")
            print(f"Scan successful: {result.total_issues} issues")
        except TavoAuthError as e:
            print(f"Authentication failed: {e}")
        except TavoAPIError as e:
            print(f"API error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Examples

### Batch Scanning

```python
import asyncio
from pathlib import Path
from tavo import TavoClient

async def scan_directory(client: TavoClient, directory: Path):
    """Scan all Python files in a directory concurrently."""
    python_files = list(directory.rglob("*.py"))

    # Create scan tasks
    scan_tasks = []
    for file_path in python_files:
        task = asyncio.create_task(scan_file(client, file_path))
        scan_tasks.append(task)

    # Wait for all scans to complete
    results = await asyncio.gather(*scan_tasks, return_exceptions=True)

    # Process results
    total_issues = 0
    for result in results:
        if isinstance(result, Exception):
            print(f"Error scanning file: {result}")
        else:
            file_path, issues = result
            total_issues += issues
            print(f"{file_path}: {issues} issues")

    print(f"Total issues found: {total_issues}")

async def scan_file(client: TavoClient, file_path: Path):
    """Scan a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        result = await client.scan_code(code, "python")
        return str(file_path), result.total_issues
    except Exception as e:
        raise Exception(f"Failed to scan {file_path}: {e}")

async def main():
    async with TavoClient("your-api-key") as client:
        await scan_directory(client, Path("./src"))

if __name__ == "__main__":
    asyncio.run(main())
```

### AI Model Analysis

```python
import asyncio
from tavo import TavoClient

async def analyze_model():
    """Analyze an AI model for security issues."""
    async with TavoClient("your-api-key") as client:
        model_config = {
            "model_type": "transformer",
            "architecture": {
                "layers": 12,
                "attention_heads": 8,
                "hidden_size": 768,
                "vocab_size": 30000
            },
            "training": {
                "dataset": "wikipedia",
                "epochs": 10,
                "learning_rate": 1e-4
            }
        }

        analysis = await client.analyze_model(model_config)

        print(f"Model safety: {'Safe' if analysis.safe else 'Unsafe'}")
        if not analysis.safe:
            print("Issues found:")
            for issue in analysis.issues:
                print(f"- {issue.title}: {issue.description}")

if __name__ == "__main__":
    asyncio.run(analyze_model())
```

### Webhook Management

```python
import asyncio
from tavo import TavoClient

async def manage_webhooks():
    """Create and manage webhooks for scan notifications."""
    async with TavoClient("your-api-key") as client:
        # Create a webhook
        webhook = await client.create_webhook({
            "url": "https://myapp.com/webhook/scan-complete",
            "events": ["scan.completed", "vulnerability.found"],
            "secret": "webhook-secret"
        })

        print(f"Created webhook: {webhook.id}")

        # List all webhooks
        webhooks = await client.list_webhooks()
        print(f"Total webhooks: {len(webhooks)}")

        for wh in webhooks:
            print(f"- {wh.id}: {wh.url} ({', '.join(wh.events)})")

        # Delete the webhook
        await client.delete_webhook(webhook.id)
        print("Webhook deleted")

if __name__ == "__main__":
    asyncio.run(manage_webhooks())
```

### Organization Management

```python
import asyncio
from tavo import TavoClient

async def manage_organization():
    """Create and manage organizations."""
    async with TavoClient("your-api-key") as client:
        # Create organization
        org = await client.create_organization({
            "name": "Security Team",
            "description": "Handles security scanning and compliance",
            "settings": {
                "scan_frequency": "daily",
                "notification_channels": ["email", "slack"]
            }
        })

        print(f"Created organization: {org.name} (ID: {org.id})")

        # List organizations
        orgs = await client.list_organizations()
        print(f"Total organizations: {len(orgs)}")

        # Update organization
        updated_org = await client.update_organization(org.id, {
            "description": "Updated description"
        })

        print(f"Updated organization: {updated_org.description}")

if __name__ == "__main__":
    asyncio.run(manage_organization())
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tavo import TavoClient
import asyncio

app = FastAPI(title="Security Scan API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global client instance
tavo_client = None

@app.on_event("startup")
async def startup_event():
    global tavo_client
    tavo_client = TavoClient("your-api-key")

@app.on_event("shutdown")
async def shutdown_event():
    if tavo_client:
        await tavo_client.close()

class ScanRequest(BaseModel):
    code: str
    language: str = "python"
    async_scan: bool = False

class ScanResponse(BaseModel):
    total_issues: int
    vulnerabilities: list
    scan_id: str = None

@app.post("/scan", response_model=ScanResponse)
async def scan_code(request: ScanRequest, background_tasks: BackgroundTasks):
    """Scan code for security vulnerabilities."""
    try:
        if request.async_scan:
            # Start async scan
            scan_id = f"scan_{asyncio.get_event_loop().time()}"
            background_tasks.add_task(
                perform_async_scan,
                request.code,
                request.language,
                scan_id
            )
            return ScanResponse(
                total_issues=0,
                vulnerabilities=[],
                scan_id=scan_id
            )
        else:
            # Synchronous scan
            result = await tavo_client.scan_code(request.code, request.language)
            return ScanResponse(
                total_issues=result.total_issues,
                vulnerabilities=result.vulnerabilities
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def perform_async_scan(code: str, language: str, scan_id: str):
    """Perform async scan and store results."""
    try:
        result = await tavo_client.scan_code(code, language)
        # Store results in database/cache
        print(f"Async scan {scan_id} completed: {result.total_issues} issues")
    except Exception as e:
        print(f"Async scan {scan_id} failed: {e}")

@app.get("/scan/{scan_id}")
async def get_scan_result(scan_id: str):
    """Get async scan result."""
    # Retrieve from database/cache
    # This is a placeholder - implement actual storage
    return {"status": "completed", "message": "Implement result storage"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Flask Integration

```python
from flask import Flask, request, jsonify
from tavo import TavoClient
import asyncio

app = Flask(__name__)

# Global event loop for Flask
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Global client
tavo_client = TavoClient("your-api-key")

@app.route('/scan', methods=['POST'])
def scan_code():
    """Scan code for security vulnerabilities."""
    try:
        data = request.get_json()

        if not data or 'code' not in data:
            return jsonify({'error': 'Code is required'}), 400

        code = data['code']
        language = data.get('language', 'python')

        # Run async function in Flask
        result = loop.run_until_complete(
            tavo_client.scan_code(code, language)
        )

        return jsonify({
            'total_issues': result.total_issues,
            'vulnerabilities': [
                {
                    'title': v.title,
                    'description': v.description,
                    'severity': v.severity,
                    'location': {
                        'file': v.location.file if v.location else None,
                        'line': v.location.line if v.location else None,
                        'column': v.location.column if v.location else None
                    } if v.location else None
                }
                for v in result.vulnerabilities
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.teardown_appcontext
def cleanup(exception):
    """Clean up resources."""
    loop.run_until_complete(tavo_client.close())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### CLI Tool

```python
#!/usr/bin/env python3
"""
Tavo AI Security Scanner CLI Tool
"""

import asyncio
import argparse
import sys
from pathlib import Path
from tavo import TavoClient
from tavo.exceptions import TavoError

async def scan_file(client: TavoClient, file_path: Path, language: str):
    """Scan a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        result = await client.scan_code(code, language)

        if result.total_issues > 0:
            print(f"\n🔴 {file_path} ({result.total_issues} issues):")
            for i, vuln in enumerate(result.vulnerabilities, 1):
                print(f"  {i}. {vuln.title} ({vuln.severity})")
                print(f"     {vuln.description}")
                if vuln.location:
                    print(f"     📍 {vuln.location.file}:{vuln.location.line}:{vuln.location.column}")
        else:
            print(f"✅ {file_path} (0 issues)")

        return result.total_issues

    except Exception as e:
        print(f"❌ Error scanning {file_path}: {e}")
        return 0

async def scan_directory(client: TavoClient, directory: Path, language: str, recursive: bool):
    """Scan all files in a directory."""
    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"

    # Determine file extensions based on language
    extensions = {
        'python': ['*.py'],
        'javascript': ['*.js', '*.ts'],
        'java': ['*.java'],
        'go': ['*.go'],
        'csharp': ['*.cs'],
        'rust': ['*.rs']
    }

    file_patterns = extensions.get(language, [f"*.{language}"])

    total_issues = 0
    total_files = 0

    for pattern in file_patterns:
        for file_path in directory.glob(pattern):
            if file_path.is_file():
                issues = await scan_file(client, file_path, language)
                total_issues += issues
                total_files += 1

    print(f"\n📊 Summary: {total_files} files scanned, {total_issues} total issues")
    return total_issues

async def main():
    parser = argparse.ArgumentParser(description="Tavo AI Security Scanner")
    parser.add_argument('--api-key', help='Tavo AI API key')
    parser.add_argument('--language', '-l', default='python',
                       help='Programming language (default: python)')
    parser.add_argument('--recursive', '-r', action='store_true',
                       help='Scan directories recursively')
    parser.add_argument('path', help='File or directory to scan')

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.environ.get('TAVO_API_KEY')
    if not api_key:
        print("❌ API key required. Use --api-key or set TAVO_API_KEY environment variable")
        sys.exit(1)

    # Validate path
    path = Path(args.path)
    if not path.exists():
        print(f"❌ Path does not exist: {path}")
        sys.exit(1)

    async with TavoClient(api_key) as client:
        try:
            if path.is_file():
                issues = await scan_file(client, path, args.language)
                sys.exit(0 if issues == 0 else 1)
            else:
                issues = await scan_directory(client, path, args.language, args.recursive)
                sys.exit(0 if issues == 0 else 1)

        except TavoError as e:
            print(f"❌ Tavo API error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
```

### Django Integration

```python
# settings.py
TAVO_API_KEY = os.environ.get('TAVO_API_KEY')

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import asyncio
from tavo import TavoClient

# Global client (in production, use proper dependency injection)
tavo_client = None

def get_tavo_client():
    global tavo_client
    if tavo_client is None:
        from django.conf import settings
        tavo_client = TavoClient(settings.TAVO_API_KEY)
    return tavo_client

@csrf_exempt
@require_http_methods(["POST"])
def scan_code_view(request):
    """Scan code for security vulnerabilities."""
    try:
        data = json.loads(request.body)
        code = data.get('code')
        language = data.get('language', 'python')

        if not code:
            return JsonResponse({'error': 'Code is required'}, status=400)

        # Run async scan
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        client = get_tavo_client()
        result = loop.run_until_complete(
            client.scan_code(code, language)
        )

        return JsonResponse({
            'total_issues': result.total_issues,
            'vulnerabilities': [
                {
                    'title': v.title,
                    'description': v.description,
                    'severity': v.severity
                }
                for v in result.vulnerabilities
            ]
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

## Testing Examples

### Unit Tests

```python
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from tavo import TavoClient
from tavo.exceptions import TavoAPIError

class TestTavoClient:
    @pytest.fixture
    async def client(self):
        """Create a test client."""
        client = TavoClient("test-api-key")
        yield client
        await client.close()

    @pytest.mark.asyncio
    async def test_scan_code_success(self, client):
        """Test successful code scan."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "total_issues": 1,
            "vulnerabilities": [{
                "title": "SQL Injection",
                "description": "Potential SQL injection vulnerability",
                "severity": "high"
            }]
        })

        # Mock the session
        client._session.post = AsyncMock(return_value=mock_response)

        result = await client.scan_code("test code", "python")

        assert result.total_issues == 1
        assert len(result.vulnerabilities) == 1
        assert result.vulnerabilities[0].title == "SQL Injection"

    @pytest.mark.asyncio
    async def test_scan_code_api_error(self, client):
        """Test API error handling."""
        mock_response = MagicMock()
        mock_response.status = 400
        mock_response.json = AsyncMock(return_value={
            "error": "Invalid request"
        })

        client._session.post = AsyncMock(return_value=mock_response)

        with pytest.raises(TavoAPIError):
            await client.scan_code("test code", "python")

    @pytest.mark.asyncio
    async def test_scan_code_with_timeout(self, client):
        """Test scan with timeout."""
        import asyncio

        # Mock a slow response
        async def slow_response(*args, **kwargs):
            await asyncio.sleep(2)
            mock_resp = MagicMock()
            mock_resp.status = 200
            mock_resp.json = AsyncMock(return_value={"total_issues": 0, "vulnerabilities": []})
            return mock_resp

        client._session.post = slow_response

        # Should timeout
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(
                client.scan_code("test code", "python"),
                timeout=1.0
            )
```

### Integration Tests

```python
import pytest
import asyncio
from tavo import TavoClient

@pytest.mark.integration
class TestTavoIntegration:
    """Integration tests that require a real API connection."""

    @pytest.fixture
    async def client(self):
        """Create client with real API key from environment."""
        api_key = os.environ.get('TAVO_API_KEY')
        if not api_key:
            pytest.skip("TAVO_API_KEY environment variable not set")

        client = TavoClient(api_key)
        yield client
        await client.close()

    @pytest.mark.asyncio
    async def test_scan_vulnerable_code(self, client):
        """Test scanning code with known vulnerabilities."""
        vulnerable_code = '''
def authenticate(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    # SQL injection vulnerability
    return execute_query(query)
'''

        result = await client.scan_code(vulnerable_code, "python")

        assert result.total_issues > 0

        # Should detect SQL injection
        sql_injection_found = any(
            "sql" in vuln.title.lower() and "inject" in vuln.title.lower()
            for vuln in result.vulnerabilities
        )
        assert sql_injection_found, "SQL injection should be detected"

    @pytest.mark.asyncio
    async def test_scan_safe_code(self, client):
        """Test scanning safe code."""
        safe_code = '''
def authenticate(username, password):
    # Use parameterized queries
    query = "SELECT * FROM users WHERE username=? AND password=?"
    return execute_query(query, (username, password))
'''

        result = await client.scan_code(safe_code, "python")

        # Should not have critical/high severity issues
        high_severity_issues = [
            vuln for vuln in result.vulnerabilities
            if vuln.severity in ['critical', 'high']
        ]
        assert len(high_severity_issues) == 0, "Safe code should not have high-severity issues"
```
