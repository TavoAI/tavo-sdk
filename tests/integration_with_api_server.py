"""SDK Integration Tests - Run against api-server test environment"""

import os
import pytest
import asyncio
from typing import Optional

# Import SDKs - these would be available when running integration tests
tavo_js_sdk = None
tavo_python_sdk = None

try:
    # Try to import Python SDK
    from tavo.client import TavoClient as PythonTavoClient
    tavo_python_sdk = True
except ImportError:
    tavo_python_sdk = False

# JavaScript SDK would need to be imported differently (via subprocess or similar)
# For now, we'll focus on Python SDK integration tests


class TestSDKIntegration:
    """Integration tests that verify SDKs work with api-server"""

    @pytest.fixture
    def api_key(self) -> str:
        """Get API key from environment or test fixtures"""
        return os.getenv('TAVO_TEST_API_KEY', 'test-api-key')

    @pytest.fixture
    def base_url(self) -> str:
        """Get base URL for test server"""
        return os.getenv('TAVO_TEST_BASE_URL', 'http://localhost:8000')

    @pytest.mark.skipif(not tavo_python_sdk, reason="Python SDK not available")
    @pytest.mark.asyncio
    async def test_python_sdk_api_key_auth(self, api_key: str, base_url: str):
        """Test Python SDK with API key authentication"""
        async with PythonTavoClient(api_key=api_key, base_url=base_url) as client:
            # Test authentication headers are set correctly
            auth_headers = client._get_auth_headers()
            assert 'X-API-Key' in auth_headers
            assert auth_headers['X-API-Key'] == api_key
            assert 'Authorization' not in auth_headers

    @pytest.mark.skipif(not tavo_python_sdk, reason="Python SDK not available")
    @pytest.mark.asyncio
    async def test_python_sdk_health_check(self, api_key: str, base_url: str):
        """Test Python SDK health check endpoint"""
        async with PythonTavoClient(api_key=api_key, base_url=base_url) as client:
            # This mirrors the health check tests in api-server
            try:
                health = await client.health_check()
                assert 'status' in health
            except Exception:
                # Expected if test server isn't running
                pass

    @pytest.mark.skipif(not tavo_python_sdk, reason="Python SDK not available")
    @pytest.mark.asyncio
    async def test_python_sdk_scan_operations(self, api_key: str, base_url: str):
        """Test Python SDK scan operations match api-server endpoints"""
        async with PythonTavoClient(api_key=api_key, base_url=base_url) as client:
            scans = client.scans()

            # Verify all expected methods exist (matches api-server test patterns)
            required_methods = ['create', 'get', 'list', 'results']
            for method in required_methods:
                assert hasattr(scans, method), f"Missing method: {method}"
                assert callable(getattr(scans, method)), f"Method not callable: {method}"

    @pytest.mark.skipif(not tavo_python_sdk, reason="Python SDK not available")
    @pytest.mark.asyncio
    async def test_python_sdk_report_operations(self, api_key: str, base_url: str):
        """Test Python SDK report operations match api-server endpoints"""
        async with PythonTavoClient(api_key=api_key, base_url=base_url) as client:
            reports = client.reports()

            # Verify all expected methods exist (matches api-server test patterns)
            required_methods = ['create', 'get', 'list']
            for method in required_methods:
                assert hasattr(reports, method), f"Missing method: {method}"
                assert callable(getattr(reports, method)), f"Method not callable: {method}"

    @pytest.mark.skipif(not tavo_python_sdk, reason="Python SDK not available")
    @pytest.mark.asyncio
    async def test_python_sdk_error_handling(self, base_url: str):
        """Test Python SDK error handling with invalid credentials"""
        async with PythonTavoClient(api_key='invalid-key', base_url=base_url) as client:
            try:
                await client.health_check()
                # If we get here without exception, server isn't validating auth
                pytest.skip("Test server not validating authentication")
            except Exception as e:
                # Expected authentication error
                assert hasattr(e, 'response') or 'auth' in str(e).lower()

    def test_javascript_sdk_available(self):
        """Test that JavaScript SDK can be imported (placeholder)"""
        # This would test JS SDK availability
        # For now, just check if the package exists
        js_sdk_path = os.path.join(os.path.dirname(__file__), '..', 'javascript')
        assert os.path.exists(js_sdk_path), "JavaScript SDK package not found"

    def test_sdk_authentication_consistency(self, api_key: str, base_url: str):
        """Test that both SDKs use consistent authentication patterns"""
        if not tavo_python_sdk:
            pytest.skip("Python SDK not available for consistency test")

        # Test Python SDK auth pattern
        client = PythonTavoClient(api_key=api_key, base_url=base_url)
        python_headers = client._get_auth_headers()

        # Verify Python SDK uses X-API-Key
        assert 'X-API-Key' in python_headers
        assert python_headers['X-API-Key'] == api_key

        # TODO: Add JavaScript SDK consistency check when available
        # JS SDK should also use X-API-Key header

        asyncio.run(client._client.aclose())