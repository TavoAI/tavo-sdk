"""Unit tests for Tavo Python SDK"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tavo.client import TavoClient, TavoConfig


class TestTavoConfig:
    """Test TavoConfig class"""

    def test_valid_config(self):
        """Test creating a valid config"""
        config = TavoConfig(
            api_key="test-key",
            base_url="https://api.example.com",
            api_version="v1",
            timeout=30.0,
            max_retries=3
        )
        assert config.api_key == "test-key"
        assert config.base_url == "https://api.example.com"
        assert config.api_version == "v1"
        assert config.timeout == pytest.approx(30.0)
        assert config.max_retries == 3

    def test_config_defaults(self):
        """Test config with default values"""
        config = TavoConfig(api_key="test-key")
        assert config.api_key == "test-key"
        assert config.base_url == "https://api.tavoai.net"
        assert config.api_version == "v1"
        assert config.timeout == pytest.approx(30.0)
        assert config.max_retries == 3

    def test_config_validation(self):
        """Test config validation - api_key is required"""
        # This should work fine
        config = TavoConfig(api_key="valid-key")
        assert config.api_key == "valid-key"


class TestTavoClient:
    """Test TavoClient class"""

    def test_init_with_api_key(self):
        """Test client initialization with direct API key"""
        client = TavoClient(api_key="test-key")
        assert client.config.api_key == "test-key"
        assert client.config.base_url == "https://api.tavoai.net"

    def test_init_with_env_var(self):
        """Test client initialization with environment variable"""
        with patch.dict(os.environ, {"TAVO_API_KEY": "env-key"}):
            client = TavoClient()
            assert client.config.api_key == "env-key"

    def test_init_no_api_key(self):
        """Test client initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Either API key or JWT token must be provided"):
                TavoClient()

    def test_init_custom_config(self):
        """Test client initialization with custom config"""
        client = TavoClient(
            api_key="test-key",
            base_url="https://custom.api.com",
            api_version="v2",
            timeout=60.0,
            max_retries=5
        )
        assert client.config.api_key == "test-key"
        assert client.config.base_url == "https://custom.api.com"
        assert client.config.api_version == "v2"
        assert client.config.timeout == pytest.approx(60.0)
        assert client.config.max_retries == 5

    @patch('tavo.client.httpx.AsyncClient')
    def test_client_initialization(self, mock_async_client):
        """Test that httpx client is properly initialized"""
        mock_client_instance = MagicMock()
        mock_async_client.return_value = mock_client_instance

        TavoClient(api_key="test-key")  # Create client for testing

        mock_async_client.assert_called_once()
        call_args = mock_async_client.call_args
        assert call_args[1]['base_url'] == "https://api.tavoai.net/api/v1"
        assert call_args[1]['headers']['Authorization'] == "Bearer test-key"
        assert call_args[1]['headers']['Content-Type'] == "application/json"
        assert call_args[1]['headers']['User-Agent'] == "tavo-python-sdk/0.1.0"
        assert call_args[1]['timeout'] == pytest.approx(30.0)

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager"""
        with patch('tavo.client.httpx.AsyncClient') as mock_async_client:
            mock_client_instance = AsyncMock()
            mock_async_client.return_value = mock_client_instance

            async with TavoClient(api_key="test-key"):
                pass  # Just test that context manager works

            mock_client_instance.aclose.assert_called_once()

    def test_scans_operations(self):
        """Test scans operations access"""
        client = TavoClient(api_key="test-key")
        scans = client.scans()
        assert scans is not None
        assert hasattr(scans, '_client')

    def test_reports_operations(self):
        """Test reports operations access"""
        client = TavoClient(api_key="test-key")
        reports = client.reports()
        assert reports is not None
        assert hasattr(reports, '_client')
