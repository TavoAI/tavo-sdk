---
sidebar_position: 8
---

# FastAPI Integration

Integrate Tavo AI security scanning into your FastAPI applications.

## Installation

```bash
pip install fastapi uvicorn httpx tavo-ai
```

## Basic Setup

### Environment Configuration

```python
# .env
TAVO_API_KEY=your-api-key-here
TAVO_BASE_URL=https://api.tavoai.net
TAVO_TIMEOUT=30
```

```python
# config.py
import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    tavo_api_key: str = os.getenv("TAVO_API_KEY", "")
    tavo_base_url: str = os.getenv("TAVO_BASE_URL", "https://api.tavoai.net")
    tavo_timeout: int = int(os.getenv("TAVO_TIMEOUT", "30"))

    class Config:
        env_file = ".env"

settings = Settings()
```

### Tavo Service

```python
# services/tavo_service.py
import httpx
from typing import Dict, Any, Optional, List
from fastapi import HTTPException
import asyncio
from config import settings

class TavoService:
    def __init__(self):
        self.api_key = settings.tavo_api_key
        self.base_url = settings.tavo_base_url
        self.timeout = settings.tavo_timeout

        if not self.api_key:
            raise ValueError("TAVO_API_KEY environment variable is required")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make authenticated request to Tavo API"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers, params=params)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=headers, json=data)
                elif method.upper() == "PUT":
                    response = await client.put(url, headers=headers, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Tavo API error: {e.response.text}"
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=503,
                    detail=f"Failed to connect to Tavo API: {str(e)}"
                )

    async def scan_code(
        self,
        code: str,
        language: str = "python",
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Scan code for security vulnerabilities"""
        if not name:
            name = f"Code Scan - {language}"

        data = {
            "name": name,
            "target": code,
            "scan_type": "code",
            "language": language
        }

        return await self._make_request("POST", "/scans", data=data)

    async def scan_url(
        self,
        url: str,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Scan URL for security vulnerabilities"""
        if not name:
            name = f"URL Scan - {url}"

        data = {
            "name": name,
            "target": url,
            "scan_type": "web"
        }

        return await self._make_request("POST", "/scans", data=data)

    async def get_scan_results(self, scan_id: str) -> Dict[str, Any]:
        """Get detailed scan results"""
        return await self._make_request("GET", f"/scans/{scan_id}/results")

    async def get_scan_status(self, scan_id: str) -> Dict[str, Any]:
        """Get scan status"""
        return await self._make_request("GET", f"/scans/{scan_id}")

    async def list_scans(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """List scans with pagination"""
        params = {
            "limit": limit,
            "offset": offset
        }
        if status:
            params["status"] = status

        return await self._make_request("GET", "/scans", params=params)

    async def generate_report(
        self,
        scan_ids: List[str],
        report_type: str = "compliance",
        format: str = "pdf"
    ) -> Dict[str, Any]:
        """Generate security report"""
        data = {
            "type": report_type,
            "format": format,
            "scan_ids": scan_ids
        }

        return await self._make_request("POST", "/reports", data=data)

    async def get_report_status(self, report_id: str) -> Dict[str, Any]:
        """Get report generation status"""
        return await self._make_request("GET", f"/reports/{report_id}")

    async def download_report(self, report_id: str) -> bytes:
        """Download generated report"""
        url = f"{self.base_url}/reports/{report_id}/download"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.content
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Failed to download report: {e.response.text}"
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=503,
                    detail=f"Failed to connect to Tavo API: {str(e)}"
                )

# Global service instance
tavo_service = TavoService()
```

## FastAPI Application

### Models

```python
# models.py
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class ScanType(str, Enum):
    CODE = "code"
    WEB = "web"

class Language(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"

class ScanRequest(BaseModel):
    name: str = Field(..., description="Name of the scan")
    target: str = Field(..., description="Code or URL to scan")
    scan_type: ScanType = Field(..., description="Type of scan")
    language: Optional[Language] = Field(None, description="Programming language")

class ReportRequest(BaseModel):
    scan_ids: List[str] = Field(..., description="List of scan IDs to include")
    report_type: str = Field("compliance", description="Type of report")
    format: str = Field("pdf", description="Report format")

class ScanResponse(BaseModel):
    id: str
    status: str
    name: str
    scan_type: str
    created_at: str
    summary: Optional[Dict[str, Any]] = None

class ReportResponse(BaseModel):
    id: str
    status: str
    report_type: str
    format: str
    created_at: str
    download_url: Optional[str] = None
```

### API Routes

