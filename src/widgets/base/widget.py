from inspect import getmro, getsource, isfunction
from pathlib import Path
from typing import Union
from widgets.base.exceptions import CLIExecutionException
from widgets.base.exceptions import WidgetFunctionException
from widgets.base.helpers import render_template
from widgets.base.resource_list import ResourceList


class Widget(ResourceList):
    """
    Base class used for building interactive widgets.
    The list of resources will be mapped by .id to the
    resource_dict at initialization.
    """

    def run(self) -> None:
        """
        Primary entrypoint used to launch the widget.

        1. Run the setup_ui() method for all resources defined in the widget;
        2. Invoke the viz() function;
        3. Add buttons extending functionality of the widget;
        """

        self.inputs()
        self.viz()
        self.extra_functions()

    def run_cli(self) -> None:
        """
        Entrypoint used to run the widget from the command line.
        Should be overridden by each specific widget type.
        """
        self.run()

    def inputs(self) -> None:
        """Read in data from all of the resources defined in the widget."""

        # Iterate over each of the resources defined for this widget
        for resource in self.resources:

            # Add the interactive input element, if any has been defined
            resource.setup_ui()

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

    def _source(self) -> str:
        """
        Return the source code for this live widget as a string.
        """

        source = render_template(
            "source.py.j2",
            name=self._name(),
            parent_name=self._parent_name(),
            resources=self._source_resources(),
            attributes=self._source_attributes(),
            functions=self._source_functions()
        )

        # Backticks in the source code will cause errors in HTML
        if "`" in source:
            raise CLIExecutionException("Script may not contain backticks (`)")

        return source

    def _name(self) -> str:
        """Return the name of this widget."""

        return self.__class__.__name__

    def _parent_name(self) -> str:
        """Return the name of the parent class for this object."""

        return self._parent_class().__name__

    def _parent_class(self):
        """Return the parent class for this object."""

        for cls in getmro(self.__class__):
            if cls != self.__class__:
                return cls

    def _class_items(self, filter_functions=False):
        """
        Yield the items associated with the class of this widget.
        If filter_functions is True, yield only functions, otherwise
        do not yield any functions.
        """
        for kw, val in self.__class__.__dict__.items():
            if kw.startswith("__"):
                continue
            if filter_functions == isfunction(val):
                yield kw, val

    def _source_resources(self, indent=4) -> str:
        """
        Return a string which captures the source code needed to initialize
        the resources attached to this object.
        """
        spacer = "".join([" " for _ in range(indent)])

        # Format the source code for each of the resources in this widget
        resources_str = []
        for r in self.resources:

            # Format the source code and append it to the lsit
            resources_str.append(r.source())

        # Join all of those resource strings into a list
        line_spacer = f",\n{spacer}{spacer}"
        resources_str = f"    resources = [\n{spacer}{spacer}{line_spacer.join(resources_str)}\n{spacer}]" # noqa

        return resources_str

    def _source_attributes(self, omit=["resources", "resource_dict"]) -> str:
        """
        Return a text block which captures the attributes of this class.
        Any attributes in the omit list will be omitted.
        """

        attributes = []

        # Iterate over the attributes of this class
        for kw, attrib in self._class_items(filter_functions=False):

            # If the attribute is not in the omit list
            if kw not in omit:

                # Add it to the list
                attributes.append(f"    {kw} = {self._source_val(attrib)}")

        return "\n\n".join(attributes)

    def _source_functions(self) -> str:
        """
        Return a text block with source code for all functions of this widget
        which do not match the parent class.
        """

        return "\n\n".join([
            getsource(func)
            for _, func in self._class_items(filter_functions=True)
        ])

    def _source_val(self, val):
        """
        Return a string representation of an attribute value
        which can be used in source code initializing this widget.
        """

        if isinstance(val, str):
            return f'"{val}"'
        else:
            return val
