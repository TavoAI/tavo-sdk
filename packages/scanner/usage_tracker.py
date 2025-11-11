"""
Usage Tracker for Tavo Scanner

Tracks token usage, costs, and provides budget warnings for AI analysis.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class UsageRecord:
    """Individual usage record."""
    timestamp: float
    operation: str
    tokens_used: int
    cost_usd: float
    model: Optional[str] = None
    bundle_id: Optional[str] = None
    scan_id: Optional[str] = None


@dataclass
class BudgetLimits:
    """Budget limits and thresholds."""
    monthly_limit_tokens: int = 100000  # 100K tokens default
    warning_threshold_pct: int = 80      # Warn at 80%
    critical_threshold_pct: int = 90     # Critical at 90%
    block_threshold_pct: int = 95        # Block at 95%

    @property
    def warning_limit(self) -> int:
        return int(self.monthly_limit_tokens * self.warning_threshold_pct / 100)

    @property
    def critical_limit(self) -> int:
        return int(self.monthly_limit_tokens * self.critical_threshold_pct / 100)

    @property
    def block_limit(self) -> int:
        return int(self.monthly_limit_tokens * self.block_threshold_pct / 100)


class UsageTracker:
    """Tracks AI usage and provides budget monitoring."""

    def __init__(self, config_dir: Optional[Path] = None, budget_limits: Optional[BudgetLimits] = None):
        """Initialize usage tracker.

        Args:
            config_dir: Directory to store usage data
            budget_limits: Budget limits and thresholds
        """
        self.config_dir = config_dir or Path.home() / ".tavoai"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.usage_file = self.config_dir / "usage.json"
        self.budget_file = self.config_dir / "budget.json"

        self.budget_limits = budget_limits or BudgetLimits()
        self._load_budget_limits()
        self._load_usage_history()

    def _load_budget_limits(self) -> None:
        """Load budget limits from file."""
        if not self.budget_file.exists():
            self._save_budget_limits()
            return

        try:
            with open(self.budget_file, 'r') as f:
                data = json.load(f)
                self.budget_limits = BudgetLimits(
                    monthly_limit_tokens=data.get('monthly_limit_tokens', 100000),
                    warning_threshold_pct=data.get('warning_threshold_pct', 80),
                    critical_threshold_pct=data.get('critical_threshold_pct', 90),
                    block_threshold_pct=data.get('block_threshold_pct', 95)
                )
        except (json.JSONDecodeError, IOError):
            # Use defaults if file corrupted
            pass

    def _save_budget_limits(self) -> None:
        """Save budget limits to file."""
        data = {
            'monthly_limit_tokens': self.budget_limits.monthly_limit_tokens,
            'warning_threshold_pct': self.budget_limits.warning_threshold_pct,
            'critical_threshold_pct': self.budget_limits.critical_threshold_pct,
            'block_threshold_pct': self.budget_limits.block_threshold_pct
        }

        with open(self.budget_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_usage_history(self) -> None:
        """Load usage history from file."""
        if not self.usage_file.exists():
            self.usage_history = []
            return

        try:
            with open(self.usage_file, 'r') as f:
                data = json.load(f)
                self.usage_history = [
                    UsageRecord(**record) for record in data.get('records', [])
                ]
        except (json.JSONDecodeError, IOError, TypeError):
            self.usage_history = []

    def _save_usage_history(self) -> None:
        """Save usage history to file."""
        data = {
            'records': [
                {
                    'timestamp': record.timestamp,
                    'operation': record.operation,
                    'tokens_used': record.tokens_used,
                    'cost_usd': record.cost_usd,
                    'model': record.model,
                    'bundle_id': record.bundle_id,
                    'scan_id': record.scan_id
                }
                for record in self.usage_history
            ]
        }

        with open(self.usage_file, 'w') as f:
            json.dump(data, f, indent=2)

    def set_budget_limits(self, limits: BudgetLimits) -> None:
        """Set budget limits."""
        self.budget_limits = limits
        self._save_budget_limits()

    def get_budget_limits(self) -> BudgetLimits:
        """Get current budget limits."""
        return self.budget_limits

    def record_usage(
        self,
        operation: str,
        tokens_used: int,
        cost_usd: float,
        model: Optional[str] = None,
        bundle_id: Optional[str] = None,
        scan_id: Optional[str] = None
    ) -> None:
        """Record AI usage.

        Args:
            operation: Type of operation (e.g., "ai_analysis", "hybrid_scan")
            tokens_used: Number of tokens consumed
            cost_usd: Cost in USD
            model: AI model used
            bundle_id: Bundle identifier
            scan_id: Scan identifier
        """
        record = UsageRecord(
            timestamp=time.time(),
            operation=operation,
            tokens_used=tokens_used,
            cost_usd=cost_usd,
            model=model,
            bundle_id=bundle_id,
            scan_id=scan_id
        )

        self.usage_history.append(record)
        self._save_usage_history()

        # Clean up old records (older than 90 days)
        self._cleanup_old_records()

    def _cleanup_old_records(self) -> None:
        """Remove usage records older than 90 days."""
        cutoff_time = time.time() - (90 * 24 * 60 * 60)
        self.usage_history = [
            record for record in self.usage_history
            if record.timestamp > cutoff_time
        ]

    def get_current_month_usage(self) -> Dict[str, Any]:
        """Get usage statistics for current month."""
        now = time.time()
        month_start = now - (30 * 24 * 60 * 60)  # 30 days ago

        monthly_records = [
            record for record in self.usage_history
            if record.timestamp > month_start
        ]

        total_tokens = sum(record.tokens_used for record in monthly_records)
        total_cost = sum(record.cost_usd for record in monthly_records)

        return {
            'total_tokens': total_tokens,
            'total_cost_usd': total_cost,
            'remaining_tokens': max(0, self.budget_limits.monthly_limit_tokens - total_tokens),
            'usage_percent': (total_tokens / self.budget_limits.monthly_limit_tokens) * 100 if self.budget_limits.monthly_limit_tokens > 0 else 0,
            'record_count': len(monthly_records)
        }

    def check_budget_status(self) -> Dict[str, Any]:
        """Check current budget status and warnings."""
        usage = self.get_current_month_usage()

        status = {
            'current_usage': usage,
            'warnings': [],
            'blocked': False
        }

        # Check thresholds
        if usage['total_tokens'] >= self.budget_limits.block_limit:
            status['warnings'].append({
                'level': 'block',
                'message': f"Monthly budget exceeded ({usage['usage_percent']:.1f}%). AI analysis blocked.",
                'action': "Purchase more tokens at https://app.tavoai.net/billing"
            })
            status['blocked'] = True

        elif usage['total_tokens'] >= self.budget_limits.critical_limit:
            status['warnings'].append({
                'level': 'critical',
                'message': f"Critical: {usage['usage_percent']:.1f}% of monthly budget used.",
                'action': "Purchase more tokens at https://app.tavoai.net/billing"
            })

        elif usage['total_tokens'] >= self.budget_limits.warning_limit:
            status['warnings'].append({
                'level': 'warning',
                'message': f"Warning: {usage['usage_percent']:.1f}% of monthly budget used.",
                'action': "Monitor usage or purchase more tokens"
            })

        return status

    def should_block_ai_analysis(self) -> bool:
        """Check if AI analysis should be blocked due to budget limits."""
        usage = self.get_current_month_usage()
        return usage['total_tokens'] >= self.budget_limits.block_limit

    def get_usage_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get usage summary for specified period.

        Args:
            days: Number of days to look back

        Returns:
            Usage summary statistics
        """
        cutoff_time = time.time() - (days * 24 * 60 * 60)

        recent_records = [
            record for record in self.usage_history
            if record.timestamp > cutoff_time
        ]

        if not recent_records:
            return {
                'period_days': days,
                'total_tokens': 0,
                'total_cost_usd': 0,
                'average_daily_tokens': 0,
                'average_daily_cost': 0,
                'operations': {}
            }

        total_tokens = sum(record.tokens_used for record in recent_records)
        total_cost = sum(record.cost_usd for record in recent_records)

        # Group by operation
        operations = {}
        for record in recent_records:
            op = record.operation
            if op not in operations:
                operations[op] = {'tokens': 0, 'cost': 0, 'count': 0}
            operations[op]['tokens'] += record.tokens_used
            operations[op]['cost'] += record.cost_usd
            operations[op]['count'] += 1

        return {
            'period_days': days,
            'total_tokens': total_tokens,
            'total_cost_usd': total_cost,
            'average_daily_tokens': total_tokens / days,
            'average_daily_cost': total_cost / days,
            'operations': operations
        }

    def clear_history(self) -> None:
        """Clear usage history."""
        self.usage_history = []
        self._save_usage_history()


