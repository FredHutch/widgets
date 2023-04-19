import streamlit as st
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.helpers import compress_json, decompress_json
from widgets.st_base.value import StValue


class StSelectString(StValue):
    """
    Select-string-value-from-list resource used for Streamlit-based widgets.
    """

    value: str = None
    options: list = []
    index: int = 0

    def __init__(
        self,
        id=None,
        value=None,
        label=None,
        help=None,
        disabled: bool = False,
        label_visibility: str = "visible",
        options: list = [],
        index: int = 0,
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
            value (str):        (optional) The starting value
            disabled (bool):    (optional) If True, the input element is
                                disabled (default: False)
            label_visibility:   (optional) The visibility of the label.
                                If "hidden", the label doesn't show but there
                                is still empty space for it above the widget
                                (equivalent to label=None). If "collapsed",
                                both the label and the space are removed.
                                Default is "visible".
            options (list):     List of options to select from.
            index (int):        The index of the preselected option on first
                                render.
            sidebar (bool):     Set up UI in the sidebar vs. the main container

            Note:
            The value may be defined either using the index position
            or the value attribute.
            The value attribute will override the index value if they happen
            to differ.

        Returns:
            StSelectString: The instantiated resource object.
        """

        # Parse the provided options, converting from a gzip-compressed
        # string if necessary
        options = decompress_json(options)

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            disabled=disabled,
            label_visibility=label_visibility,
            options=options,
            index=index,
            sidebar=sidebar,
            **kwargs
        )

        # Resolve any inconsistencies between value and index
        self._resolve_index()

    def _resolve_index(self):
        """Resolve any inconsistencies between the value and index."""

        # There must be a list of options provided
        if self.options is None or not isinstance(self.options, list):
            msg = f"Resource {self.id} must have a list of options defined"
            raise ResourceConfigurationException(msg)

        # If there is no value attribute provided
        if self.value is None:

            # There must be an index defined
            if self.index is None or not isinstance(self.index, int):
                msg = f"Resource {self.id} must have an index defined"
                raise ResourceConfigurationException(msg)

            # The index must be a valid indeger
            if self.index < 0 or (len(self.options) > 0 and self.index >= len(self.options)): # noqa
                msg = f"Resource {self.id} must have an index defined in the valid range" # noqa
                raise ResourceConfigurationException(msg)

            # Set the value using the index position from the list
            if self.index < len(self.options):
                self.value = self.options[self.index]

        # If the value attribute was provided
        elif self.value is not None:

            # The value must be present in the list of options
            if self.value not in self.options:
                msg = f"Default ({self.value} [{type(self.value)}]) not found in list of options: {', '.join(self.options)}" # noqa
                raise ResourceConfigurationException(msg)

            # Set the index position of the default element
            self.index = self.options.index(self.value)

    def run_self(self):
        """
        Read in the selected string value from the user.
        """

        # Increment the UI revision
        self.revision += 1

        # Make sure to resolve the index
        if self.value not in self.options and len(self.options) > 0:
            self.value = self.options[0]
        self._resolve_index()

        # Update the input element
        self.ui_container().selectbox(
            self.label,
            on_change=self.on_change,
            key=self.key(),
            options=self.options,
            index=self.index,
            help=self.help,
            label_visibility=self.label_visibility,
            disabled=self.disabled
        )

        self.on_change()

    def on_change(self):
        """Function called when the selectbox is changed."""

        # Set the value attribute on the resource
        self.value = st.session_state[self.key()]

        if self.value is not None:
            # Update the starting index position (used in update_ui())
            self.index = self.options.index(self.value)

    def _source_val(self, val, **kwargs):
        """
        Use gzip encoding for any list elements
        """

        if isinstance(val, list):
            return compress_json(val)
        else:
            return super()._source_val(val, **kwargs)
