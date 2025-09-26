---
sidebar_position: 3
---

# Flask Integration

Integrate Tavo AI security scanning into your Flask applications.

## Installation

```bash
pip install tavo-ai flask flask-cors python-dotenv
```

## Basic Setup

### Environment Configuration

```bash
# .env
TAVO_API_KEY=your-api-key-here
TAVO_BASE_URL=https://api.tavo.ai
TAVO_TIMEOUT=30.0
TAVO_MAX_RETRIES=3
FLASK_ENV=development
FLASK_DEBUG=True
```

### Tavo Service Class

```python
# services/tavo_service.py
import os
from typing import Dict, Any, Optional
from tavo import TavoClient, TavoConfig

class TavoService:
    def __init__(self):
        self.config = TavoConfig(
            api_key=os.getenv('TAVO_API_KEY'),
            base_url=os.getenv('TAVO_BASE_URL', 'https://api.tavo.ai'),
            timeout=float(os.getenv('TAVO_TIMEOUT', 30.0)),
            max_retries=int(os.getenv('TAVO_MAX_RETRIES', 3)),
        )
        self.client = TavoClient(self.config)

    def scan_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """Scan code for security vulnerabilities"""
        try:
            return self.client.scans().create_scan({
                'name': f'Code Scan - {language}',
                'target': code,
                'scan_type': 'code',
                'language': language,
            })
        except Exception as e:
            raise Exception(f"Code scan failed: {str(e)}")

    def scan_url(self, url: str) -> Dict[str, Any]:
        """Scan a URL for security issues"""
        try:
            return self.client.scans().create_scan({
                'name': f'URL Scan - {url}',
                'target': url,
                'scan_type': 'web',
            })
        except Exception as e:
            raise Exception(f"URL scan failed: {str(e)}")

    def get_scan_results(self, scan_id: str) -> Dict[str, Any]:
        """Get results for a specific scan"""
        try:
            return self.client.scans().get_scan_results(scan_id)
        except Exception as e:
            raise Exception(f"Failed to get scan results: {str(e)}")

    def generate_report(self, scan_ids: list, format: str = 'pdf') -> Dict[str, Any]:
        """Generate a compliance report"""
        try:
            return self.client.reports().generate_report({
                'type': 'compliance',
                'format': format,
                'scan_ids': scan_ids,
            })
        except Exception as e:
            raise Exception(f"Report generation failed: {str(e)}")

# Singleton instance
tavo_service = TavoService()
```

## Flask Routes

### Code Scanning Routes

```python
# routes/scan.py
from flask import Blueprint, request, jsonify
from services.tavo_service import tavo_service

scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/code', methods=['POST'])
def scan_code():
    """Scan code for security vulnerabilities"""
    try:
        data = request.get_json()

        if not data or 'code' not in data:
            return jsonify({
                'error': 'Code is required',
                'code': 'MISSING_CODE'
            }), 400

        code = data['code']
        language = data.get('language', 'python')

        result = tavo_service.scan_code(code, language)

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'SCAN_FAILED'
        }), 500

@scan_bp.route('/url', methods=['POST'])
def scan_url():
    """Scan a URL for security issues"""
    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({
                'error': 'URL is required',
                'code': 'MISSING_URL'
            }), 400

        url = data['url']

        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                'error': 'Invalid URL format',
                'code': 'INVALID_URL'
            }), 400

        result = tavo_service.scan_url(url)

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'SCAN_FAILED'
        }), 500

@scan_bp.route('/<scan_id>/results', methods=['GET'])
def get_scan_results(scan_id):
    """Get results for a specific scan"""
    try:
        result = tavo_service.get_scan_results(scan_id)

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'RESULTS_FAILED'
        }), 500
```

### Report Routes

```python
# routes/reports.py
from flask import Blueprint, request, jsonify
from services.tavo_service import tavo_service

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/generate', methods=['POST'])
def generate_report():
    """Generate a compliance report"""
    try:
        data = request.get_json()

        if not data or 'scan_ids' not in data:
            return jsonify({
                'error': 'Scan IDs are required',
                'code': 'MISSING_SCAN_IDS'
            }), 400

        scan_ids = data['scan_ids']
        report_format = data.get('format', 'pdf')

        if not isinstance(scan_ids, list) or len(scan_ids) == 0:
            return jsonify({
                'error': 'At least one scan ID is required',
                'code': 'INVALID_SCAN_IDS'
            }), 400

        result = tavo_service.generate_report(scan_ids, report_format)

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'REPORT_FAILED'
        }), 500
```

