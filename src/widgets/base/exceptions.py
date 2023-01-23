class WidgetConfigurationException(Exception):
    """Exception raised when a widget is not configured properly."""
    pass


class WidgetInitializationException(Exception):
    """Exception raised when a widget is not initialized properly."""
    pass


class WidgetFunctionException(Exception):
    """Exception raised when a widget function is not called properly."""
    pass


class ResourceConfigurationException(Exception):
    """Exception raised when a resource is not configured properly."""
    pass


class ResourceExecutionException(Exception):
    """Exception raised when a resource is not executed properly."""
    pass


class CLIInvocationException(Exception):
    """Exception raised when the CLI is not invoked properly."""
    pass


class CLIExecutionException(Exception):
    """Exception raised when the CLI is not executed properly."""
    pass


class IOException(Exception):
    """Exception raised upon IO error."""
    pass
