from typing import Any, Dict, List
from widgets.base.resource import Resource
from widgets.base.exceptions import WidgetConfigurationException
from widgets.base.exceptions import WidgetFunctionException


class ResourceList:
    """
    Base class used for interacting with a list of Resources
    """

    resources: List[Resource] = list()
    resource_dict: Dict[str, Resource] = dict()

    def __init__(self):
        """
        Set up the ResourceList object
        """

        # The resource_dict must be empty at initialization
        self.resource_dict = dict()

        # Iterate over each resource defined in the widget
        for resource in self.resources:

            # Make sure that the resource is a recognized type
            if not isinstance(resource, Resource):
                msg = "All resources must be a derivative of Resource"
                raise WidgetConfigurationException(msg)

            # Make sure that the id attribute is not repeated
            if resource.id in self.resource_dict:
                msg = f"Resource ids must be unique (repeated: {resource.id})"
                raise WidgetConfigurationException(msg)
            self.resource_dict[resource.id] = resource

    def get(self, resource_id: str, attr: str) -> Any:
        """Get the value of an attribute of a resource."""

        # Return the value provided by the get method of the resource
        return self._get_resource(resource_id).get(attr)

    def get_value(self, resource_id: str) -> Any:
        """Get the 'value' attribute of a resource."""

        return self._get_resource(resource_id).get_value()

    def set(self, resource_id, attr, val):
        """Set the value of an attribute of a resource."""

        # Call the set function of the resource
        self._get_resource(resource_id).set(attr, val)

    def set_value(self, resource_id, val):
        """Set the 'value' attribute of a resource."""

        # Call the set function of the resource
        self.set(resource_id, "value", val)

    def _get_resource(self, resource_id) -> Resource:
        """Return the resource with a corresponding id."""

        # Get the resource
        r = self.resource_dict.get(resource_id)

        if r is None:
            raise WidgetFunctionException(f"No resource exists: {resource_id}")
        return r