## Main Application

```python
# app.py
from flask import Flask, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from routes.scan import scan_bp
from routes.reports import reports_bp

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Enable CORS
    CORS(app, origins=['http://localhost:3000', 'http://localhost:5000'])

    # Register blueprints
    app.register_blueprint(scan_bp, url_prefix='/api/scan')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'service': 'tavo-flask-integration',
            'timestamp': datetime.utcnow().isoformat()
        }

    # Web interface routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/scan')
    def scan_page():
        return render_template('scan.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG']
    )
```

## Middleware for Automatic Scanning

### Request Security Middleware

```python
# middleware/security.py
from functools import wraps
from flask import request, g
from services.tavo_service import tavo_service
import threading
import time

class SecurityMiddleware:
    def __init__(self, app):
        self.app = app
        self.rate_limits = {}
        self.rate_limit_window = 900  # 15 minutes
        self.rate_limit_max = 100

    def init_app(self, app):
        @app.before_request
        def before_request():
            self._check_rate_limit()
            self._scan_request_body()

        @app.after_request
        def after_request(response):
            # Add security headers
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            return response

    def _check_rate_limit(self):
        """Check rate limiting for scan endpoints"""
        if request.path.startswith('/api/scan'):
            client_ip = request.remote_addr
            now = time.time()

            # Clean old entries
            self.rate_limits[client_ip] = [
                timestamp for timestamp in self.rate_limits.get(client_ip, [])
                if now - timestamp < self.rate_limit_window
            ]

            if len(self.rate_limits[client_ip]) >= self.rate_limit_max:
                from flask import abort
                abort(429, description="Too many requests")

            self.rate_limits[client_ip].append(now)

    def _scan_request_body(self):
        """Automatically scan code in request bodies"""
        if request.method in ['POST', 'PUT', 'PATCH'] and request.is_json:
            data = request.get_json(silent=True)
            if data and 'code' in data:
                language = data.get('language', 'python')

                # Perform scan asynchronously
                def async_scan():
                    try:
                        result = tavo_service.scan_code(data['code'], language)
                        g.scan_result = result
                        print(f"Security scan completed: {result.get('id')}")
                    except Exception as e:
                        print(f"Background security scan failed: {e}")

                thread = threading.Thread(target=async_scan)
                thread.daemon = True
                thread.start()
```

### Apply Middleware

```python
# app.py (continued)
from middleware.security import SecurityMiddleware

def create_app():
    # ... existing code ...

    # Initialize security middleware
    security_middleware = SecurityMiddleware(app)
    security_middleware.init_app(app)

    # ... rest of the code ...
```

## Templates

### Base Template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Tavo AI Security Scanner{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    {% block head %}{% endblock %}
</head>
<body class="bg-gray-100 min-h-screen">
    <nav class="bg-blue-600 text-white p-4">
        <div class="container mx-auto">
            <h1 class="text-xl font-bold">Tavo AI Security Scanner</h1>
        </div>
    </nav>

    <main class="container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </main>

    <script>
        // Global error handler
        window.addEventListener('error', function(e) {
            console.error('Global error:', e.error);
        });
    </script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Code Scanner Template