```python
# routes/scans.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List, Optional
from models import ScanRequest, ScanResponse, ReportRequest, ReportResponse
from services.tavo_service import tavo_service

router = APIRouter(prefix="/api/scans", tags=["scans"])

@router.post("/", response_model=ScanResponse)
async def create_scan(scan_request: ScanRequest, background_tasks: BackgroundTasks):
    """Create a new security scan"""
    try:
        if scan_request.scan_type == "code":
            result = await tavo_service.scan_code(
                scan_request.target,
                scan_request.language or "python",
                scan_request.name
            )
        elif scan_request.scan_type == "web":
            result = await tavo_service.scan_url(
                scan_request.target,
                scan_request.name
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid scan type")

        return ScanResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(scan_id: str):
    """Get scan details"""
    try:
        result = await tavo_service.get_scan_status(scan_id)
        return ScanResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{scan_id}/results")
async def get_scan_results(scan_id: str):
    """Get detailed scan results"""
    try:
        result = await tavo_service.get_scan_results(scan_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ScanResponse])
async def list_scans(
    limit: int = 50,
    offset: int = 0,
    status: Optional[str] = None
):
    """List scans with pagination"""
    try:
        result = await tavo_service.list_scans(limit, offset, status)
        return [ScanResponse(**scan) for scan in result.get("scans", [])]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reports", response_model=ReportResponse)
async def generate_report(report_request: ReportRequest):
    """Generate security report"""
    try:
        result = await tavo_service.generate_report(
            report_request.scan_ids,
            report_request.report_type,
            report_request.format
        )
        return ReportResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report_status(report_id: str):
    """Get report generation status"""
    try:
        result = await tavo_service.get_report_status(report_id)
        return ReportResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/{report_id}/download")
async def download_report(report_id: str):
    """Download generated report"""
    try:
        content = await tavo_service.download_report(report_id)

        # Determine content type based on report format
        report_info = await tavo_service.get_report_status(report_id)
        format_type = report_info.get("format", "pdf")

        if format_type == "pdf":
            media_type = "application/pdf"
        elif format_type == "json":
            media_type = "application/json"
        elif format_type == "html":
            media_type = "text/html"
        else:
            media_type = "application/octet-stream"

        from fastapi.responses import Response
        return Response(
            content=content,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename=report.{format_type}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Main Application

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
from routes.scans import router as scans_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tavo AI Security Scanner API",
    description="FastAPI integration for Tavo AI security scanning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]  # Add your domain in production
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tavo-fastapi"}

# Include routers
app.include_router(scans_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Middleware

### Rate Limiting

```python
# middleware/rate_limit.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < 60
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

        # Add current request
        self.requests[client_ip].append(current_time)

        response = await call_next(request)
        return response
```

### Logging Middleware

```python
# middleware/logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url}")

        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} - "
            f"Process time: {process_time:.3f}s"
        )

        return response
```

### Update main.py with middleware

```python
# main.py (updated)
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
from routes.scans import router as scans_router
from middleware.rate_limit import RateLimitMiddleware
from middleware.logging import LoggingMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tavo AI Security Scanner API",
    description="FastAPI integration for Tavo AI security scanning",
    version="1.0.0"
)

# Add custom middleware
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
app.add_middleware(LoggingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

# ... rest of the code remains the same
```

## Background Tasks

### Scan Processor

```python
# tasks/scan_processor.py
import asyncio
from typing import Dict, Any
import logging
from services.tavo_service import tavo_service

logger = logging.getLogger(__name__)

class ScanProcessor:
    def __init__(self):
        self.active_scans = {}

    async def process_scan(self, scan_id: str):
        """Process a scan asynchronously"""
        try:
            logger.info(f"Starting scan processing for {scan_id}")

            # Wait for scan to complete
            while True:
                status = await tavo_service.get_scan_status(scan_id)
                scan_status = status.get("status")

                if scan_status == "completed":
                    logger.info(f"Scan {scan_id} completed successfully")
                    break
                elif scan_status == "failed":
                    logger.error(f"Scan {scan_id} failed")
                    break
                elif scan_status == "running":
                    await asyncio.sleep(5)  # Wait 5 seconds before checking again
                else:
                    logger.warning(f"Unknown scan status: {scan_status}")
                    await asyncio.sleep(5)

            # Get final results
            results = await tavo_service.get_scan_results(scan_id)

            # Here you could send notifications, update database, etc.
            logger.info(f"Scan {scan_id} processing complete")

        except Exception as e:
            logger.error(f"Error processing scan {scan_id}: {e}")
        finally:
            # Clean up
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]

    def start_scan_processing(self, scan_id: str):
        """Start background processing for a scan"""
        if scan_id not in self.active_scans:
            self.active_scans[scan_id] = True
            asyncio.create_task(self.process_scan(scan_id))

# Global processor instance
scan_processor = ScanProcessor()
```

### Update routes to use background tasks

```python
# routes/scans.py (updated)
from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List, Optional
from models import ScanRequest, ScanResponse, ReportRequest, ReportResponse
from services.tavo_service import tavo_service
from tasks.scan_processor import scan_processor

router = APIRouter(prefix="/api/scans", tags=["scans"])

