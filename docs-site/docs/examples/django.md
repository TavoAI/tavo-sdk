---
sidebar_position: 1
---

# Django Integration

Integrate Tavo AI security scanning into your Django applications.

## Installation

```bash
pip install tavo-ai django
```

## Basic Setup

### Settings Configuration

Add Tavo AI configuration to your Django settings:

```python
# settings.py
import os

TAVO_CONFIG = {
    'API_KEY': os.getenv('TAVO_API_KEY'),
    'BASE_URL': os.getenv('TAVO_BASE_URL', 'https://api.tavo.ai'),
    'TIMEOUT': 30.0,
    'MAX_RETRIES': 3,
}
```

### Tavo Service Class

Create a service class for Tavo AI operations:

```python
# services/tavo_service.py
from typing import Dict, Any, Optional
from django.conf import settings
from tavo import TavoClient, TavoConfig

class TavoService:
    def __init__(self):
        config = TavoConfig(**settings.TAVO_CONFIG)
        self.client = TavoClient(config)

    def scan_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """Scan code for security vulnerabilities"""
        return self.client.scans().create_scan({
            'name': f'Code Scan - {language}',
            'target': code,
            'scan_type': 'code',
            'language': language,
        })

    def scan_url(self, url: str) -> Dict[str, Any]:
        """Scan a URL for security issues"""
        return self.client.scans().create_scan({
            'name': f'URL Scan - {url}',
            'target': url,
            'scan_type': 'web',
        })

    def get_scan_results(self, scan_id: str) -> Dict[str, Any]:
        """Get results for a specific scan"""
        return self.client.scans().get_scan_results(scan_id)

    def generate_report(self, scan_ids: list, format: str = 'pdf') -> Dict[str, Any]:
        """Generate a compliance report"""
        return self.client.reports().generate_report({
            'type': 'compliance',
            'format': format,
            'scan_ids': scan_ids,
        })

# Singleton instance
tavo_service = TavoService()
```

## Django Views Integration

### Code Scanning View

```python
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .services.tavo_service import tavo_service

@csrf_exempt
@require_POST
def scan_code(request):
    """API endpoint for code scanning"""
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        language = data.get('language', 'python')

        if not code:
            return JsonResponse({'error': 'Code is required'}, status=400)

        result = tavo_service.scan_code(code, language)
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def scan_results(request, scan_id):
    """Get scan results"""
    try:
        results = tavo_service.get_scan_results(scan_id)
        return JsonResponse(results)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

### URL Scanning View

```python
# views.py (continued)
@csrf_exempt
@require_POST
def scan_url(request):
    """API endpoint for URL scanning"""
    try:
        data = json.loads(request.body)
        url = data.get('url', '')

        if not url:
            return JsonResponse({'error': 'URL is required'}, status=400)

        result = tavo_service.scan_url(url)
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

## Django Templates

### Code Scanner Template

```html
<!-- templates/code_scanner.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Tavo AI Code Scanner</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold mb-8">AI Security Code Scanner</h1>

        <div class="bg-white rounded-lg shadow-md p-6">
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Programming Language
                </label>
                <select id="language" class="w-full p-2 border border-gray-300 rounded-md">
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
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
                    class="w-full p-2 border border-gray-300 rounded-md font-mono"
                    placeholder="Paste your code here..."
                ></textarea>
            </div>

            <button
                id="scanBtn"
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
                Scan Code
            </button>
        </div>

        <div id="results" class="mt-8 hidden">
            <h2 class="text-xl font-bold mb-4">Scan Results</h2>
            <div id="resultsContent" class="bg-white rounded-lg shadow-md p-6">
                <!-- Results will be displayed here -->
            </div>
        </div>
    </div>

    <script>
        document.getElementById('scanBtn').addEventListener('click', async () => {
            const code = document.getElementById('code').value;
            const language = document.getElementById('language').value;
            const scanBtn = document.getElementById('scanBtn');
            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');

            if (!code.trim()) {
                alert('Please enter some code to scan');
                return;
            }

            scanBtn.disabled = true;
            scanBtn.textContent = 'Scanning...';

            try {
                const response = await fetch('/api/scan-code/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({ code, language })
                });

                const result = await response.json();

                if (response.ok) {
                    resultsContent.innerHTML = `
                        <div class="mb-4">
                            <h3 class="text-lg font-semibold">Scan ID: ${result.id}</h3>
                            <p class="text-sm text-gray-600">Status: ${result.status}</p>
                        </div>
                        <div class="mb-4">
                            <h4 class="font-semibold">Summary:</h4>
                            <ul class="list-disc list-inside">
                                <li>Files scanned: ${result.summary?.files_scanned || 0}</li>
                                <li>Vulnerabilities found: ${result.summary?.vulnerabilities_found || 0}</li>
                                <li>Scan duration: ${result.summary?.duration || 'N/A'}</li>
                            </ul>
                        </div>
                        <a href="/scan-results/${result.id}/" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
                            View Detailed Results
                        </a>
                    `;
                    resultsDiv.classList.remove('hidden');
                } else {
                    resultsContent.innerHTML = `<div class="text-red-600">Error: ${result.error}</div>`;
                    resultsDiv.classList.remove('hidden');
                }
            } catch (error) {
                resultsContent.innerHTML = `<div class="text-red-600">Error: ${error.message}</div>`;
                resultsDiv.classList.remove('hidden');
            } finally {
                scanBtn.disabled = false;
                scanBtn.textContent = 'Scan Code';
            }
        });
    </script>
</body>
</html>
```