```html
<!-- templates/scan.html -->
{% extends "base.html" %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <!-- Code Scanner -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-2xl font-semibold mb-4">Code Security Scan</h2>

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
                class="w-full p-2 border border-gray-300 rounded-md font-mono text-sm"
                placeholder="Paste your code here..."
            ></textarea>
        </div>

        <button
            id="scanCodeBtn"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
            Scan Code
        </button>
    </div>

    <!-- URL Scanner -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-2xl font-semibold mb-4">URL Security Scan</h2>

        <div class="mb-4">
            <input
                type="url"
                id="url"
                class="w-full p-2 border border-gray-300 rounded-md"
                placeholder="https://example.com"
            >
        </div>

        <button
            id="scanUrlBtn"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
            Scan URL
        </button>
    </div>

    <!-- Results -->
    <div id="results" class="bg-white rounded-lg shadow-md p-6 hidden">
        <h2 class="text-2xl font-semibold mb-4">Scan Results</h2>
        <div id="resultsContent"></div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    const API_BASE = '/api';

    // Code scanning
    document.getElementById('scanCodeBtn').addEventListener('click', async () => {
        const code = document.getElementById('code').value;
        const language = document.getElementById('language').value;
        const btn = document.getElementById('scanCodeBtn');

        if (!code.trim()) {
            alert('Please enter some code to scan');
            return;
        }

        btn.disabled = true;
        btn.textContent = 'Scanning...';

        try {
            const response = await fetch(`${API_BASE}/scan/code`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code, language })
            });

            const result = await response.json();
            displayResults(result);

        } catch (error) {
            displayResults({ error: error.message });
        } finally {
            btn.disabled = false;
            btn.textContent = 'Scan Code';
        }
    });

    // URL scanning
    document.getElementById('scanUrlBtn').addEventListener('click', async () => {
        const url = document.getElementById('url').value;
        const btn = document.getElementById('scanUrlBtn');

        if (!url.trim()) {
            alert('Please enter a URL to scan');
            return;
        }

        btn.disabled = true;
        btn.textContent = 'Scanning...';

        try {
            const response = await fetch(`${API_BASE}/scan/url`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url })
            });

            const result = await response.json();
            displayResults(result);

        } catch (error) {
            displayResults({ error: error.message });
        } finally {
            btn.disabled = false;
            btn.textContent = 'Scan URL';
        }
    });

    function displayResults(result) {
        const resultsDiv = document.getElementById('results');
        const resultsContent = document.getElementById('resultsContent');

        if (result.success) {
            const data = result.data;
            resultsContent.innerHTML = `
                <div class="mb-4">
                    <h3 class="text-lg font-semibold text-green-600">Scan Successful</h3>
                    <p class="text-sm text-gray-600">Scan ID: ${data.id}</p>
                    <p class="text-sm text-gray-600">Status: ${data.status}</p>
                </div>
                ${data.summary ? `
                <div class="mb-4">
                    <h4 class="font-semibold">Summary:</h4>
                    <ul class="list-disc list-inside text-sm">
                        <li>Files scanned: ${data.summary.files_scanned || 0}</li>
                        <li>Vulnerabilities found: ${data.summary.vulnerabilities_found || 0}</li>
                        <li>Scan duration: ${data.summary.duration || 'N/A'}</li>
                    </ul>
                </div>
                ` : ''}
                <button
                    onclick="viewDetailedResults('${data.id}')"
                    class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                    View Detailed Results
                </button>
            `;
        } else {
            resultsContent.innerHTML = `
                <div class="text-red-600">
                    <h3 class="text-lg font-semibold">Scan Failed</h3>
                    <p>${result.error}</p>
                </div>
            `;
        }

        resultsDiv.classList.remove('hidden');
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }

    async function viewDetailedResults(scanId) {
        try {
            const response = await fetch(`${API_BASE}/scan/${scanId}/results`);
            const result = await response.json();

            if (result.success) {
                // Display detailed results (implement as needed)
                console.log('Detailed results:', result.data);
            }
        } catch (error) {
            console.error('Failed to get detailed results:', error);
        }
    }
</script>
{% endblock %}
```

## Testing

### Unit Tests with pytest

```python
# tests/test_tavo_service.py
import pytest
from unittest.mock import patch, MagicMock
from services.tavo_service import TavoService

class TestTavoService:
    @patch('tavo.TavoClient')
    def test_scan_code_success(self, mock_client):
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.scans.return_value.create_scan.return_value = {
            'id': 'test-scan-id',
            'status': 'completed'
        }

        service = TavoService()
        result = service.scan_code("print('hello')", "python")

        assert result['id'] == 'test-scan-id'
        assert result['status'] == 'completed'
        mock_instance.scans.return_value.create_scan.assert_called_once()

    @patch('tavo.TavoClient')
    def test_scan_code_failure(self, mock_client):
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.scans.return_value.create_scan.side_effect = Exception("API Error")

        service = TavoService()

        with pytest.raises(Exception, match="Code scan failed: API Error"):
            service.scan_code("invalid code", "python")
```

