from pathlib import Path
from typing import Union
from widgets.base.exceptions import WidgetFunctionException
from widgets.base.resource import Resource


class Widget(Resource):
    """
    Base class used for building interactive widgets.

    Attributes:
            id (str):          The unique key used to identify the resource.
            label (str):       Label displayed to the user for the resource.
            help (str):        Help text describing the resource to the user.
            children (list):   List of child resources contained within.
    """

    def run_cli(self) -> None:
        """
        Entrypoint used to run the widget from the command line.
        Should be overridden by each specific widget type.
        """
        self.run()

    def to_html(self, fp: Union[Path, None] = None) -> Union[None, str]:
        """
        Create an HTML file which will load this widget.
        Should be overriden by each child class
        """
        pass

    def to_script(self, fp: Union[Path, None] = None) -> Union[None, str]:
        """
        Create a python script which will be load this widget.
        If fp is None, return a string.
        Should be overridden by each child class.
        """
        pass

    def _to_file(
        self,
        text: str,
        fp: Union[Path, None] = None
    ) -> Union[None, str]:
        """
        If fp is not None, write the contents of text to the file object fp.
        If fp is None, return text.
        """

        # If a path was not provided
        if fp is None:

            # Return the string
            return text

        # Otherwise
        else:

            if not isinstance(fp, Path):
                msg = "The argument of _to_file() must be a Path or None"
                raise WidgetFunctionException(msg)

            # Write out to the file
            with open(fp, "w") as handle:
                handle.write(text)

    def download_html_button(self):
        """
        Render a button which allows the user to download the widget as HTML.
        """
        pass

    def download_script_button(self):
        """
        Render a button which allows the user to download the widget as code.
        """
        pass
