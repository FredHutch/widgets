from tempfile import _TemporaryFileWrapper, NamedTemporaryFile
from pathlib import Path
from streamlit.web.cli import _main_run
from typing import Any, Dict, List, Union
from widgets.base.widget import Widget
from widgets.base.helpers import render_template
from widgets.streamlit.resource.base import StResource
import widgets


class StreamlitWidget(StResource, Widget):
    """
    Base class used for building interactive widgets using Streamlit.
    """

    requirements: List[str] = []
    imports: List[str] = [
        "import streamlit as st",
        "from widgets.streamlit import *"
    ]
    extra_imports: List[str] = []

    # "auto" or "expanded" or "collapsed"
    initial_sidebar_state = "auto"

    # "centered" or "wide"
    layout = "centered"

    title = ""
    subtitle = ""

    def prep(self) -> None:
        """
        Set up a Streamlit-based widget
        """

        # Instantiate the base container elements
        super().prep()

        # Display any title/subtitle provided by the user
        if isinstance(self.title, str) and len(self.title) > 0:
            self._get_ui_element(
                sidebar=False,
                empty=False
            ).markdown(
                f"## {self.title}"
            )
        if isinstance(self.subtitle, str) and len(self.subtitle) > 0:
            self._get_ui_element(
                sidebar=False,
                empty=False
            ).markdown(
                f"### {self.subtitle}"
            )

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

    def download_html_button(self, sidebar=True):
        """
        Render a button which allows the user to download the widget as HTML.
        """

        self._get_ui_element(
            sidebar=sidebar,
            empty=False
        ).download_button(
            "Download HTML",
            self._render_html(title=self._name()),
            file_name=f"{self._name()}.html",
            mime="text/html",
            help="Download this widget as a webpage (HTML)"
        )

    def download_script_button(self, sidebar=True):
        """
        Render a button which allows the user to download the widget as code.
        """

        self._get_ui_element(
            sidebar=sidebar,
            empty=False
        ).download_button(
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
            title=title if len(self.title) == 0 else self.title,
            layout=self.layout,
            initial_sidebar_state=self.initial_sidebar_state,
            imports=self._imports(),
            widget_source=self.source_all(),
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

    def to_html(self, fp: Union[Path, None] = None) -> Union[None, str]:
        """
        Create an HTML file which will load this widget using the stlite
        library, based on pyodide.
        If no path is provided, return a string representation.
        """

        # Create the HTML as a string
        html = self._render_html(title=self._name())

        # Write it out to a file (if provided), or return the string
        return self._to_file(html, fp)

    def to_script(self, fp: Union[Path, None] = None) -> Union[None, str]:
        """
        Create a python script which will be used to load this widget.
        If fp is None, return a string.
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
        footer="Widget (github.com/FredHutch/widgets)",
        stlite_ver="0.22.2",
    ):
        """Render the widget as HTML"""

        # Render the template for this HTML
        html = render_template(
            "streamlit_single.html.j2",
            title=title,
            stlite_ver=stlite_ver,
            footer=footer,
            requirements=self.requirements + [
                f"widgets-lib=={widgets.__version__}"
            ],
            imports=self._imports(),
            widget_source=self.source_all().replace("\\", "\\\\"),
            widget_name=self._name()
        )

        return html
