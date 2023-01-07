from pathlib import Path
from typing import List, Union
from widgets.streamlit.resources.base import StreamlitResource

from widgets.base.exceptions import WidgetConfigurationException
from widgets.base.exceptions import WidgetFunctionException
from widgets.base.exceptions import WidgetInitializationException


class Widget:
    """
    Base class used for building interactive widgets.
    """

    resources:List[Resource] = list()
    data = dict()

    def __init__(self, data=dict()) -> None:
        """
        Set up the Widget object.
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
                raise WidgetConfigurationException("All resources must be a derivative of Resource")

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
        Create an HTML file which will load this widget.
        Should be overriden by each child class
        """

        pass
