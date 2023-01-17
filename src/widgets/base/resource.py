from inspect import signature
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.helpers import source_val


class Resource:
    """
    Base class for all resources used by widgets.

    Attributes:
            id (str):   The unique key used to store the resource
                        in the widget `data` object.
            default:    The default value for the resource, used
                        if no saved value is present.
            datatype:   The variable type returned by the `load()` method
                        (should match the type of the default value).
            label (str): Label displayed to the user for the resource
            help (str): Help text describing the resource to the user
    """

    id: str = None
    default = None
    datatype: type = None
    label: str = None
    help: str = None

    def setup(
        self,
        id="",
        default=None,
        label="",
        help=""
    ) -> None:
        """
        Set up the attributes which are used by all Resource objects.
        """

        # Set up the id, label, and help attributes
        self._setup_attributes(id, label, help)

        # Set up the default value
        self._setup_default(default)

        # If any extra setup behavior is needed, invoke it here
        self._setup_extra()

    def _setup_default(self, default):
        """
        If a non-null value is provided, assign it to the default attribute
        for this object.
        Otherwise, use an empty initialization of the default datatype
        """

        # If a non-null default value is provided
        if default is not None:

            # Make sure that the default value conforms to the expected type
            if not isinstance(default, self.datatype):

                # Try to convert it to the expected type
                try:
                    default = self.datatype(default)
                except Exception as e:
                    msg = f"Resource {self.id}: Default value {self.default} ({str(type(self.default))}) cannot be converted to expected type {self.datatype}\n{str(e)}" # noqa
                    raise ResourceConfigurationException(msg)

            # Attach the value to this object
            self.default = default

        # If no value is provided
        else:

            # Set up an empty instance of the datatype
            self.default = self.datatype()

    def _setup_attributes(self, id, label, help):

        # Save the id and default value for this particular resource
        self.id = id

        # If no label is provided, default to the id
        self.label = id if label == "" else label
        self.help = None if help == "" else help

    def _setup_extra(self):
        """If any extra setup behavior is needed, invoke it here."""
        pass

    def user_input(self, widget_data):
        """
        Method used to provide the option for user input from the GUI.
        Should be overridden by each specific resource.
        """
        pass

    def cli(self):
        """
        Method used to provide the option for user input from the command line.
        Should be overridden by each specific resource.
        """
        pass

    def native(self, d):
        """
        Return a native python representation of a value of this resource.
        While this base method is extremely simple, it can be overridden
        by resource types with more complex serialization.
        """

        return d

    def source(self, default, indent=4):
        """Return the code used to recreate this resource."""
        spacer = "".join([" " for _ in range(indent)])

        # Get the signature of the initialization function
        sig = signature(self.__class__.__init__)

        # Build up the parameters to use to invoke the object
        params = {}

        for kw in sig.parameters.keys():
            if kw == "self":
                continue
            if kw == "default":
                params[kw] = self.native(default)
            else:
                params[kw] = self.__dict__[kw]

        # Format the params as a string
        params_str = f',\n{spacer}{spacer}{spacer}'.join([
            f"{kw}={source_val(val)}"
            for kw, val in params.items()
        ])

        return f"{self.__class__.__name__}(\n{spacer}{spacer}{spacer}{params_str}\n{spacer}{spacer})" # noqa
