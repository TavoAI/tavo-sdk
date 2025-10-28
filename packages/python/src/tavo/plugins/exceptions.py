"""Plugin system exceptions"""


class PluginError(Exception):
    """Base exception for plugin errors"""

    pass


class PluginNotFoundError(PluginError):
    """Raised when a plugin cannot be found"""

    pass


class PluginLoadError(PluginError):
    """Raised when a plugin fails to load"""

    pass


class PluginExecutionError(PluginError):
    """Raised when a plugin execution fails"""

    pass


class PluginValidationError(PluginError):
    """Raised when plugin validation fails"""

    pass


class PluginSecurityError(PluginError):
    """Raised when a security check fails for a plugin"""

    pass


class PluginDependencyError(PluginError):
    """Raised when plugin dependencies are not met"""

    pass
