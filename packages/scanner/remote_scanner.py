"""
Remote Scanner for Tavo Scanner

Handles remote scan requests and management through the API server.
"""

from typing import Dict, List, Any, Optional
import asyncio


class RemoteScanner:
    """Handles remote scanning operations via API server."""

    def __init__(self, sdk_integration, usage_tracker=None):
        """Initialize remote scanner.

        Args:
            sdk_integration: SDK integration instance
            usage_tracker: Usage tracker for cost monitoring
        """
        self.sdk_integration = sdk_integration
        self.usage_tracker = usage_tracker

    async def request_scan(
        self,
        target: str,
        scan_type: str = "security",
        **kwargs
    ) -> Dict[str, Any]:
        """Request a remote scan.

        Args:
            target: Target to scan (file path, directory, or repository URL)
            scan_type: Type of scan to perform
            **kwargs: Additional scan options

        Returns:
            Scan request result with job ID
        """
        # Determine target type
        if target.startswith(('http://', 'https://', 'git@', 'ssh://')):
            # Repository URL
            scan_request = {
                'repository_url': target,
                'scan_type': scan_type,
                **kwargs
            }
        else:
            # Local path - would need to be submitted first
            raise ValueError("Local file/directory scanning requires submission first. Use 'tavo submit' command.")

        # Create scan request
        result = await self.sdk_integration.create_scan(**scan_request)

        # Track usage if available
        if self.usage_tracker and 'cost' in result:
            self.usage_tracker.record_usage(
                operation='remote_scan_request',
                tokens_used=result.get('tokens_used', 0),
                cost_usd=result.get('cost', 0.0),
                scan_id=result.get('id')
            )

        return result

    async def get_scan_status(self, scan_id: str) -> Dict[str, Any]:
        """Get status of remote scan.

        Args:
            scan_id: Scan identifier

        Returns:
            Scan status information
        """
        return await self.sdk_integration.get_scan_results(scan_id)

    async def wait_for_scan_completion(
        self,
        scan_id: str,
        timeout_seconds: int = 300,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """Wait for scan to complete.

        Args:
            scan_id: Scan identifier
            timeout_seconds: Maximum time to wait
            poll_interval: Polling interval in seconds

        Returns:
            Final scan results
        """
        start_time = asyncio.get_event_loop().time()

        while True:
            try:
                results = await self.sdk_integration.get_scan_results(scan_id)

                # Check if scan is complete
                status = results.get('status', '').lower()
                if status in ['completed', 'failed', 'error', 'cancelled']:
                    return results

                # Check timeout
                elapsed = asyncio.get_event_loop().time() - start_time
                if elapsed > timeout_seconds:
                    raise TimeoutError(f"Scan {scan_id} timed out after {timeout_seconds} seconds")

                # Wait before next poll
                await asyncio.sleep(poll_interval)

            except Exception as e:
                # If we can't get status, assume scan failed
                return {
                    'id': scan_id,
                    'status': 'error',
                    'error': str(e)
                }

    async def list_scans(self, **kwargs) -> List[Dict[str, Any]]:
        """List remote scans.

        Returns:
            List of scan information
        """
        # This would need a list scans endpoint
        # For now, return empty list
        return []

    async def cancel_scan(self, scan_id: str) -> bool:
        """Cancel a running scan.

        Args:
            scan_id: Scan identifier

        Returns:
            True if cancelled successfully
        """
        try:
            await self.sdk_integration.cancel_job(scan_id)
            return True
        except Exception:
            return False

    async def get_scan_results(self, scan_id: str) -> Dict[str, Any]:
        """Get complete scan results.

        Args:
            scan_id: Scan identifier

        Returns:
            Scan results with findings
        """
        return await self.sdk_integration.get_scan_results(scan_id)

    async def export_scan_results(
        self,
        scan_id: str,
        format: str = "json",
        **kwargs
    ) -> Dict[str, Any]:
        """Export scan results.

        Args:
            scan_id: Scan identifier
            format: Export format (json, sarif, csv, pdf)
            **kwargs: Additional export options

        Returns:
            Export result with download URL
        """
        return await self.sdk_integration.export_results(
            scan_id=scan_id,
            format=format,
            **kwargs
        )

    def check_budget_before_scan(self) -> Dict[str, Any]:
        """Check budget status before starting expensive operations.

        Returns:
            Budget status information
        """
        if not self.usage_tracker:
            return {'status': 'ok', 'warnings': []}

        return self.usage_tracker.check_budget_status()

    def should_block_scan(self) -> bool:
        """Check if scan should be blocked due to budget limits.

        Returns:
            True if scan should be blocked
        """
        if not self.usage_tracker:
            return False

        return self.usage_tracker.should_block_ai_analysis()


