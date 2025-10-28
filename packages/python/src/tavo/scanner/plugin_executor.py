"""Plugin execution orchestration"""

import time
import logging
from typing import List, Dict, Any
from pathlib import Path

from ..plugins import (
    PluginRegistry,
    PluginType,
    PluginExecutionContext,
    PluginExecutionResult,
)
from ..plugins.exceptions import PluginExecutionError
from .scanner_config import ScannerConfig, ScanOptions

logger = logging.getLogger(__name__)


class PluginExecutor:
    """Orchestrates plugin execution"""

    def __init__(self, config: ScannerConfig):
        """Initialize plugin executor

        Args:
            config: Scanner configuration
        """
        self.config = config
        self.registry = PluginRegistry(
            api_key=config.api_key, cache_dir=config.plugin_cache_dir
        )

    def execute_plugins(
        self,
        target_path: Path,
        options: ScanOptions,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> List[PluginExecutionResult]:
        """Execute all configured plugins

        Args:
            target_path: Path to scan
            options: Scan options
            user_id: Optional user ID
            organization_id: Optional organization ID

        Returns:
            List of execution results
        """
        results = []

        # Execute static analysis plugins
        if options.static_analysis and options.static_plugins:
            for plugin_id in options.static_plugins:
                result = self._execute_plugin(
                    plugin_id=plugin_id,
                    plugin_type=PluginType.STATIC_ANALYSIS,
                    target_path=target_path,
                    options=options,
                    user_id=user_id,
                    organization_id=organization_id,
                )
                if result:
                    results.append(result)

        # Execute dynamic testing plugins
        if options.dynamic_testing and options.dynamic_plugins:
            for plugin_id in options.dynamic_plugins:
                result = self._execute_plugin(
                    plugin_id=plugin_id,
                    plugin_type=PluginType.DYNAMIC_TESTING,
                    target_path=target_path,
                    options=options,
                    user_id=user_id,
                    organization_id=organization_id,
                )
                if result:
                    results.append(result)

        return results

    def _execute_plugin(
        self,
        plugin_id: str,
        plugin_type: PluginType,
        target_path: Path,
        options: ScanOptions,
        user_id: Optional[str],
        organization_id: Optional[str],
    ) -> Optional[PluginExecutionResult]:
        """Execute a single plugin

        Args:
            plugin_id: Plugin identifier
            plugin_type: Expected plugin type
            target_path: Path to scan
            options: Scan options
            user_id: Optional user ID
            organization_id: Optional organization ID

        Returns:
            Execution result or None if execution fails
        """
        try:
            start_time = time.time()

            # Load plugin
            plugin = self.registry.load_plugin(plugin_id, plugin_type)

            # Get plugin configuration
            plugin_config = options.plugin_config.get(plugin_id, {})

            # Initialize plugin
            plugin.initialize(plugin_config)

            # Create execution context
            context = PluginExecutionContext(
                plugin_id=plugin_id,
                plugin_type=plugin_type,
                target_path=str(target_path),
                config=plugin_config,
                user_id=user_id,
                organization_id=organization_id,
                api_key=self.config.api_key,
                timeout=options.timeout,
            )

            # Execute plugin
            logger.info(f"Executing plugin: {plugin_id}")
            result = plugin.execute(context)

            # Add execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            result.execution_time_ms = execution_time_ms

            logger.info(
                f"Plugin {plugin_id} completed in {execution_time_ms}ms "
                f"with {len(result.findings)} findings"
            )

            # Cleanup
            plugin.cleanup()

            return result

        except PluginExecutionError as e:
            logger.error(f"Plugin {plugin_id} execution failed: {e}")
            # Return error result
            metadata = self.registry.get_plugin_metadata(plugin_id)
            return PluginExecutionResult(
                plugin_id=plugin_id,
                plugin_name=metadata.name if metadata else plugin_id,
                plugin_version=metadata.version if metadata else "unknown",
                success=False,
                errors=[str(e)],
            )

        except Exception as e:
            logger.error(f"Unexpected error executing plugin {plugin_id}: {e}")
            return None

    def list_available_plugins(
        self, plugin_type: Optional[PluginType] = None
    ) -> List[str]:
        """List available plugins

        Args:
            plugin_type: Filter by plugin type

        Returns:
            List of available plugin IDs
        """
        return self.registry.list_installed_plugins(plugin_type)
