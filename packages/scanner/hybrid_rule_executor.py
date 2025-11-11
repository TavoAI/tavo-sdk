"""
Hybrid Rule Executor for Tavo Scanner

Executes hybrid rules combining local heuristics with remote AI analysis.
Handles conditional AI triggering and result merging.
"""

import time
import asyncio
import subprocess
import tempfile
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from .rules_loader import HybridRule, RulesLoader
from .sdk_integration import SDKIntegration, SDKError

# Optional OPA client integration
try:
    from opa_client import create_opa_client
    OPA_CLIENT_AVAILABLE = True
except ImportError:
    OPA_CLIENT_AVAILABLE = False


@dataclass
class HeuristicResult:
    """Result from heuristic execution."""
    findings: List[Dict[str, Any]]
    execution_time_ms: int


@dataclass
class AIAnalysisResult:
    """Result from AI analysis."""
    severity: str
    vulnerable_lines: List[int]
    description: str
    remediation: str
    owasp_mapping: List[str]
    confidence: float
    tokens_used: int
    cost_usd: float


@dataclass
class HybridExecutionResult:
    """Combined result from hybrid rule execution."""
    heuristics: Optional[HeuristicResult]
    ai_analysis: Optional[AIAnalysisResult]
    execution_time_ms: int
    total_cost_usd: float


