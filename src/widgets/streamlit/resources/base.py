from widgets.base.exceptions import ResourceConfigurationException


class StreamlitResource:
    """
    Base class for all resources used by Streamlit-based apps.

    Attributes:
            id (str): The unique key used to store the resource in the widget `data` object.
            default: The default value for the resource, used if no saved value is present.
            datatype: The variable type returned by the `load()` method (should match the type of the default value).
    """

    id:str = None
    default = None
    datatype:type = None

    def __init__(
        self,
        id="",
        default=None,
    ) -> None:
        """
        Args:
            id (str): The unique key used to store the resource in the widget `data` object.
            default: (optional) The default value for the resource, used if no saved value is present.
                    If no default value is provided, then self.datatype() will be used.
        
        Returns:
            StreamlitResource: The instantiated resource object.
        """

        # If no default value is provided
        if default is None:

            # Make an empty instance of datatype
            default = self.datatype()

        # Make sure that the default value conforms to the expected type
        if not isinstance(default, self.datatype):
            msg = f"Default value for resource '{id}' does not match expected type {self.datatype}"
            raise ResourceConfigurationException(msg)
        
        # Save the id and default value for this particular resource
        self.id = id
        self.default = default

    def read(self):
        """
        Method used to return the contents of the resource.
        Should be overridden by each specific resource.
        """
        pass

    def load(self):
        """
        Returns:
            self.datatype: The saved value, or the default value if no value is saved.
        """

        # Read the saved value
        saved_value = self.read()

        # If no value is saved
        if saved_value is None:

            # Return the default value
            return self.default

        else:
            return saved_value