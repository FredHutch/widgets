from tempfile import _TemporaryFileWrapper, NamedTemporaryFile, TemporaryFile
from jinja2 import Environment, PackageLoader
from pathlib import Path
from streamlit.web.cli import _main_run
from typing import IO, Any, Dict, List, Union
from widgets.base.widget import Widget
from widgets.base.resource import Resource
from widgets.base.exceptions import WidgetConfigurationException
from widgets.base.exceptions import WidgetFunctionException
from widgets.base.exceptions import WidgetInitializationException


class StreamlitWidget(Widget):
    """
    Base class used for building interactive widgets using Streamlit.
    """

    requirements:List[str] = ["widgets"]
    imports:List[str] = [
        "import streamlit as st",
        "from widgets.streamlit.resources.dataframe import StDataFrame",
        "from widgets.streamlit.resources.value import StString, StInteger, StFloat",
        "from widgets.streamlit.widget import StreamlitWidget"
    ]
    extra_imports:List[str] = []

    def __init__(self, data=dict()) -> Widget:
        """
        Set up the StreamlitWidget object.
        Optionally provide input data which will override the default values for each
        of the resources defined by this widget.
        """

        if not isinstance(data, dict):
            raise WidgetInitializationException(f"data must be a dict, not a {type(data)}")

        # Attach the data provided at initialization
        self.data = data

        # Iterate over each resource defined in the widget
        for resource in self.resources:

            # Make sure that the resource is a recognized type
            if not isinstance(resource, Resource):
                raise WidgetConfigurationException("All resources must be a derivative of StreamlitResource")

            # If any data was provided at the time of initialization, use that to
            # override the default value defined for the resource
            resource._setup_default(data.get(resource.id))

            # Populate the initial state of the `data` object
            self.data[resource.id] = resource.default

    def run(self) -> None:
        """
        Primary entrypoint used to launch the widget.

        1. Run the user_input() method for all resources defined in the widget;
        2. Invoke the viz() function;
        3. Add buttons extending functionality of the widget;
        """
        
        self.inputs()
        self.viz()
        self.extra_functions()

    def run_cli(self, args:List[str]=[], flag_options:Dict[str,Any]={}, title="Widget") -> None:
        """
        Run the widget from the command line.
        """

        # Make a copy of this widget in a tempfile
        with self._render_script(title=title) as script:

            # Launch the script with Streamlit
            _main_run(script.name, args, flag_options=flag_options)

    def _render_script(self, title="Widget") -> _TemporaryFileWrapper:
        """Return a temporary file object which contains a script for this widget."""

        # Render the template for this script
        script = self._render_template(
            "streamlit_single.py.j2",
            title=title,
            imports=self._imports(),
            widget_source=self._source(),
            widget_name=self._name(),
            data=self._data_to_json()
        )

        # Make a temporary file
        fp = NamedTemporaryFile(mode="w+t", prefix="script", suffix=".py")

        # Write out the script
        fp.write(script)

        # Move the pointer back to the top
        fp.seek(0)

        # Return the file object
        return fp

    def inputs(self) -> None:
        """Read in data from all of the resources defined in the widget."""
        
        # Iterate over each of the resources defined for this widget
        for resource in self.resources:

            # Add the interactive input element, if any has been defined
            # We pass in the data object for the widget so that the value
            # can be updated when the user input changes
            resource.user_input(self.data)

    def viz(self) -> None:
        """The viz() method should be overridden by any widget based on this class."""
        pass

    def extra_functions(self) -> None:
        """Add generalized functionality to the widget."""
        pass

    def to_html(self, fp:Union[Path, None]=None) -> Union[None, str]:
        """
        Create an HTML file which will load this widget using the stlite
        library, based on pyodide.
        If no path is provided, return a string representation.
        """

        # Create the HTML as a string
        html = self._render_html()

        # If a path was not provided
        if fp is None:

            # Return the string
            return html

        # Otherwise
        else:

            if not isinstance(fp, Path):
                raise WidgetFunctionException("The argument of to_html() must be a Path or None")


            # Write out to the file
            with open(fp, "w") as handle:
                handle.write(html)

    def _imports(self) -> str:
        """Return the imports needed by this widget."""

        return "\n".join(["\n".join(self.imports), "\n".join(self.extra_imports)])

    def _render_html(
        self,
        title="Widget",
        stlite_ver="0.22.1",
        footer="Made with widgets-lib (github.com/FredHutch/widgets)"
    ):
        """Render the widget as HTML"""

        # Render the template for this HTML
        html = self._render_template(
            "streamlit_single.html.j2",
            title=title,
            stlite_ver=stlite_ver,
            footer=footer,
            requirements=self.requirements,
            imports=self._imports(),
            widget_source=self._source(),
            widget_name=self._name(),
            data=self._data_to_json()
        )
        
        return html

    def _render_template(self, template_name:str, **kwargs):
        """Return a jinja2 template defined in this library."""

        # Set up the jinja2 environment
        env = Environment(
            loader=PackageLoader("widgets")
        )

        # Get the template being used
        template = env.get_template(template_name)

        # Render the template
        return template.render(**kwargs)
