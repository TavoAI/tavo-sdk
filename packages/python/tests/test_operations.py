"""Unit tests for Tavo Python SDK operations"""

import pytest
from unittest.mock import AsyncMock, patch

from tavo.client import TavoClient


class TestScanOperations:
    """Test ScanOperations class"""

    def setup_method(self):
        """Set up test client"""
        self.client = TavoClient(api_key="test-key")

    @pytest.mark.asyncio
    async def test_create_scan(self):
        """Test creating a new scan"""
        expected_response = {
            "id": "scan-123",
            "status": "pending",
            "repository_url": "https://github.com/user/repo"
        }

        with patch.object(self.client, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response

            result = await self.client.scans().create(
                repository_url="https://github.com/user/repo",
                branch="main"
            )

            assert result == expected_response
            mock_request.assert_called_once_with(
                "POST",
                "/scans",
                data={
                    "repository_url": "https://github.com/user/repo",
                    "branch": "main"
                }
            )

    @pytest.mark.asyncio
    async def test_get_scan(self):
        """Test getting scan details"""
        scan_id = "scan-123"
        expected_response = {
            "id": scan_id,
            "status": "completed",
            "repository_url": "https://github.com/user/repo"
        }

        with patch.object(self.client, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response

            result = await self.client.scans().get(scan_id)

            assert result == expected_response
            mock_request.assert_called_once_with("GET", f"/scans/{scan_id}")

    @pytest.mark.asyncio
    async def test_list_scans(self):
        """Test listing scans"""
        expected_response = {
            "scans": [
                {"id": "scan-1", "status": "completed"},
                {"id": "scan-2", "status": "running"}
            ],
            "total": 2
        }

        with patch.object(self.client, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response

            result = await self.client.scans().list(limit=10, offset=0)

            assert result == expected_response
            mock_request.assert_called_once_with(
                "GET",
                "/scans",
                params={"limit": 10, "offset": 0}
            )

    @pytest.mark.asyncio
    async def test_list_scans_no_params(self):
        """Test listing scans without parameters"""
        expected_response = {"scans": [], "total": 0}

        with patch.object(self.client, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response

            result = await self.client.scans().list()

            assert result == expected_response
            mock_request.assert_called_once_with("GET", "/scans", params={})


class TestReportOperations:
    """Test ReportOperations class"""

    def setup_method(self):
        """Set up test client"""
        self.client = TavoClient(api_key="test-key")

    @pytest.mark.asyncio
    async def test_get_report(self):
        """Test getting report details"""
        report_id = "report-123"
        expected_response = {
            "id": report_id,
            "scan_id": "scan-123",
            "status": "completed",
            "findings": []
        }

        with patch.object(self.client, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response

            result = await self.client.reports().get(report_id)

            assert result == expected_response
            mock_request.assert_called_once_with("GET", f"/reports/{report_id}")

    @pytest.mark.asyncio
    async def test_list_reports(self):
        """Test listing reports"""
        expected_response = {
            "reports": [
                {"id": "report-1", "status": "completed"},
                {"id": "report-2", "status": "pending"}
            ],
            "total": 2
        }

        with patch.object(self.client, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response

            result = await self.client.reports().list(scan_id="scan-123", limit=5)

            assert result == expected_response
            mock_request.assert_called_once_with(
                "GET",
                "/reports",
                params={"scan_id": "scan-123", "limit": 5}
            )

    @pytest.mark.asyncio
    async def test_list_reports_no_params(self):
        """Test listing reports without parameters"""
        expected_response = {"reports": [], "total": 0}

        with patch.object(self.client, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = expected_response

            result = await self.client.reports().list()

            assert result == expected_response
            mock_request.assert_called_once_with("GET", "/reports", params={})
