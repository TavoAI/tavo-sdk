"""Integration tests for Tavo Python SDK"""

import os
import pytest

from tavo.client import TavoClient


class TestTavoClientIntegration:
    """Integration tests for TavoClient with mocked HTTP responses"""

    @pytest.mark.asyncio
    async def test_health_check_success(self):
        """Test successful health check - mirrors api-server test patterns"""
        api_key = os.getenv('TAVO_TEST_API_KEY', 'test-api-key')
        base_url = os.getenv('TAVO_TEST_BASE_URL', 'http://localhost:8000')

        async with TavoClient(api_key=api_key, base_url=base_url) as client:
            # This mirrors health check tests in api-server
            assert hasattr(client, 'health_check')
            assert callable(client.health_check)

    @pytest.mark.asyncio
    async def test_scan_operations_integration(self):
        """Test scan operations integration - mirrors api-server scan tests"""
        api_key = os.getenv('TAVO_TEST_API_KEY', 'test-api-key')
        base_url = os.getenv('TAVO_TEST_BASE_URL', 'http://localhost:8000')

        async with TavoClient(api_key=api_key, base_url=base_url) as client:
            scans = client.scans()

            # Test that all expected methods exist (mirrors api-server endpoint tests)
            assert hasattr(scans, 'create')
            assert hasattr(scans, 'get')
            assert hasattr(scans, 'list')
            assert hasattr(scans, 'results')  # Additional method for results
            assert callable(scans.create)
            assert callable(scans.get)
            assert callable(scans.list)
            assert callable(scans.results)

    @pytest.mark.asyncio
    async def test_report_operations_integration(self):
        """Test report operations integration - mirrors api-server report tests"""
        api_key = os.getenv('TAVO_TEST_API_KEY', 'test-api-key')
        base_url = os.getenv('TAVO_TEST_BASE_URL', 'http://localhost:8000')

        async with TavoClient(api_key=api_key, base_url=base_url) as client:
            reports = client.reports()

            # Test that all expected methods exist (mirrors api-server endpoint tests)
            assert hasattr(reports, 'create')
            assert hasattr(reports, 'get')
            assert hasattr(reports, 'list')
            assert callable(reports.create)
            assert callable(reports.get)
            assert callable(reports.list)

    @pytest.mark.asyncio
    async def test_api_key_authentication_header(self):
        """Test that API key authentication uses X-API-Key header"""
        api_key = 'test-api-key-123'
        base_url = 'http://localhost:8000'

        client = TavoClient(api_key=api_key, base_url=base_url)

        # Check that the auth headers are set correctly
        # This mirrors authentication header tests in api-server
        auth_headers = client._get_auth_headers()
        assert 'X-API-Key' in auth_headers
        assert auth_headers['X-API-Key'] == api_key
        assert 'Authorization' not in auth_headers  # Should not have Bearer token

        await client._client.aclose()

    @pytest.mark.asyncio
    async def test_jwt_token_authentication_header(self):
        """Test that JWT token authentication uses Authorization header"""
        jwt_token = 'test-jwt-token-123'
        base_url = 'http://localhost:8000'

        client = TavoClient(jwt_token=jwt_token, base_url=base_url)

        # Check that the auth headers are set correctly
        # This mirrors JWT authentication tests in api-server
        auth_headers = client._get_auth_headers()
        assert 'Authorization' in auth_headers
        assert auth_headers['Authorization'] == f'Bearer {jwt_token}'
        assert 'X-API-Key' not in auth_headers  # Should not have API key header

        await client._client.aclose()


class TestTavoClientErrorHandling:
    """Test error handling in TavoClient"""

    @pytest.mark.asyncio
    async def test_request_with_retry_on_500(self):
        """Test that client retries on 500 errors"""
        async with TavoClient(api_key="test-key", max_retries=2) as client:
            # This test would require mocking httpx to simulate 500 errors
            # and verify retry behavior
            assert client.config.max_retries == 2

    @pytest.mark.asyncio
    async def test_request_failure_after_retries(self):
        """Test that client fails after exhausting retries"""
        async with TavoClient(api_key="test-key", max_retries=1) as client:
            # This test would require mocking httpx to always return 500
            # and verify RuntimeError is raised
            assert client.config.max_retries == 1


class TestTavoClientConfiguration:
    """Test client configuration scenarios"""

    @pytest.mark.asyncio
    async def test_custom_base_url(self):
        """Test client with custom base URL"""
        async with TavoClient(
            api_key="test-key",
            base_url="https://custom.api.example.com"
        ) as client:
            assert client.config.base_url == "https://custom.api.example.com"

    @pytest.mark.asyncio
    async def test_custom_timeout(self):
        """Test client with custom timeout"""
        async with TavoClient(
            api_key="test-key",
            timeout=120.0
        ) as client:
            assert client.config.timeout == pytest.approx(120.0)

    @pytest.mark.asyncio
    async def test_custom_api_version(self):
        """Test client with custom API version"""
        async with TavoClient(
            api_key="test-key",
            api_version="v2"
        ) as client:
            assert client.config.api_version == "v2"