### API Tests with Flask-Testing

```python
# tests/test_routes.py
import json
import pytest
from flask import Flask
from flask_testing import TestCase
from app import create_app
from services.tavo_service import tavo_service

class TestScanRoutes(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.client = self.app.test_client()

    @patch.object(tavo_service, 'scan_code')
    def test_scan_code_success(self, mock_scan):
        mock_scan.return_value = {
            'id': 'test-scan-id',
            'status': 'completed',
            'summary': {'vulnerabilities_found': 0}
        }

        response = self.client.post('/api/scan/code',
            data=json.dumps({
                'code': 'print("hello")',
                'language': 'python'
            }),
            content_type='application/json'
        )

        self.assert200(response)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['id'], 'test-scan-id')

    def test_scan_code_missing_code(self):
        response = self.client.post('/api/scan/code',
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assert400(response)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Code is required')
```

## Background Tasks with Celery

### Celery Configuration

```python
# celery_app.py
from celery import Celery
from app import create_app

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

flask_app = create_app()
celery = make_celery(flask_app)
```

### Celery Tasks

```python
# tasks.py
from celery_app import celery
from services.tavo_service import tavo_service

@celery.task
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
        return {'error': str(e)}

@celery.task
def generate_security_report(scan_ids, format='pdf'):
    """Generate security report for multiple scans"""
    try:
        report = tavo_service.generate_report(scan_ids, format)
        return report
    except Exception as e:
        return {'error': str(e)}
```

### Using Celery Tasks in Routes

```python
# routes/scan.py (continued)
from tasks import scan_code_async

@scan_bp.route('/code/async', methods=['POST'])
def scan_code_async_route():
    """Asynchronous code scanning"""
    try:
        data = request.get_json()

        if not data or 'code' not in data:
            return jsonify({
                'error': 'Code is required',
                'code': 'MISSING_CODE'
            }), 400

        code = data['code']
        language = data.get('language', 'python')
        callback_url = data.get('callback_url')

        # Start async task
        task = scan_code_async.delay(code, language, callback_url)

        return jsonify({
            'task_id': task.id,
            'status': 'accepted'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'SCAN_FAILED'
        }), 500

@scan_bp.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Check the status of an async task"""
    from celery.result import AsyncResult
    from celery_app import celery

    task_result = AsyncResult(task_id, app=celery)

    response = {
        'task_id': task_id,
        'status': task_result.status,
    }

    if task_result.ready():
        response['result'] = task_result.result

    return jsonify(response)
```

## Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 5000

CMD ["python", "app.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  tavo-flask:
    build: .
    ports:
      - "5000:5000"
    environment:
      - TAVO_API_KEY=${TAVO_API_KEY}
      - TAVO_BASE_URL=https://api.tavo.ai
      - FLASK_ENV=production
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  celery:
    build: .
    command: celery -A celery_app.celery worker --loglevel=info
    environment:
      - TAVO_API_KEY=${TAVO_API_KEY}
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis://redis:6379/0
    depends_on:
      - redis
    restart: unless-stopped

volumes:
  redis_data:
```

### requirements.txt

```text
tavo-ai==1.0.0
flask==2.3.3
flask-cors==4.0.0
python-dotenv==1.0.0
celery==5.3.1
redis==4.6.0
pytest==7.4.0
flask-testing==1.0.0
```

## Deployment

### Gunicorn Configuration

```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
```

### Production Startup Script

```bash
#!/bin/bash
# start.sh

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis is ready!"

# Start Celery worker
echo "Starting Celery worker..."
celery -A celery_app.celery worker --loglevel=info &

# Start Flask app with Gunicorn
echo "Starting Flask app..."
exec gunicorn --config gunicorn.conf.py app:create_app()
```

This Flask integration provides a comprehensive solution for incorporating Tavo AI security scanning into Python web applications with both synchronous and asynchronous processing capabilities, extensive testing, and production-ready deployment configurations.
