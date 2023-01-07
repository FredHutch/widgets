from widgets.base.exceptions import ResourceConfigurationException


class Resource:
    """
    Base class for all resources used by widgets.

    Attributes:
            id (str): The unique key used to store the resource in the widget `data` object.
            default: The default value for the resource, used if no saved value is present.
            datatype: The variable type returned by the `load()` method (should match the type of the default value).
            label (str): Label displayed to the user for the resource
            help (str): Help text describing the resource to the user
    """

    id:str = None
    default = None
    datatype:type = None
    label:str = None
    help:str = None

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
        """If a non-null value is provided, assign it to the default attribute for this object."""

        # If a non-null default value is provided
        if default is not None:

            # Make sure that the default value conforms to the expected type
            if not isinstance(default, self.datatype):
                msg = f"Resource {self.id}: Default value {self.default} ({str(type(self.default))}) for  does not match expected type {self.datatype}"
                raise ResourceConfigurationException(msg)

            # Attach the value to this object
            self.default = default

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

    def to_json(self, d):
        """
        Return a JSON-compatible representation of a value of this resource.
        While this base method is extremely simple, it can be overridden
        by resource types with more complex serialization.
        """

        return d