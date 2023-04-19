from widgets.base.exceptions import ResourceConfigurationException
from widgets.st_base.value import StValue


class StFloat(StValue):
    """Float value resource used for Streamlit-based widgets."""

    value = 0.0
    min_value: int = None
    max_value: int = None
    step: int = None
    format: str = "%f"

    def __init__(
        self,
        id=None,
        value=0.0,
        label=None,
        help=None,
        disabled: bool = False,
        label_visibility: str = "visible",
        min_value: int = None,
        max_value: int = None,
        step: int = None,
        format: str = "%f",
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
            value (float):      (optional) The starting value.
            disabled (bool):    (optional) If True, the input element is
                                disabled (default: False)
            label_visibility:   (optional) The visibility of the label.
                                If "hidden", the label doesn't show but there
                                is still empty space for it above the widget
                                (equivalent to label=None).
                                If "collapsed", both the label and the space
                                are removed. Default is "visible".
            min_value (int):    (optional) The minimum value used for the
                                input element
            max_value (int):    (optional) The maximum value used for the
                                input element
            step (int):         (optional) Step size for input element
            format (str):       (optional) Formatting f-string used for the
                                input element
            sidebar (bool):     Set up UI in the sidebar vs. the main container

        Returns:
            StFloat: The instantiated resource object.
        """

        if not isinstance(value, float):
            raise ResourceConfigurationException("value must be a float")

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            disabled=disabled,
            label_visibility=label_visibility,
            min_value=min_value,
            max_value=max_value,
            step=step,
            format=format,
            sidebar=sidebar,
            **kwargs
        )

    def run_self(self):
        """
        Read in the integer value from the user.
        """

        # Increment the UI revision
        self.revision += 1

        # Update the input element
        self.ui_container().number_input(
            self.label,
            on_change=self.on_change,
            value=self.value,
            key=self.key(),
            help=self.help,
            min_value=self.min_value,
            max_value=self.max_value,
            step=self.step,
            format=self.format,
            label_visibility=self.label_visibility,
            disabled=self.disabled
        )

        self.on_change()
