from tempfile import _TemporaryFileWrapper, NamedTemporaryFile
from pathlib import Path
import streamlit as st
from streamlit.web.cli import _main_run
from typing import Any, Dict, List, Union
from widgets.base.widget import Widget
from widgets.base.helpers import render_template
from widgets.streamlit.resources.base import StResource


class StreamlitWidget(Widget):
    """
    Base class used for building interactive widgets using Streamlit.
    """

    resources: List[StResource] = list()
    resource_dict: Dict[str, StResource] = dict()
    requirements: List[str] = ["widgets-lib"]
    imports: List[str] = [
        "import streamlit as st",
        "from widgets.streamlit.resources.dataframe import StDataFrame",
        "from widgets.streamlit.resources.value import StString",
        "from widgets.streamlit.resources.value import StInteger",
        "from widgets.streamlit.resources.value import StFloat",
        "from widgets.streamlit.resources.value import StSelectString",
        "from widgets.streamlit.widget import StreamlitWidget"
    ]
    extra_imports: List[str] = []

    def run_cli(
        self,
        args: List[str] = [],
        flag_options: Dict[str, Any] = {},
        title="Widget"
    ) -> None:
        """
        Run the widget from the command line.
        """

        # Make a copy of this widget in a tempfile
        with self._script_tempfile(title=title) as script:

            # Launch the script with Streamlit
            _main_run(script.name, args, flag_options=flag_options)

    def download_html_button(self):
        """
        Render a button which allows the user to download the widget as HTML.
        """

        with st.sidebar:
            st.download_button(
                "Download HTML",
                self._render_html(),
                file_name=f"{self._name()}.html",
                mime="text/html",
                help="Download this widget as a webpage (HTML)"
            )

    def download_script_button(self):
        """
        Render a button which allows the user to download the widget as code.
        """

        with st.sidebar:
            st.download_button(
                "Download Script",
                self._render_script(),
                file_name=f"{self._name()}.py",
                mime="text/x-python",
                help="Download this widget as a script (Python)"
            )

    def _render_script(self, title="Widget") -> str:
        """
        Return the script for this widget as a string.
        """

        # Render the template for this script
        script = render_template(
            "streamlit_single.py.j2",
            title=title,
            imports=self._imports(),
            widget_source=self._source(),
            widget_name=self._name()
        )

        return script

    def _script_tempfile(self, title="Widget") -> _TemporaryFileWrapper:
        """
        Return a temporary file object which contains a script for this widget.
        """

        # Make a temporary file
        fp = NamedTemporaryFile(mode="w+t", prefix="script", suffix=".py")

        # Write out the script
        fp.write(self._render_script(title=title))

        # Move the pointer back to the top
        fp.seek(0)

        # Return the file object
        return fp

    def viz(self) -> None:
        """
        The viz() method should be overridden by any widget based on this.
        """
        pass

    def extra_functions(self) -> None:
        """Add generalized functionality to the widget."""
        pass

    def to_html(self, fp: Union[Path, None] = None) -> Union[None, str]:
        """
        Create an HTML file which will load this widget using the stlite
        library, based on pyodide.
        If no path is provided, return a string representation.
        """

        # Create the HTML as a string
        html = self._render_html()

        # Write it out to a file (if provided), or return the string
        return self._to_file(html, fp)

    def to_script(self, fp: Union[Path, None] = None) -> Union[None, str]:
        """
        Create a python script which will be load this widget.
        If fp is None, return a string.
        Should be overridden by each child class.
        """

        # Create the Python script as a string
        script = self._render_script()

        # Write it out to a file (if provided), or return the string
        return self._to_file(script, fp)

    def _imports(self) -> str:
        """Return the imports needed by this widget."""

        return "\n".join(["\n".join(self.imports), "\n".join(self.extra_imports)]) # noqa

    def _render_html(
        self,
        title="Widget",
        stlite_ver="0.22.1",
        footer="Made with widgets-lib (github.com/FredHutch/widgets)"
    ):
        """Render the widget as HTML"""

        # Render the template for this HTML
        html = render_template(
            "streamlit_single.html.j2",
            title=title,
            stlite_ver=stlite_ver,
            footer=footer,
            requirements=self.requirements,
            imports=self._imports(),
            widget_source=self._source(),
            widget_name=self._name()
        )

        return html

    def resource_key(self, resource_id):
        """Return the UI identifier for a resource."""

        return self._get_resource(resource_id).key()
