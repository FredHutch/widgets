import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from typing import Dict, List, Union
from widgets.base.exceptions import WidgetConfigurationException
from widgets.base.resource_list import ResourceList
from widgets.streamlit.resource.base import StResource


class StResourceList(ResourceList):
    """
    Collection of StResource objects.
    """

    resources: List[StResource] = list()
    _resource_dict: Dict[str, StResource] = dict()

    def setup_ui(
        self,
        container: Union[None, DeltaGenerator],
        sidebar=True
    ) -> None:
        """
        Run the .setup_ui() method for each Resource in the list.
        If a container is provided, add a new container to it.
        If no container is provided (is None), then set up a new container.
        """

        # If no container is provided
        if container is None:

            # Make a new one in the global scope
            if sidebar:
                list_container = st.sidebar.container()
            else:
                list_container = st.container()

        # If a container is provided
        else:

            # It must be a valid container
            if not isinstance(container, DeltaGenerator):
                msg = f"Not a valid container ({self.__class__.__name__})"
                raise WidgetConfigurationException(msg)

            # Make a new container within it
            list_container = container.container()

        # Provide an opportunity for child classes to manipulate the container
        # prior to setting up the UI for the child resources
        list_container = self.customize_container(list_container)

        super().setup_ui(list_container)

    def customize_container(self, container: DeltaGenerator) -> DeltaGenerator:
        """Customize the container prior to setting up the child resources."""
        return container

    def set(self, resource_id, attr, val, *subattrs, update=True, **kwargs):
        """
        Set the value of an attribute of a resource.
        Supports nested ResourceList objects.

        Set the attribute of a Resource:
            set(resource_id, attr, val)

        Set the attribute of a resource nested within a ResourceList:
            set(resource_id, subresource_id, attr, val)

        Optional kwargs are passed to the set() method for the Resource
        """

        # Call the set function defined by ResourceList
        super().set(resource_id, attr, val, *subattrs, update=update, **kwargs)

    def set_value(self, resource_id, val, *subattrs, update=True, **kwargs):
        """Set the 'value' attribute of a resource."""

        # Call the set_value function defined by ResourceList
        super().set_value(resource_id, val, *subattrs, update=update, **kwargs)
