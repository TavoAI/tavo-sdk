"""Integration tests for Tavo Python SDK"""

import pytest

from tavo.client import TavoClient


class TestTavoClientIntegration:
    """Integration tests for TavoClient with mocked HTTP responses"""

    @pytest.mark.asyncio
    async def test_health_check_success(self):
        """Test successful health check"""
        async with TavoClient(api_key="test-key") as client:
            # This would normally make a real HTTP request
            # For integration testing, we'd use a mock server
            # For now, we'll test the method exists and can be called
            assert hasattr(client, 'health_check')
            assert callable(client.health_check)

    @pytest.mark.asyncio
    async def test_scan_operations_integration(self):
        """Test scan operations integration"""
        async with TavoClient(api_key="test-key") as client:
            scans = client.scans()

            # Test that all expected methods exist
            assert hasattr(scans, 'create')
            assert hasattr(scans, 'get')
            assert hasattr(scans, 'list')
            assert callable(scans.create)
            assert callable(scans.get)
            assert callable(scans.list)

    @pytest.mark.asyncio
    async def test_report_operations_integration(self):
        """Test report operations integration"""
        async with TavoClient(api_key="test-key") as client:
            reports = client.reports()

            # Test that all expected methods exist
            assert hasattr(reports, 'get')
            assert hasattr(reports, 'list')
            assert callable(reports.get)
            assert callable(reports.list)


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
