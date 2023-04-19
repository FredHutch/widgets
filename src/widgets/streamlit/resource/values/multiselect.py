from typing import Any, List
import numpy as np
from widgets.base.exceptions import WidgetFunctionException
from widgets.base.helpers import compress_json, decompress_json
from widgets.st_base.value import StValue


class StMultiSelect(StValue):
    """
    Multi-select resource used for Streamlit-based widgets.
    """

    value: List[Any] = None
    options: List[Any] = []

    def __init__(
        self,
        id=None,
        value: list = [],
        label=None,
        help=None,
        disabled: bool = False,
        label_visibility: str = "visible",
        options: list = [],
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
            options (list):     List of options to select from.
            value (list):       (optional) The starting value(s)
            disabled (bool):    (optional) If True, the input element is
                                disabled (default: False)
            label_visibility:   (optional) The visibility of the label.
                                If "hidden", the label doesn't show but there
                                is still empty space for it above the widget
                                (equivalent to label=None). If "collapsed",
                                both the label and the space are removed.
                                Default is "visible".
            index (int):        The index of the preselected option on first
                                render.
            sidebar (bool):     Set up UI in the sidebar vs. the main container


        Returns:
            StMultiSelect: The instantiated resource object.
        """

        # Parse the provided value or options, converting from a
        # gzip-compressed string if necessary
        options = decompress_json(options)
        value = decompress_json(value)

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            disabled=disabled,
            label_visibility=label_visibility,
            options=options,
            sidebar=sidebar,
            **kwargs
        )

    def run_self(self):
        """
        Read in the selected value(s) from the user.
        """

        # Increment the UI revision
        self.revision += 1

        if not all([i in self.options for i in self.value]):
            msg = f"Default value for {self.id} does not exist in options"
            msg = f"{msg} ({self.value}, {self.options})"
            raise WidgetFunctionException(msg)

        # Update the input element
        self.ui_container().multiselect(
            self.label,
            options=self.options,
            default=self.value,
            on_change=self.on_change,
            key=self.key(),
            help=self.help,
            label_visibility=self.label_visibility,
            disabled=self.disabled
        )

        self.on_change()

    def _source_val(self, val, **kwargs):
        """
        Use gzip encoding for any list elements
        """

        if isinstance(val, np.ndarray):
            val = list(val)
        if isinstance(val, list):
            return compress_json(val)
        else:
            return super()._source_val(val, **kwargs)
