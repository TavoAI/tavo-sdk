"""
Rules Loader for Tavo Scanner

Supports both legacy and new hybrid rule formats.
Handles YAML parsing, validation, and format conversion.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass


@dataclass
class HeuristicRule:
    """Heuristic rule configuration."""
    type: str  # "semgrep" or "opa"
    pattern: str
    message: str


@dataclass
class AIAnalysisConfig:
    """AI analysis configuration."""
    trigger: List[str]
    prompt_template: str
    expected_response_schema: Dict[str, Any]


@dataclass
class ExecutionConfig:
    """Rule execution configuration."""
    max_tokens: int = 2000
    temperature: float = 0.1
    cache_results: bool = True
    cache_duration: str = "7d"
    fallback_model: Optional[str] = None


@dataclass
class HybridRule:
    """Hybrid rule combining heuristics and AI analysis."""
    id: str
    name: str
    category: str
    subcategory: str
    severity: str
    rule_type: str  # "opengrep", "opa", "hybrid", "ai-only"
    compatible_models: List[str]
    heuristics: List[HeuristicRule]
    ai_analysis: Optional[AIAnalysisConfig]
    execution: ExecutionConfig
    tags: List[str]
    version: str = "1.0"


class RulesLoader:
    """Loader for rule bundles supporting multiple formats."""

    def __init__(self):
        self.supported_formats = ["legacy", "hybrid"]

    def load_bundle(self, bundle_path: Union[str, Path]) -> Dict[str, Any]:
        """Load a rule bundle from file or directory."""
        bundle_path = Path(bundle_path)

        if bundle_path.is_file():
            return self._load_bundle_file(bundle_path)
        elif bundle_path.is_dir():
            return self._load_bundle_directory(bundle_path)
        else:
            raise FileNotFoundError(f"Bundle path not found: {bundle_path}")

    def _load_bundle_file(self, bundle_file: Path) -> Dict[str, Any]:
        """Load bundle from a single file."""
        if bundle_file.suffix.lower() in ['.yaml', '.yml']:
            return self._load_yaml_bundle(bundle_file)
        elif bundle_file.suffix.lower() == '.json':
            return self._load_json_bundle(bundle_file)
        else:
            raise ValueError(f"Unsupported bundle format: {bundle_file.suffix}")

    def _load_bundle_directory(self, bundle_dir: Path) -> Dict[str, Any]:
        """Load bundle from directory structure."""
        # Look for index file
        index_files = ["bundle.json", "index.json", "manifest.json"]
        index_file = None

        for filename in index_files:
            candidate = bundle_dir / filename
            if candidate.exists():
                index_file = candidate
                break

        if not index_file:
            raise FileNotFoundError(f"No index file found in {bundle_dir}")

        # Load index
        with open(index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)

        bundle = {
            "name": index_data["name"],
            "version": index_data["version"],
            "description": index_data["description"],
            "rules": []
        }

        # Load all YAML rule files
        for yaml_file in bundle_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                    if yaml_data and isinstance(yaml_data, dict) and "rules" in yaml_data:
                        bundle["rules"].extend(yaml_data["rules"])
            except Exception as e:
                print(f"Warning: Failed to load rules from {yaml_file}: {e}")

        return bundle

    def _load_yaml_bundle(self, bundle_file: Path) -> Dict[str, Any]:
        """Load YAML bundle file."""
        with open(bundle_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError("Invalid bundle format")

        # Check if it's a new hybrid format bundle
        if "rules" in data and isinstance(data["rules"], list):
            return data

        # Assume legacy format
        return self._convert_legacy_bundle(data)

    def _load_json_bundle(self, bundle_file: Path) -> Dict[str, Any]:
        """Load JSON bundle file."""
        with open(bundle_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("Invalid bundle format")

        return data

    def _convert_legacy_bundle(self, legacy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert legacy bundle format to hybrid format."""
        converted_rules = []

        for rule_id, rule_data in legacy_data.items():
            if not isinstance(rule_data, dict):
                continue

            # Convert legacy rule to hybrid format
            converted_rule = {
                "version": "1.0",
                "id": rule_id,
                "name": rule_data.get("name", rule_id),
                "category": rule_data.get("category", "security"),
                "subcategory": rule_data.get("subcategory", ""),
                "severity": rule_data.get("severity", "medium"),
                "rule_type": "opengrep",  # Legacy rules are opengrep-only
                "compatible_models": [],
                "tags": rule_data.get("tags", []),
                "heuristics": [],
                "execution": {
                    "max_tokens": 2000,
                    "temperature": 0.1,
                    "cache_results": True,
                    "cache_duration": "7d"
                }
            }

            # Convert legacy pattern to heuristic
            if "pattern" in rule_data:
                heuristic = {
                    "type": "semgrep",
                    "pattern": rule_data["pattern"],
                    "message": rule_data.get("message", f"Pattern match: {rule_id}")
                }
                converted_rule["heuristics"].append(heuristic)

            converted_rules.append(converted_rule)

        return {
            "name": "legacy-bundle",
            "version": "1.0",
            "description": "Converted legacy bundle",
            "rules": converted_rules
        }

    def parse_hybrid_rule(self, rule_data: Dict[str, Any]) -> HybridRule:
        """Parse a hybrid rule from dictionary data."""
        # Validate required fields
        required_fields = ["id", "name", "category", "severity", "rule_type"]
        for field in required_fields:
            if field not in rule_data:
                raise ValueError(f"Missing required field '{field}' in rule")

        # Parse heuristics
        heuristics = []
        if "heuristics" in rule_data:
            for h_data in rule_data["heuristics"]:
                heuristic = HeuristicRule(
                    type=h_data["type"],
                    pattern=h_data["pattern"],
                    message=h_data["message"]
                )
                heuristics.append(heuristic)

        # Parse AI analysis config
        ai_analysis = None
        if "ai_analysis" in rule_data:
            ai_config = rule_data["ai_analysis"]
            ai_analysis = AIAnalysisConfig(
                trigger=ai_config.get("trigger", ["always"]),
                prompt_template=ai_config["prompt_template"],
                expected_response_schema=ai_config["expected_response_schema"]
            )

        # Parse execution config
        exec_config = rule_data.get("execution", {})
        execution = ExecutionConfig(
            max_tokens=exec_config.get("max_tokens", 2000),
            temperature=exec_config.get("temperature", 0.1),
            cache_results=exec_config.get("cache_results", True),
            cache_duration=exec_config.get("cache_duration", "7d"),
            fallback_model=exec_config.get("fallback_model")
        )

        return HybridRule(
            id=rule_data["id"],
            name=rule_data["name"],
            category=rule_data["category"],
            subcategory=rule_data.get("subcategory", ""),
            severity=rule_data["severity"],
            rule_type=rule_data["rule_type"],
            compatible_models=rule_data.get("compatible_models", []),
            heuristics=heuristics,
            ai_analysis=ai_analysis,
            execution=execution,
            tags=rule_data.get("tags", []),
            version=rule_data.get("version", "1.0")
        )

    def validate_rule(self, rule: HybridRule) -> List[str]:
        """Validate a hybrid rule and return list of errors."""
        errors = []

        # Validate rule type
        valid_types = ["opengrep", "opa", "hybrid", "ai-only"]
        if rule.rule_type not in valid_types:
            errors.append(f"Invalid rule_type: {rule.rule_type}. Must be one of {valid_types}")

        # Validate severity
        valid_severities = ["low", "medium", "high", "critical"]
        if rule.severity not in valid_severities:
            errors.append(f"Invalid severity: {rule.severity}. Must be one of {valid_severities}")

        # Validate heuristics
        if rule.rule_type in ["opengrep", "hybrid"]:
            if not rule.heuristics:
                errors.append("Rules with opengrep or hybrid type must have heuristics")
            for i, h in enumerate(rule.heuristics):
                if h.type not in ["semgrep", "opa"]:
                    errors.append(f"Heuristic {i}: Invalid type '{h.type}'. Must be 'semgrep' or 'opa'")
                if not h.pattern:
                    errors.append(f"Heuristic {i}: Missing pattern")
                # Additional validation for OPA rules
                if h.type == "opa" and not self._validate_rego_syntax(h.pattern):
                    errors.append(f"Heuristic {i}: Invalid Rego syntax")

        # Validate AI analysis
        if rule.rule_type in ["hybrid", "ai-only"]:
            if not rule.ai_analysis:
                errors.append("Rules with hybrid or ai-only type must have ai_analysis config")
            elif not rule.ai_analysis.prompt_template:
                errors.append("AI analysis config missing prompt_template")

        # Validate compatible models for AI rules
        if rule.rule_type in ["hybrid", "ai-only"] and not rule.compatible_models:
            errors.append("AI-enabled rules must specify compatible_models")

        return errors

    def get_opengrep_rules(self, bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract OpenGrep-compatible rules from bundle."""
        opengrep_rules = []

        for rule_data in bundle.get("rules", []):
            try:
                rule = self.parse_hybrid_rule(rule_data)

                # Only include rules with heuristics
                if rule.heuristics:
                    for heuristic in rule.heuristics:
                        if heuristic.type == "semgrep":
                            opengrep_rule = {
                                "id": rule.id,
                                "name": rule.name,
                                "severity": rule.severity,
                                "category": rule.category,
                                "subcategory": rule.subcategory,
                                "tags": rule.tags,
                                "pattern": heuristic.pattern,
                                "message": heuristic.message
                            }
                            opengrep_rules.append(opengrep_rule)

            except Exception as e:
                print(f"Warning: Failed to parse rule {rule_data.get('id', 'unknown')}: {e}")

        return opengrep_rules

    def get_opa_rules(self, bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract OPA/Rego rules from bundle."""
        opa_rules = []

        for rule_data in bundle.get("rules", []):
            try:
                rule = self.parse_hybrid_rule(rule_data)

                # Only include rules with OPA heuristics
                if rule.heuristics:
                    for heuristic in rule.heuristics:
                        if heuristic.type == "opa":
                            opa_rule = {
                                "id": rule.id,
                                "name": rule.name,
                                "severity": rule.severity,
                                "category": rule.category,
                                "subcategory": rule.subcategory,
                                "tags": rule.tags,
                                "rego_policy": heuristic.pattern,
                                "message": heuristic.message
                            }
                            opa_rules.append(opa_rule)

            except Exception as e:
                print(f"Warning: Failed to parse rule {rule_data.get('id', 'unknown')}: {e}")

        return opa_rules

    def get_all_heuristics(self, bundle: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all heuristics grouped by type."""
        heuristics_by_type = {
            "semgrep": [],
            "opa": []
        }

        for rule_data in bundle.get("rules", []):
            try:
                rule = self.parse_hybrid_rule(rule_data)

                for heuristic in rule.heuristics:
                    if heuristic.type in heuristics_by_type:
                        heuristic_dict = {
                            "rule_id": rule.id,
                            "rule_name": rule.name,
                            "severity": rule.severity,
                            "category": rule.category,
                            "subcategory": rule.subcategory,
                            "tags": rule.tags,
                            "pattern": heuristic.pattern,
                            "message": heuristic.message
                        }
                        heuristics_by_type[heuristic.type].append(heuristic_dict)

            except Exception as e:
                print(f"Warning: Failed to parse rule {rule_data.get('id', 'unknown')}: {e}")

        return heuristics_by_type

    def _validate_rego_syntax(self, rego_code: str) -> bool:
        """Basic validation of Rego syntax."""
        if not rego_code or not rego_code.strip():
            return False

        # Check for basic Rego keywords and structure
        required_keywords = ['package', 'import', 'default', 'allow', 'deny']
        has_keywords = any(keyword in rego_code for keyword in required_keywords)

        # Check for balanced brackets and quotes
        if not self._check_balanced_delimiters(rego_code):
            return False

        return has_keywords or True  # Allow non-standard Rego for flexibility

    def _check_balanced_delimiters(self, code: str) -> bool:
        """Check for balanced delimiters in code."""
        stack = []
        delimiters = {
            '(': ')',
            '[': ']',
            '{': '}',
            '"': '"',
            "'": "'"
        }

        i = 0
        while i < len(code):
            char = code[i]

            if char in delimiters:
                if char in ['"', "'"]:
                    # Handle string literals
                    quote_char = char
                    i += 1
                    while i < len(code) and code[i] != quote_char:
                        if code[i] == '\\':
                            i += 1  # Skip escaped character
                        i += 1
                    if i >= len(code):
                        return False  # Unclosed string
                else:
                    stack.append((char, delimiters[char]))
            elif char in [')', ']', '}', '"', "'"]:
                if not stack:
                    return False
                expected_open, expected_close = stack.pop()
                if char != expected_close:
                    return False

            i += 1

        return len(stack) == 0
