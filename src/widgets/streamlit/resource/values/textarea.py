from typing import Any
from widgets.st_base.value import StValue


class StTextArea(StValue):
    """Text area resource used for Streamlit-based widgets."""

    value: str = ""
    height: int = None
    max_chars: int = None
    placeholder = None

    def __init__(
        self,
        id=None,
        label=None,
        value="",
        height=None,
        max_chars: int = None,
        help=None,
        placeholder: str = None,
        disabled: bool = False,
        label_visibility: str = "visible",
        sidebar=True,
        **kwargs
    ):
        """
        Args:
            id (str):           The unique key for the resource.
            label (str):        (optional) Label used for user input
                                display elements
            value (str):        (optional) The starting value.
            height (int):       (optional) Height of input area in pixels.
            max_chars (int):    (optional) Max number of characters allowed in
                                text input
            help (str):         (optional) Help text used for user input
                                display elements
            placeholder (str):  (optional) An optional string displayed when
                                the text input is empty
            disabled (bool):    (optional) If True, the input element is
                                disabled (default: False)
            label_visibility:   (optional) The visibility of the label.
                                If "hidden", the label doesn't show but there
                                is still empty space for
                                it above the widget (equivalent to label=None).
                                If "collapsed", both the label and the space
                                are removed. Default is "visible".
            sidebar (bool):     Set up UI in the sidebar vs. the main container

        Returns:
            StTextArea: The instantiated resource object.
        """

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            height=height,
            disabled=disabled,
            label_visibility=label_visibility,
            max_chars=max_chars,
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
        self.ui_container().text_area(
            self.label,
            value=self.value,
            height=self.height,
            on_change=self.on_change,
            key=self.key(),
            help=self.help,
            max_chars=self.max_chars,
            placeholder=self.placeholder,
            disabled=self.disabled,
            label_visibility=self.label_visibility
        )

        self.on_change()

    def _source_val(self, val, indent=4) -> Any:
        """Triple quote strings to wrap new lines."""

        if isinstance(val, str):
            return f'"""{val}"""'
        else:
            return super()._source_val(val, indent)