@router.post("/", response_model=ScanResponse)
async def create_scan(
    scan_request: ScanRequest,
    background_tasks: BackgroundTasks
):
    """Create a new security scan"""
    try:
        if scan_request.scan_type == "code":
            result = await tavo_service.scan_code(
                scan_request.target,
                scan_request.language or "python",
                scan_request.name
            )
        elif scan_request.scan_type == "web":
            result = await tavo_service.scan_url(
                scan_request.target,
                scan_request.name
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid scan type")

        # Start background processing
        background_tasks.add_task(scan_processor.start_scan_processing, result["id"])

        return ScanResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ... rest of the routes remain the same
```

## Testing

### Test Configuration

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app
import os

@pytest.fixture
def client():
    # Set test environment variables
    os.environ["TAVO_API_KEY"] = "test-api-key"
    os.environ["TAVO_BASE_URL"] = "https://api.tavoai.net"

    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def mock_tavo_response():
    return {
        "id": "test-scan-id",
        "status": "completed",
        "name": "Test Scan",
        "scan_type": "code",
        "created_at": "2023-01-01T00:00:00Z",
        "summary": {
            "files_scanned": 1,
            "vulnerabilities_found": 0,
            "duration": "5.2s"
        }
    }
```

### Service Tests

```python
# tests/test_tavo_service.py
import pytest
from unittest.mock import AsyncMock, patch
from services.tavo_service import TavoService
from fastapi import HTTPException

class TestTavoService:
    @pytest.fixture
    def service(self):
        with patch.dict('os.environ', {'TAVO_API_KEY': 'test-key'}):
            return TavoService()

    @pytest.mark.asyncio
    async def test_scan_code_success(self, service):
        mock_response = {
            "id": "test-id",
            "status": "completed",
            "name": "Test Scan"
        }

        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = AsyncMock()
            mock_instance.post.return_value.json.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await service.scan_code("print('hello')", "python")

            assert result == mock_response
            mock_instance.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_scan_code_api_error(self, service):
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_response = AsyncMock()
            mock_response.raise_for_status.side_effect = Exception("API Error")
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(HTTPException):
                await service.scan_code("invalid code", "python")

    def test_init_without_api_key(self):
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="TAVO_API_KEY environment variable is required"):
                TavoService()
```

### API Tests

```python
# tests/test_scans_api.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

class TestScansAPI:
    def test_create_scan_code(self, client, mock_tavo_response):
        scan_data = {
            "name": "Test Code Scan",
            "target": "print('hello world')",
            "scan_type": "code",
            "language": "python"
        }

        with patch('services.tavo_service.tavo_service.scan_code') as mock_scan:
            mock_scan.return_value = mock_tavo_response

            response = client.post("/api/scans/", json=scan_data)

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test-scan-id"
            assert data["status"] == "completed"

    def test_create_scan_url(self, client, mock_tavo_response):
        scan_data = {
            "name": "Test URL Scan",
            "target": "https://example.com",
            "scan_type": "web"
        }

        with patch('services.tavo_service.tavo_service.scan_url') as mock_scan:
            mock_scan.return_value = mock_tavo_response

            response = client.post("/api/scans/", json=scan_data)

            assert response.status_code == 200
            data = response.json()
            assert data["scan_type"] == "code"  # Will be updated by mock

    def test_create_scan_invalid_type(self, client):
        scan_data = {
            "name": "Invalid Scan",
            "target": "test",
            "scan_type": "invalid"
        }

        response = client.post("/api/scans/", json=scan_data)

        assert response.status_code == 400
        assert "Invalid scan type" in response.json()["detail"]

    def test_get_scan(self, client, mock_tavo_response):
        with patch('services.tavo_service.tavo_service.get_scan_status') as mock_get:
            mock_get.return_value = mock_tavo_response

            response = client.get("/api/scans/test-scan-id")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test-scan-id"

    def test_health_check(self, client):
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "tavo-fastapi"
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

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  tavo-fastapi:
    build: .
    ports:
      - "8000:8000"
    environment:
      - TAVO_API_KEY=${TAVO_API_KEY}
      - TAVO_BASE_URL=https://api.tavoai.net
      - TAVO_TIMEOUT=30
    volumes:
      - .:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add Redis for caching/background tasks
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.2
pydantic==2.5.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

## Deployment

### Production Configuration

```python
# config.py (production updates)
import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    tavo_api_key: str = os.getenv("TAVO_API_KEY", "")
    tavo_base_url: str = os.getenv("TAVO_BASE_URL", "https://api.tavoai.net")
    tavo_timeout: int = int(os.getenv("TAVO_TIMEOUT", "30"))

    # Production settings
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    workers: int = int(os.getenv("WORKERS", "4"))
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # CORS settings
    allowed_origins: list = os.getenv("ALLOWED_ORIGINS", "https://yourdomain.com").split(",")
    allowed_hosts: list = os.getenv("ALLOWED_HOSTS", "yourdomain.com").split(",")

    class Config:
        env_file = ".env"

settings = Settings()
```

### Production Dockerfile

```dockerfile
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy source code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

This FastAPI integration provides a robust, async-first interface for Tavo AI security scanning with comprehensive error handling, background task processing, rate limiting, and production deployment configurations.
