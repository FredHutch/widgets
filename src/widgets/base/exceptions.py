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