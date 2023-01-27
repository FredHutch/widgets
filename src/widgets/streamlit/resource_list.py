from typing import Dict, List
from widgets.base.resource_list import ResourceList
from widgets.streamlit.resources.base import StResource


class StResourceList(ResourceList):
    """
    Collection of StResource objects.
    """

    resources: List[StResource] = list()
    resource_dict: Dict[str, StResource] = dict()

    def resource_key(self, resource_id):
        """Return the UI identifier for a resource."""

        return self._get_resource(resource_id).key()

    def set(self, resource_id, attr, val, update=True):
        """Set the value of an attribute of a resource."""

        # Call the set function of the resource
        self._get_resource(resource_id).set(attr, val, update=update)

    def set_value(self, resource_id, val, update=True):
        """Set the 'value' attribute of a resource."""

        # Call the set function of the resource
        self.set(resource_id, "value", val, update=update)