## Django URLs

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('scan-code/', views.scan_code, name='scan_code'),
    path('scan-url/', views.scan_url, name='scan_url'),
    path('scan-results/<str:scan_id>/', views.scan_results, name='scan_results'),
    path('code-scanner/', views.code_scanner_page, name='code_scanner'),
]
```

## Middleware for Automatic Scanning

### Request Logging Middleware

```python
# middleware.py
import json
from django.conf import settings
from .services.tavo_service import tavo_service

class SecurityScanMiddleware:
    """Middleware to automatically scan requests for security issues"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request for security analysis
        if hasattr(settings, 'TAVO_AUTO_SCAN') and settings.TAVO_AUTO_SCAN:
            self._log_request_for_scanning(request)

        response = self.get_response(request)
        return response

    def _log_request_for_scanning(self, request):
        """Log request data for later security scanning"""
        try:
            request_data = {
                'method': request.method,
                'path': request.path,
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'ip': self._get_client_ip(request),
                'timestamp': timezone.now().isoformat(),
            }

            # Store in cache or database for batch processing
            cache_key = f"tavo_request_{timezone.now().timestamp()}"
            cache.set(cache_key, request_data, timeout=3600)  # 1 hour

        except Exception as e:
            # Don't let logging failures break the request
            logger.warning(f"Failed to log request for security scanning: {e}")

    def _get_client_ip(self, request):
        """Get the client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

## Background Tasks with Celery

### Celery Task for Scanning

```python
# tasks.py
from celery import shared_task
from .services.tavo_service import tavo_service

@shared_task
def scan_code_async(code, language='python', callback_url=None):
    """Asynchronous code scanning task"""
    try:
        result = tavo_service.scan_code(code, language)

        # Send callback if provided
        if callback_url:
            import requests
            requests.post(callback_url, json=result)

        return result
    except Exception as e:
        # Handle errors appropriately
        return {'error': str(e)}

@shared_task
def generate_security_report(scan_ids, format='pdf'):
    """Generate security report for multiple scans"""
    try:
        report = tavo_service.generate_report(scan_ids, format)
        return report
    except Exception as e:
        return {'error': str(e)}
```

### Using Celery Tasks in Views

```python
# views.py (continued)
from .tasks import scan_code_async

@csrf_exempt
@require_POST
def scan_code_async(request):
    """Asynchronous code scanning"""
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        language = data.get('language', 'python')
        callback_url = data.get('callback_url')

        if not code:
            return JsonResponse({'error': 'Code is required'}, status=400)

        # Start async task
        task = scan_code_async.delay(code, language, callback_url)

        return JsonResponse({
            'task_id': task.id,
            'status': 'accepted'
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def task_status(request, task_id):
    """Check the status of an async task"""
    from celery.result import AsyncResult
    from .tasks import app as celery_app

    task_result = AsyncResult(task_id, app=celery_app)

    response = {
        'task_id': task_id,
        'status': task_result.status,
    }

    if task_result.ready():
        response['result'] = task_result.result

    return JsonResponse(response)
```

## Testing

### Unit Tests

```python
# tests.py
from django.test import TestCase
from unittest.mock import patch, MagicMock
from .services.tavo_service import TavoService

class TavoServiceTest(TestCase):
    def setUp(self):
        self.service = TavoService()

    @patch('tavo.TavoClient')
    def test_scan_code(self, mock_client):
        # Mock the client
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.scans.return_value.create_scan.return_value = {
            'id': 'test-scan-id',
            'status': 'completed'
        }

        result = self.service.scan_code("print('hello')", "python")

        self.assertEqual(result['id'], 'test-scan-id')
        self.assertEqual(result['status'], 'completed')
        mock_instance.scans.return_value.create_scan.assert_called_once()
```

## Deployment Considerations

### Environment Variables

```bash
# Production environment variables
TAVO_API_KEY=your-production-api-key
TAVO_BASE_URL=https://api.tavo.ai
TAVO_AUTO_SCAN=true
```

### Health Checks

```python
# health_checks.py
from django.core.checks import CheckMessage, Error
from .services.tavo_service import tavo_service

def check_tavo_connection(app_configs, **kwargs):
    """Check Tavo AI service connectivity"""
    errors = []

    try:
        health = tavo_service.client.health_check()
        if health.get('status') != 'healthy':
            errors.append(
                Error(
                    'Tavo AI service unhealthy',
                    hint='Check Tavo AI service status and configuration',
                    id='tavo.E001',
                )
            )
    except Exception as e:
        errors.append(
            Error(
                f'Tavo AI connection failed: {e}',
                hint='Check TAVO_API_KEY and network connectivity',
                id='tavo.E002',
            )
        )

    return errors
```

This Django integration provides a complete example of how to incorporate Tavo AI security scanning into Django applications, with both synchronous and asynchronous processing capabilities.
