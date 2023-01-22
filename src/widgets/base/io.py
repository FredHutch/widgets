from importlib.util import spec_from_file_location
from importlib.util import module_from_spec
from inspect import getsource
import sys
from widgets.base.widget import Widget
from widgets.base.exceptions import IOException, WidgetInitializationException


def _load_module(url):
    """Load the Python code from the indicated file as a module"""

    try:
        spec = spec_from_file_location("imported_widget", url)
    except Exception as e:
        msg = f"Error accessing URL: {url}\n{str(e)}"
        raise IOException(msg)

    try:
        module = module_from_spec(spec)
    except Exception as e:
        msg = f"Error loading module: {url}\n{str(e)}"
        raise IOException(msg)

    sys.modules["imported_widget"] = module

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        msg = f"Error executing code: {url}\n{str(e)}"
        raise IOException(msg)


def load_widget(url: str, widget_name: str) -> Widget:
    """
    Import a Widget defined in a script.

    Arguments:
        url (str):          URL to local or HTTP(S) file containing code
                            defining a Widget
        widget_name (str):  Name of the Widget defined in the file to import
    """

    # Load the script as a module
    _load_module(url)

    # Get the widget defined in that module
    widget = sys.modules["imported_widget"].__dict__.get(widget_name)

    # If that widget was not defined
    if widget is None:
        raise IOException(f"Widget {widget_name} not defined in {url}")

    # Try to instantiate the widget
    try:
        w = widget()
    except Exception as e:
        source = getsource(widget)
        msg = f"Error loading module:\n{source}\n{str(e)}"
        raise WidgetInitializationException(msg)

    # If the code does not define a valid Widget object
    if not isinstance(w, Widget):
        t = str(type(widget))
        msg = f"Code for {widget_name} must be a Widget-based object, not {t}"
        raise WidgetInitializationException(msg)

    return widget
