from importlib.util import spec_from_file_location
from importlib.util import module_from_spec
import sys
from widgets.streamlit.widget import StreamlitWidget
from widgets.base.widget import Widget
from widgets.base.exceptions import CLIExecutionException


def _load_module(url):
    """Load the Python code from the indicated file as a module"""

    try:
        spec = spec_from_file_location("imported_widget", url)
    except Exception as e:
        msg = f"Error accessing URL: {url}\n{str(e)}"
        raise CLIExecutionException(msg)

    try:
        module = module_from_spec(spec)
    except Exception as e:
        msg = f"Error loading module: {url}\n{str(e)}"
        raise CLIExecutionException(msg)

    sys.modules["imported_widget"] = module

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        msg = f"Error executing code: {url}\n{str(e)}"
        raise CLIExecutionException(msg)


def load_widget(url, widget_name) -> Widget:
    """
    Import a Widget defined in a script.
    
    Arguments:
        url (str):          URL to local or HTTP(S) file containing code defining a Widget
        widget_name (str):  Name of the Widget defined in the file to import
    """

    # Load the script as a module
    _load_module(url)

    # Get the widget defined in that module
    widget = sys.modules["imported_widget"].__dict__.get(widget_name)

    # If that widget was not defined
    if widget is None:
        raise CLIExecutionException(f"Widget {widget_name} not defined in {url}")

    # If the code does not define a valid Widget object
    if not isinstance(widget(), Widget):
        raise CLIExecutionException(f"Code for {widget_name} must be a Widget-based object, not {str(type(widget))}")

    return widget
