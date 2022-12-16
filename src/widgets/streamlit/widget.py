from typing import List
from widgets.streamlit.resources.base import StreamlitResource
from widgets.base.exceptions import WidgetConfigurationException

class StreamlitWidget:
    """
    Base class used for building interactive widgets using Streamlit.
    """

    resources:List[StreamlitResource] = list()
    data = dict()

    def __init__(self) -> None:
        """Set up the StreamlitWidget object."""        
        pass

    def viz(self) -> None:
        """The viz() method should be overridden by any widget based on this class."""
        pass

    def run(self) -> None:
        """
        Primary entrypoint used to launch the widget.

        1. Connect to all resources defined in the widget;
        2. Invoke the viz() function;
        3. Add buttons extending functionality of the widget;
        """
        
        self.read_data()
        self.viz()
        self.extra_functions()

    def read_data(self) -> None:
        """Read in data from all of the resources defined in the widget."""
        
        # Iterate over each of the resources defined for this widget
        for resource in self.resources:

            # Make sure that the resource is a recognized type
            if not isinstance(resource, StreamlitResource):
                raise WidgetConfigurationException("All resources must be a derivative of StreamlitResource")

            # Store the contents of the resource in `data`, keyed by
            # the `id` attribute of the resource
            self.data[resource.id] = resource.read()

    def extra_functions(self) -> None:
        """Add generalized functionality to the widget."""
        pass
