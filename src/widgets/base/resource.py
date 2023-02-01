from inspect import signature
from typing import Any
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.exceptions import ResourceExecutionException


class Resource:
    """
    Base class for all resources used by widgets.

    Attributes:
            id (str):          The unique key used to identify the resource.
            value:             The starting value for the resource.
            label (str):       Label displayed to the user for the resource.
            help (str):        Help text describing the resource to the user.
            parent_ids (list): Optional list of all parent element ids.
    """

    id = ""
    value = None
    label = ""
    help = ""
    parent_ids = []

    def __init__(
        self,
        id="",
        value=None,
        label="",
        help="",
        parent_ids=[]
    ) -> None:
        """
        Set up the attributes which are used by all Resource objects.
        """

        # The 'id' cannot be empty
        if len(id) == 0:
            msg = "Must provide id for Resource"
            raise ResourceConfigurationException(msg)

        # Save the id and starting value for this particular resource
        self.id = id
        self.value = value
        self.parent_ids = parent_ids

        # If no label is provided, default to the id
        self.label = id if label == "" else label
        self.help = help

    def setup_ui(self, container) -> None:
        """
        Method used to provide the option for user input from the GUI.
        Should be overridden by each specific resource.
        """
        pass

    def get(self, attr) -> Any:
        """Return the value of the attribute for this resource."""

        if attr not in self.__dict__:
            msg = f"Attribute does not exist {attr} for {self.id}"
            raise ResourceExecutionException(msg)

        return self.__dict__.get(attr)

    def get_value(self) -> Any:
        """
        Return the selected value of this resource (the 'value' attribute).
        Provided in the base class to be overridden by specialized resources.
        """

        return self.get("value")

    def set(self, attr, val) -> None:
        """Set the value of an attribute for this resource."""

        self.__dict__[attr] = val

    def set_value(self, val, **kwargs) -> None:
        """Set the value of the 'value' attribute for this resource."""

        self.set("value", val, **kwargs)

    def source(self, indent=4) -> str:
        """Return the code used to initialize this resource."""

        spacer = "".join([" " for _ in range(indent)])

        # Get the signature of the initialization function
        sig = signature(self.__class__.__init__)

        # Build up the parameters to use to invoke the object
        params = {}

        for kw in sig.parameters.keys():
            if kw == "self":
                continue
            else:
                params[kw] = self.__dict__[kw]

        # Format the params as a string
        params_str = f',\n{spacer}{spacer}{spacer}'.join([
            f"{kw}={self._source_val(val, indent=indent+4)}"
            for kw, val in params.items()
        ])

        return f"{self.__class__.__name__}(\n{spacer}{spacer}{spacer}{params_str}\n{spacer}{spacer})" # noqa

    def _source_val(self, val, indent=4) -> Any:
        """
        Return a string representation of an attribute value
        which can be used in source code initializing this resource.
        """

        if isinstance(val, str):
            return f'"{val}"'
        elif isinstance(val, list):
            return f"""[{', '.join([
                self._source_val(i, indent=indent)
                for i in val
            ])}]"""
        elif isinstance(val, Resource):
            return val.source(indent=indent)
        else:
            return val
