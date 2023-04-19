from widgets.base.exceptions import ResourceConfigurationException
from widgets.st_base.value import StValue


class StCheckbox(StValue):
    """Checkbox resource used for Streamlit-based widgets."""

    value = False

    def __init__(
        self,
        id=None,
        value=False,
        label=None,
        help=None,
        disabled: bool = False,
        sidebar=True,
        **kwargs
    ):
        """
        Args:
            id (str):           The unique key for the resource.
            label (str):        (optional) Label used for user input
                                display elements
            help (str):         (optional) Help text used for user input
                                display elements
            value (bool):       (optional) The starting value.
            disabled (bool):    (optional) If True, the input element is
                                disabled (default: False)
            sidebar (bool):     Set up UI in the sidebar vs. the main container

        Returns:
            StCheckbox: The instantiated resource object.
        """

        if not isinstance(value, bool):
            raise ResourceConfigurationException("value must be a bool")

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            disabled=disabled,
            sidebar=sidebar,
            **kwargs
        )

    def run_self(self):
        """
        Read in the bool value from the user.
        """

        # Increment the UI revision
        self.revision += 1

        # Update the input element
        self.ui_container().checkbox(
            self.label,
            on_change=self.on_change,
            value=self.value,
            key=self.key(),
            help=self.help,
            disabled=self.disabled
        )

        self.on_change()
