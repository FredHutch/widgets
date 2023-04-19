from importlib.metadata import PackageNotFoundError, version
from tempfile import _TemporaryFileWrapper, NamedTemporaryFile
from pathlib import Path
import streamlit as st
from typing import Any, Dict, List, Union
from widgets.base.exceptions import WidgetFunctionException
from widgets.base.widget import Widget
from widgets.base.helpers import render_template
from widgets.st_base.resource import StResource
import widgets


class StreamlitWidget(StResource, Widget):
    """
    Base class used for building interactive widgets using Streamlit.
    """

    requirements: List[str] = []
    pyodide_requirements: List[str] = []
    imports: List[str] = [
        "import streamlit as st",
        "from widgets.streamlit import *"
    ]
    extra_imports: List[str] = []

    # "auto" or "expanded" or "collapsed"
    initial_sidebar_state = "auto"

    # "centered" or "wide"
    layout = "centered"

    # Optional GA tag
    ga_tag = None

    title = ""
    subtitle = ""

    def __init__(
        self,
        requirements: Union[List[str], None] = None,
        pyodide_requirements: Union[List[str], None] = None,
        imports: Union[List[str], None] = None,
        extra_imports: Union[List[str], None] = None,
        initial_sidebar_state: Union[str, None] = None,
        layout: Union[str, None] = None,
        ga_tag: Union[str, None] = None,
        title: Union[str, None] = None,
        subtitle: Union[str, None] = None,
        **kwargs
    ):
        super().__init__(
            requirements=self.__class__.requirements,
            pyodide_requirements=self.__class__.pyodide_requirements,
            imports=self.__class__.imports,
            extra_imports=self.__class__.extra_imports,
            initial_sidebar_state=self.__class__.initial_sidebar_state,
            layout=self.__class__.layout,
            ga_tag=self.__class__.ga_tag,
            title=self.__class__.title,
            subtitle=self.__class__.subtitle,
            **kwargs
        )

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
            from streamlit.web.cli import _main_run
            _main_run(script.name, args, flag_options=flag_options)

    def clone_button(
            self,
            sidebar=True,
            as_html=True,
            as_script=True
    ):
        """
        Render a button which gives the user the option to download a
        cloned copy of this widget.
        Importantly, the code is only generated once the button is
        initially pressed, which should make it more performant than
        download_html_button and download_script_buton, which have to
        recompute the clone with every change to the object.
        """

        if sidebar:
            button_container = self._get_ui_element(
                sidebar=sidebar,
                empty=False
            )
        else:
            _, button_container, _ = self._get_ui_element(
                sidebar=sidebar,
                empty=False
            ).columns(3)

        if st.session_state.get("_ready_to_clone", False):

            if as_html:
                button_container.download_button(
                    "Download HTML",
                    self._render_html(
                        title=self._name(),
                        layout=self.layout,
                        initial_sidebar_state=self.initial_sidebar_state
                    ),
                    file_name=f"{self._name()}.html",
                    mime="text/html",
                    help="Download this widget as a webpage (HTML)",
                    use_container_width=True,
                    on_click=self._set_session_state,
                    args=('_ready_to_clone', False)
                )
            if as_script:
                button_container.download_button(
                    "Download Script",
                    self._render_script(),
                    file_name=f"{self._name()}.py",
                    mime="text/x-python",
                    help="Download this widget as a script (Python)",
                    use_container_width=True,
                    on_click=self._set_session_state,
                    args=('_ready_to_clone', False)
                )

        else:

            button_container.button(
                "Clone",
                help="Save a copy with all changes frozen",
                on_click=self._set_session_state,
                args=('_ready_to_clone', True)
            )

    def _set_session_state(self, kw, val):
        """Utility to set a value in the session state."""
        st.session_state[kw] = val

    def download_html_button(
        self,
        sidebar=True
    ):
        """
        Render a button which allows the user to download the widget as HTML.
        """

        col1, col2, col3 = self._get_ui_element(
            sidebar=sidebar,
            empty=False
        ).columns(3)

        col2.download_button(
            "Download HTML",
            self._render_html(
                title=self._name(),
                layout=self.layout,
                initial_sidebar_state=self.initial_sidebar_state
            ),
            file_name=f"{self._name()}.html",
            mime="text/html",
            help="Download this widget as a webpage (HTML)",
            use_container_width=True
        )

    def download_script_button(self, sidebar=True):
        """
        Render a button which allows the user to download the widget as code.
        """

        col1, col2, col3 = self._get_ui_element(
            sidebar=sidebar,
            empty=False
        ).columns(3)

        col2.download_button(
            "Download Script",
            self._render_script(),
            file_name=f"{self._name()}.py",
            mime="text/x-python",
            help="Download this widget as a script (Python)",
            use_container_width=True
        )

    def _render_script(self, title="Widget") -> str:
        """
        Return the script for this widget as a string.
        """

        if self.disable_sidebar:
            initial_sidebar_state = "collapsed"
        else:
            initial_sidebar_state = self.initial_sidebar_state

        # Render the template for this script
        script = render_template(
            "streamlit_single.py.j2",
            title=title if len(self.title) == 0 else self.title,
            layout=self.layout,
            initial_sidebar_state=initial_sidebar_state,
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

    def to_html(
        self,
        fp: Union[Path, None] = None
    ) -> Union[None, str]:
        """
        Create an HTML file which will load this widget using the stlite
        library, based on pyodide.
        If no path is provided, return a string representation.
        """

        # Create the HTML as a string
        html = self._render_html(
            title=self._name(),
            layout=self.layout,
            initial_sidebar_state=self.initial_sidebar_state
        )

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
        layout="centered",
        initial_sidebar_state="auto",
        stlite_ver="0.31.0",
    ):
        """Render the widget as HTML"""

        # Pin the version of all requirements
        requirements = [
            self._pin_module_version(module)
            for module in self.requirements
        ] + [
            f"widgets-lib=={widgets.__version__}"
        ]

        # Set up the contents of the HTML
        kwargs = dict(
            title=title,
            layout=layout,
            initial_sidebar_state=initial_sidebar_state,
            stlite_ver=stlite_ver,
            requirements=requirements,
            imports=self._imports(),
            widget_source=self.source_all().replace("\\", "\\\\"),
            widget_name=self._name()
        )

        # Select the template based on whether a ga_tag exists
        if self.ga_tag is None:
            template = "streamlit_single.html.j2"
        else:
            template = "streamlit_single_ga.html.j2"
            kwargs['ga_tag'] = self.ga_tag

        # Render the template for this HTML
        html = render_template(
            template,
            **kwargs
        )

        return html

    def _pin_module_version(self, module):
        """
        Pin a module version, if possible.
        Do not pin a version for any packages which are
        listed in self.pyodide_requirements.
        """

        if module in self.pyodide_requirements:
            return module

        try:
            module_ver = version(module)
        except PackageNotFoundError:
            msg = f"Module is not installed: {module}"
            raise WidgetFunctionException(msg)

        return f"{module}=={module_ver}"