class HybridRuleExecutor:
    """Executor for hybrid rules combining heuristics and AI analysis."""

    def __init__(self, sdk_integration: Optional[SDKIntegration] = None):
        """Initialize hybrid rule executor.

        Args:
            sdk_integration: SDK integration for remote operations
        """
        self.sdk_integration = sdk_integration
        self.rules_loader = RulesLoader()

    def should_run_ai_analysis(
        self,
        rule: HybridRule,
        heuristic_result: HeuristicResult,
        code_context: Dict[str, Any]
    ) -> bool:
        """Determine if AI analysis should be triggered."""
        if not rule.ai_analysis:
            return False

        triggers = rule.ai_analysis.trigger

        # Always run if specified
        if "always" in triggers:
            return True

        # Run if heuristics found issues
        if "heuristics_matched" in triggers and heuristic_result.findings:
            return True

        # Run for high-risk files
        if "high_risk_files" in triggers:
            # Check file extension, path patterns, etc.
            file_path = Path(code_context.get("file_path", ""))
            high_risk_extensions = [".py", ".js", ".ts", ".java", ".cpp", ".c", ".php"]
            high_risk_paths = ["config", "auth", "security", "admin"]

            if file_path.suffix.lower() in high_risk_extensions:
                return True

            if any(pattern in str(file_path).lower() for pattern in high_risk_paths):
                return True

        return False

    async def execute_hybrid_rule(
        self,
        rule: HybridRule,
        code_context: Dict[str, Any]
    ) -> HybridExecutionResult:
        """Execute a hybrid rule through multi-phase pipeline."""
        start_time = time.time()

        # Phase 1: Execute heuristics (local, fast)
        heuristic_result = await self._execute_heuristics(rule, code_context)

        # Phase 2: Check AI trigger conditions
        should_run_ai = self.should_run_ai_analysis(rule, heuristic_result, code_context)

        ai_result = None
        if should_run_ai and self.sdk_integration:
            # Phase 3: Execute AI analysis (remote, slower)
            try:
                ai_result = await self._execute_ai_analysis(rule, code_context, heuristic_result)
            except Exception as e:
                print(f"Warning: AI analysis failed for rule {rule.id}: {e}")

        # Calculate execution time
        execution_time = int((time.time() - start_time) * 1000)
        total_cost = ai_result.cost_usd if ai_result else 0.0

        return HybridExecutionResult(
            heuristics=heuristic_result,
            ai_analysis=ai_result,
            execution_time_ms=execution_time,
            total_cost_usd=total_cost
        )

    async def _execute_heuristics(
        self,
        rule: HybridRule,
        code_context: Dict[str, Any]
    ) -> HeuristicResult:
        """Execute heuristic phase locally."""
        start_time = time.time()

        findings = []

        for heuristic in rule.heuristics:
            try:
                if heuristic.type == "semgrep":
                    # Execute semgrep pattern matching
                    heuristic_findings = await self._execute_semgrep_heuristic(heuristic, code_context)
                    findings.extend(heuristic_findings)

                elif heuristic.type == "opa":
                    # Execute OPA/Rego policy evaluation
                    heuristic_findings = await self._execute_opa_heuristic(heuristic, code_context)
                    findings.extend(heuristic_findings)

            except Exception as e:
                # Log error but continue with other heuristics
                print(f"Warning: Failed to execute heuristic {heuristic.type} for rule {rule.id}: {e}")

        execution_time = int((time.time() - start_time) * 1000)

        return HeuristicResult(
            findings=findings,
            execution_time_ms=execution_time
        )

    async def _execute_semgrep_heuristic(
        self,
        heuristic,
        code_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Execute semgrep pattern matching."""
        findings = []
        code = code_context.get("code_snippet", "")
        file_path = code_context.get("file_path", "")

        # Simple pattern matching for now
        # In production, this would integrate with semgrep engine
        if heuristic.pattern in code:
            # Find line numbers where pattern occurs
            lines = code.split('\n')
            for line_num, line in enumerate(lines, 1):
                if heuristic.pattern in line:
                    finding = {
                        "rule_id": "",  # Will be set by caller
                        "message": heuristic.message,
                        "path": file_path,
                        "start_line": line_num,
                        "end_line": line_num,
                        "severity": "medium",  # Will be overridden
                        "category": "security",  # Will be overridden
                        "metadata": {
                            "pattern": heuristic.pattern,
                            "matched_line": line.strip(),
                            "engine": "semgrep"
                        }
                    }
                    findings.append(finding)

        return findings

    async def _execute_opa_heuristic(
        self,
        heuristic,
        code_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Execute OPA/Rego policy evaluation."""
        findings = []
        code = code_context.get("code_snippet", "")
        file_path = code_context.get("file_path", "")

        try:
            # Create temporary files for OPA execution
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rego', delete=False) as rego_file:
                rego_file.write(heuristic.pattern)
                rego_path = rego_file.name

            # Create input data for OPA
            opa_input = {
                "code": code,
                "file_path": file_path,
                "language": code_context.get("language", "unknown"),
                "metadata": code_context.get("metadata", {})
            }

            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as input_file:
                json.dump(opa_input, input_file)
                input_path = input_file.name

            # Execute OPA evaluation
            result = await self._run_opa_evaluation(rego_path, input_path)

            # Clean up temp files
            Path(rego_path).unlink(missing_ok=True)
            Path(input_path).unlink(missing_ok=True)

            # Process OPA results
            if result and "violations" in result:
                for violation in result["violations"]:
                    finding = {
                        "rule_id": "",  # Will be set by caller
                        "message": violation.get("message", heuristic.message),
                        "path": file_path,
                        "start_line": violation.get("line", 1),
                        "end_line": violation.get("line", 1),
                        "severity": violation.get("severity", "medium"),
                        "category": "policy",
                        "metadata": {
                            "opa_violation": violation,
                            "engine": "opa",
                            "rego_rule": heuristic.pattern[:100] + "..." if len(heuristic.pattern) > 100 else heuristic.pattern
                        }
                    }
                    findings.append(finding)

        except Exception as e:
            print(f"Warning: OPA evaluation failed: {e}")

        return findings

    async def _run_opa_evaluation(self, rego_path: str, input_path: str) -> Optional[Dict[str, Any]]:
        """Run OPA evaluation using available method (client or subprocess)."""

        # Try OPA Python client first if available
        if OPA_CLIENT_AVAILABLE:
            try:
                result = await self._run_opa_client_evaluation(rego_path, input_path)
                if result is not None:
                    return result
            except Exception as e:
                # Fall back to subprocess if client fails
                pass

        # Fall back to subprocess approach
        return await self._run_opa_subprocess_evaluation(rego_path, input_path)

    async def _run_opa_client_evaluation(self, rego_path: str, input_path: str) -> Optional[Dict[str, Any]]:
        """Run OPA evaluation using opa-python-client."""
        try:
            # Load the Rego policy and input data
            with open(rego_path, 'r') as f:
                rego_content = f.read()

            with open(input_path, 'r') as f:
                input_data = json.load(f)

            # Create async OPA client
            client = create_opa_client(async_mode=True, host='localhost', port=8181)

            # Check if server is available
            connected = await client.check_connection()
            if not connected:
                await client.close_connection()
                return None

            # Upload the policy
            policy_name = "scanner_policy"
            await client.update_policy_from_string(rego_content, policy_name)

            # Evaluate using the input data
            # For now, use ad-hoc query since we want to evaluate against input
            result = await client.ad_hoc_query(query="data", input_data=input_data)

            await client.close_connection()
            return result

        except Exception as e:
            # If client approach fails, return None to fall back to subprocess
            return None

    async def _run_opa_subprocess_evaluation(self, rego_path: str, input_path: str) -> Optional[Dict[str, Any]]:
        """Run OPA evaluation using subprocess (fallback method)."""
        try:
            # Execute OPA eval command
            cmd = [
                "opa", "eval",
                "--data", rego_path,
                "--input", input_path,
                "--format", "json",
                "data"
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                return json.loads(stdout.decode())
            else:
                print(f"Warning: OPA evaluation failed: {stderr.decode()}")
                return None

        except FileNotFoundError:
            print("Warning: OPA (opa) command not found. Please install Open Policy Agent.")
            return None
        except Exception as e:
            print(f"Warning: Failed to run OPA evaluation: {e}")
            return None

    async def _execute_ai_analysis(
        self,
        rule: HybridRule,
        code_context: Dict[str, Any],
        heuristic_result: HeuristicResult
    ) -> AIAnalysisResult:
        """Execute AI analysis phase remotely."""
        if not rule.ai_analysis or not self.sdk_integration:
            raise ValueError("AI analysis not available")

        # Render prompt template
        prompt = self._render_prompt_template(
            rule.ai_analysis.prompt_template,
            code_context,
            heuristic_result
        )

        # Select best compatible model
        model = self._select_best_model(rule.compatible_models)

        # Execute AI analysis
        ai_response = await self.sdk_integration.submit_ai_analysis(
            code_snippet=code_context.get("code_snippet", ""),
            model=model,
            prompt=prompt,
            max_tokens=rule.execution.max_tokens,
            temperature=rule.execution.temperature
        )

        # Parse and validate response
        return self._parse_ai_response(ai_response, rule)

    def _render_prompt_template(
        self,
        template: str,
        code_context: Dict[str, Any],
        heuristic_result: HeuristicResult
    ) -> str:
        """Render AI prompt template with context variables."""
        variables = {
            "language": code_context.get("language", "unknown"),
            "code_snippet": code_context.get("code_snippet", ""),
            "file_path": code_context.get("file_path", ""),
            "line_number": str(code_context.get("line_number", 1)),
            "heuristic_findings": str(len(heuristic_result.findings))
        }

        # Simple template rendering (could be enhanced)
        prompt = template
        for key, value in variables.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))

        return prompt

    def _select_best_model(self, compatible_models: List[str]) -> str:
        """Select the best available model from compatible models."""
        if not compatible_models:
            return "openai/gpt-3.5-turbo"  # Default fallback

        # Priority: cost-effective models first, then capability
        priority_order = [
            "openai/gpt-3.5-turbo",      # Cheapest
            "anthropic/claude-3-haiku",  # Fast and cheap
            "google/gemini-pro",         # Good balance
            "openai/gpt-4",             # Most capable
            "anthropic/claude-3-opus",   # Most capable but expensive
        ]

        for model in priority_order:
            if model in compatible_models:
                return model

        # Return first compatible model if none in priority list
        return compatible_models[0]

    def _parse_ai_response(
        self,
        ai_response: Dict[str, Any],
        rule: HybridRule
    ) -> AIAnalysisResult:
        """Parse and validate AI analysis response."""
        # Extract response content
        content = ai_response.get("content", "")
        metadata = ai_response.get("metadata", {})

        # For now, return a basic structure
        # In practice, this would parse the AI response according to
        # the expected_response_schema and validate it
        return AIAnalysisResult(
            severity="medium",  # Placeholder
            vulnerable_lines=[1],  # Placeholder
            description=f"AI analysis result for rule {rule.id}",
            remediation="Review and fix the identified issue",
            owasp_mapping=["LLM01"],  # Placeholder
            confidence=0.8,
            tokens_used=metadata.get("tokens_used", 150),
            cost_usd=metadata.get("cost_usd", 0.002)
        )

    async def execute_bundle_rules(
        self,
        bundle: Dict[str, Any],
        code_context: Dict[str, Any]
    ) -> List[HybridExecutionResult]:
        """Execute all rules in a bundle against code context."""
        results = []

        for rule_data in bundle.get("rules", []):
            try:
                rule = self.rules_loader.parse_hybrid_rule(rule_data)
                result = await self.execute_hybrid_rule(rule, code_context)
                results.append(result)
            except Exception as e:
                print(f"Warning: Failed to execute rule {rule_data.get('id', 'unknown')}: {e}")

        return results

    def get_execution_stats(self, results: List[HybridExecutionResult]) -> Dict[str, Any]:
        """Calculate execution statistics."""
        total_time = sum(r.execution_time_ms for r in results)
        total_cost = sum(r.total_cost_usd for r in results)

        heuristic_executions = sum(1 for r in r.heuristics is not None)
        ai_executions = sum(1 for r in r.ai_analysis is not None)

        total_findings = sum(
            len(r.heuristics.findings) if r.heuristics else 0
            for r in results
        )

        return {
            "total_rules": len(results),
            "heuristic_executions": heuristic_executions,
            "ai_executions": ai_executions,
            "total_findings": total_findings,
            "total_execution_time_ms": total_time,
            "total_cost_usd": total_cost,
            "average_cost_per_rule": total_cost / len(results) if results else 0
        }
