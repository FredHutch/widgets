from typing import Any, Dict, List, Union
from widgets.base.resource import Resource
from widgets.base.exceptions import ResourceExecutionException
from widgets.base.exceptions import WidgetConfigurationException
from widgets.base.exceptions import WidgetFunctionException


class ResourceList(Resource):
    """
    Base class used for interacting with a list of Resources

    Attributes:
            id (str):          The unique key used to identify the resource.
            label (str):       Label displayed to the user for the resource.
            help (str):        Help text describing the resource to the user.
            resources (list):  List of resources contained in this object.

    """

    resources: List[Resource] = list()
    _resource_dict: Dict[str, Resource] = dict()

    def __init__(
        self,
        id="root",
        resources: List[Resource] = [],
        label="",
        help="",
        **kwargs
    ) -> None:
        """
        Set up the ResourceList object
        """

        # Set up the core attributes of the ResourceList
        super().__init__(id=id, label=label, help=help, **kwargs)

        # The _resource_dict must be empty at initialization
        self._resource_dict = dict()

        # If resources were provided
        if len(resources) > 0:

            # Attach the resource list to the object
            self.resources = resources

        # Iterate over each resource defined in the widget
        for resource in self.resources:

            # Make sure that the resource is a recognized type
            if not isinstance(resource, Resource):
                msg = "All resources must be a derivative of Resource"
                raise WidgetConfigurationException(msg)

            # Make sure that the id attribute is not repeated
            if resource.id in self._resource_dict:
                msg = f"Resource ids must be unique (repeated: {resource.id})"
                raise WidgetConfigurationException(msg)
            self._resource_dict[resource.id] = resource

            # Attach this list as the parent of the resource
            resource.parent = self

    def get(self, resource_id: str, attr: str, *subattrs, **kwargs) -> Any:
        """
        Get the value of an attribute of a resource, optionally
        including subattributes for nested ResourceList objects.

        Get the attribute of a Resource:
            get(resource_id, attr)

        Get the attribute of a resource nested within a ResourceList:
            get(resource_id, subresource_id, attr)

        Optional kwargs are passed to the get() method for the Resource
        """

        # Get the indicated resource
        r = self._get_resource(
            resource_id,
            # If subattribute(s) were specified, the first level is a list
            is_list=len(subattrs) > 0
        )

        # Recursively run this get function on that object
        return r.get(attr, *subattrs, **kwargs)

    def get_value(self, resource_id: str, *subattrs, **kwargs) -> Any:
        """
        Get the contents of the 'value' attribute of a resource.
        Supports nested ResourceList objects.

        Get the value of a Resource:
            get_value(resource_id)

        Get the attribute of a resource nested within a ResourceList:
            get_value(resource_id, subresource_id)

        Optional kwargs are passed to the get_value() method for the Resource
        """

        # Get the indicated resource
        r = self._get_resource(
            resource_id,
            # If subattribute(s) were specified, the first level is a list
            is_list=len(subattrs) > 0
        )

        # Recursively run this get_value function on that object
        return r.get_value(*subattrs, **kwargs)

    def all_values(self, *subattrs, **kwargs) -> dict:
        """
        Return a dict with the values of every element in this list.
        The keys of the dict will be the .id element, while the
        value will be the results of .get_value() for each Resource,
        and the results of .all_values() for each Resource List.

        Optional kwargs will be passed along to those methods.
        """

        # If a subattrs was specified
        if len(subattrs) > 0:

            subattrs = list(subattrs)

            # The first element must be a resource
            resource_id = subattrs.pop(0)

            # Get the resource
            r = self._get_resource(
                resource_id,
                # If subattribute(s) were specified, the first level is a list
                is_list=len(subattrs) > 0
            )

            # Return the all_values() result for that resource
            return r.all_values(*subattrs, **kwargs)

        else:

            return {
                resource_id: r.all_values(**kwargs) if isinstance(r, ResourceList) else r.get_value(**kwargs) # noqa
                for resource_id, r in self._resource_dict.items()
            }

    def set(self, resource_id, attr, val, *subattrs, **kwargs) -> None:
        """
        Set the value of an attribute of a resource.
        Supports nested ResourceList objects.

        Set the attribute of a Resource:
            set(resource_id, attr, val)

        Set the attribute of a resource nested within a ResourceList:
            set(resource_id, subresource_id, attr, val)

        Optional kwargs are passed to the set() method for the Resource
        """

        # Get the indicated resource
        r = self._get_resource(
            resource_id,
            # If subattribute(s) were specified, the first level is a list
            is_list=len(subattrs) > 0
        )

        # Call the set function of the resource
        r.set(attr, val, *subattrs, **kwargs)

    def set_value(self, resource_id, val, *subattrs, **kwargs) -> None:
        """Set the 'value' attribute of a resource."""

        # Get the indicated resource
        r = self._get_resource(
            resource_id,
            # If subattribute(s) were specified, the first level is a list
            is_list=len(subattrs) > 0
        )

        # Call the set_value function on that resource
        r.set_value(val, *subattrs, **kwargs)

    def _get_resource(
        self,
        resource_id,
        is_list=False
    ) -> Union[Resource, 'ResourceList']:
        """Return the resource with a corresponding id."""

        # Get the resource
        r = self._resource_dict.get(resource_id)

        # If no key exists for resource_id
        if r is None:
            raise WidgetFunctionException(f"No resource exists: {resource_id}")

        # If the input specified that it should be a ResourcesList
        if is_list:

            # Check the class
            if not isinstance(r, ResourceList):
                msg = f"Element must contain nested resources ({resource_id})"
                raise ResourceExecutionException(msg)

        return r

    def setup_ui(self, container) -> None:
        """Run the .setup_ui() method for each Resource in the list"""

        for r in self.resources:
            r.setup_ui(container)
