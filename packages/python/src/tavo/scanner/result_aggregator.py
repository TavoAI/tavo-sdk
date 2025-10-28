"""Result aggregation for combining plugin outputs into SARIF format"""

from typing import List, Dict, Any
from datetime import datetime, timezone
import logging

from ..plugins import PluginExecutionResult

logger = logging.getLogger(__name__)


class ResultAggregator:
    """Aggregates results from multiple plugins into standard formats"""

    def __init__(self):
        """Initialize result aggregator"""
        self.tool_name = "TavoAI Scanner"
        self.tool_version = "1.0.0"

    def to_sarif(self, results: List[PluginExecutionResult]) -> Dict[str, Any]:
        """Convert plugin results to SARIF format

        Args:
            results: List of plugin execution results

        Returns:
            SARIF-formatted report
        """
        sarif_results = []
        tool_extensions = []

        for plugin_result in results:
            # Add plugin as tool extension
            tool_extensions.append(
                {
                    "name": plugin_result.plugin_name,
                    "version": plugin_result.plugin_version,
                    "properties": {
                        "success": plugin_result.success,
                        "executionTimeMs": plugin_result.execution_time_ms,
                        "tokensUsed": plugin_result.tokens_used,
                        "costUsd": plugin_result.cost_usd,
                    },
                }
            )

            # Convert findings to SARIF results
            for finding in plugin_result.findings:
                sarif_result = self._finding_to_sarif_result(
                    finding, plugin_result.plugin_id
                )
                sarif_results.append(sarif_result)

        # Build complete SARIF document
        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": self.tool_name,
                            "version": self.tool_version,
                            "informationUri": "https://tavoai.net",
                            "extensions": tool_extensions,
                        }
                    },
                    "results": sarif_results,
                    "invocations": [
                        {
                            "executionSuccessful": all(r.success for r in results),
                            "endTimeUtc": datetime.now(timezone.utc).isoformat(),
                        }
                    ],
                }
            ],
        }

        return sarif

    def _finding_to_sarif_result(
        self, finding: Dict[str, Any], plugin_id: str
    ) -> Dict[str, Any]:
        """Convert a finding to SARIF result format

        Args:
            finding: Finding dictionary from plugin
            plugin_id: Plugin that generated the finding

        Returns:
            SARIF result object
        """
        # Map severity to SARIF level
        severity_map = {
            "critical": "error",
            "high": "error",
            "error": "error",
            "medium": "warning",
            "warning": "warning",
            "low": "note",
            "info": "note",
            "note": "note",
        }

        level = severity_map.get(finding.get("severity", "warning").lower(), "warning")

        # Build locations
        locations = []
        if finding.get("path") or finding.get("file"):
            file_path = finding.get("path") or finding.get("file", "unknown")
            location = {
                "physicalLocation": {
                    "artifactLocation": {"uri": file_path},
                    "region": {
                        "startLine": finding.get("line", finding.get("start_line", 1)),
                    },
                }
            }

            # Add column if available
            if "column" in finding or "start_column" in finding:
                location["physicalLocation"]["region"]["startColumn"] = finding.get(
                    "column", finding.get("start_column", 1)
                )

            # Add end line/column if available
            if "end_line" in finding:
                location["physicalLocation"]["region"]["endLine"] = finding["end_line"]
            if "end_column" in finding:
                location["physicalLocation"]["region"]["endColumn"] = finding[
                    "end_column"
                ]

            locations.append(location)

        # Build SARIF result
        result = {
            "ruleId": finding.get("rule_id", finding.get("id", "unknown")),
            "level": level,
            "message": {
                "text": finding.get("message", finding.get("description", "No message"))
            },
            "locations": locations,
        }

        # Add plugin info as property
        result["properties"] = {
            "plugin": plugin_id,
            "attack_type": finding.get("attack_type"),
            "confidence": finding.get("confidence"),
            "remediation": finding.get("remediation"),
        }

        # Add fixes if available
        if "fix" in finding:
            result["fixes"] = [
                {
                    "description": {"text": "Suggested fix"},
                    "artifactChanges": [
                        {
                            "artifactLocation": {
                                "uri": finding.get(
                                    "path", finding.get("file", "unknown")
                                )
                            },
                            "replacements": [
                                {
                                    "deletedRegion": {
                                        "startLine": finding.get("line", 1),
                                    },
                                    "insertedContent": {"text": finding["fix"]},
                                }
                            ],
                        }
                    ],
                }
            ]

        return result

    def to_json(self, results: List[PluginExecutionResult]) -> Dict[str, Any]:
        """Convert plugin results to JSON format

        Args:
            results: List of plugin execution results

        Returns:
            JSON-formatted report
        """
        return {
            "tool": {"name": self.tool_name, "version": self.tool_version},
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": [
                {
                    "plugin_id": r.plugin_id,
                    "plugin_name": r.plugin_name,
                    "plugin_version": r.plugin_version,
                    "success": r.success,
                    "findings": r.findings,
                    "errors": r.errors,
                    "warnings": r.warnings,
                    "execution_time_ms": r.execution_time_ms,
                    "tokens_used": r.tokens_used,
                    "cost_usd": r.cost_usd,
                    "metadata": r.metadata,
                }
                for r in results
            ],
            "summary": {
                "total_plugins": len(results),
                "successful_plugins": sum(1 for r in results if r.success),
                "total_findings": sum(len(r.findings) for r in results),
                "total_execution_time_ms": sum(
                    r.execution_time_ms or 0 for r in results
                ),
                "total_tokens_used": sum(r.tokens_used or 0 for r in results),
                "total_cost_usd": sum(r.cost_usd or 0 for r in results),
            },
        }

    def to_text(self, results: List[PluginExecutionResult]) -> str:
        """Convert plugin results to text format

        Args:
            results: List of plugin execution results

        Returns:
            Text-formatted report
        """
        lines = []
        lines.append(f"{self.tool_name} v{self.tool_version}")
        lines.append("=" * 60)
        lines.append("")

        for result in results:
            lines.append(f"Plugin: {result.plugin_name} v{result.plugin_version}")
            lines.append(f"Status: {'✓ Success' if result.success else '✗ Failed'}")

            if result.execution_time_ms:
                lines.append(f"Execution time: {result.execution_time_ms}ms")

            if result.errors:
                lines.append("Errors:")
                for error in result.errors:
                    lines.append(f"  - {error}")

            if result.warnings:
                lines.append("Warnings:")
                for warning in result.warnings:
                    lines.append(f"  - {warning}")

            if result.findings:
                lines.append(f"Findings ({len(result.findings)}):")
                for finding in result.findings:
                    severity = finding.get("severity", "unknown").upper()
                    message = finding.get("message", "No message")
                    file_path = finding.get("path", finding.get("file", "unknown"))
                    line_num = finding.get("line", finding.get("start_line", "?"))

                    lines.append(f"  [{severity}] {file_path}:{line_num}")
                    lines.append(f"    {message}")

            lines.append("")
            lines.append("-" * 60)
            lines.append("")

        # Add summary
        total_findings = sum(len(r.findings) for r in results)
        total_time = sum(r.execution_time_ms or 0 for r in results)

        lines.append("Summary:")
        lines.append(f"  Total plugins: {len(results)}")
        lines.append(f"  Successful: {sum(1 for r in results if r.success)}")
        lines.append(f"  Total findings: {total_findings}")
        lines.append(f"  Total execution time: {total_time}ms")

        if any(r.tokens_used for r in results):
            total_tokens = sum(r.tokens_used or 0 for r in results)
            total_cost = sum(r.cost_usd or 0 for r in results)
            lines.append(f"  Total tokens used: {total_tokens}")
            lines.append(f"  Total cost: ${total_cost:.4f}")

        return "\n".join(lines)
