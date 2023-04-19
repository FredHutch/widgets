from widgets.st_base.value import StValue


class StString(StValue):
    """String value resource used for Streamlit-based widgets."""

    value: str = None
    max_chars: int = None
    type = "default"
    autocomplete = None
    placeholder = None

    def __init__(
        self,
        id=None,
        value=None,
        label=None,
        help=None,
        disabled: bool = False,
        label_visibility: str = "visible",
        max_chars: int = None,
        type: str = "default",
        autocomplete=None,
        placeholder: str = None,
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
            value (str):        (optional) The starting value.
            disabled (bool):    (optional) If True, the input element is
                                disabled (default: False)
            label_visibility:   (optional) The visibility of the label.
                                If "hidden", the label doesn't show but there
                                is still empty space for
                                it above the widget (equivalent to label=None).
                                If "collapsed", both the label and the space
                                are removed. Default is "visible".
            max_chars (int):    (optional) Max number of characters allowed in
                                text input
            type (str):         (optional) The type of the text input.
                                This can be either "default"
                                (for a regular text input), or "password"
                                (for a text input that masks the user's
                                typed value). Defaults to "default".
            autocomplete:       (optional) An optional value that will be
                                passed to the <input> element's autocomplete
                                property.
            placeholder (str):  (optional) An optional string displayed when
                                the text input is empty
            sidebar (bool):     Set up UI in the sidebar vs. the main container

        Returns:
            StString: The instantiated resource object.
        """

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            disabled=disabled,
            label_visibility=label_visibility,
            max_chars=max_chars,
            type=type,
            autocomplete=autocomplete,
            placeholder=placeholder,
            sidebar=sidebar,
            **kwargs
        )

    def run_self(self):
        """
        Read in the string value from the user.
        """

        # Increment the UI revision
        self.revision += 1

        # Update the input element
        self.ui_container().text_input(
            self.label,
            on_change=self.on_change,
            value=self.value,
            key=self.key(),
            help=self.help,
            max_chars=self.max_chars,
            type=self.type,
            autocomplete=self.autocomplete,
            placeholder=self.placeholder,
            disabled=self.disabled,
            label_visibility=self.label_visibility
        )

        self.on_change()
