from typing import Any, List
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from widgets.base.exceptions import ResourceConfigurationException
from widgets.streamlit.resource.base import StResource


class StValue(StResource):
    """Functions shared across single-value-entry resources."""

    sidebar = True
    disabled = False
    label_visibility = "visible"

    def ui_container(self) -> DeltaGenerator:
        """
        Return the empty element in the sidebar or main container,
        depending on whether the self.sidebar attribute is True.
        """

        return self._get_ui_element(empty=True, sidebar=self.sidebar)


class StString(StValue):
    """String value resource used for Streamlit-based widgets."""

    value: str = None
    max_chars: int = None
    type = "default"
    autocomplete = None
    placeholder = None

    def __init__(
        self,
        id="",
        value=None,
        label="",
        help="",
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
            value (int):        (optional) The starting value.
            disabled (bool):    (optional) If True, the input element is
                                disabled (default: False)
            label_visibility:   (optional) The visibility of the label.
                                If "hidden", the label doesn't show but there
                                is still empty space for
                                it above the widget (equivalent to label="").
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
            **kwargs
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.max_chars = max_chars
        self.type = type
        self.autocomplete = autocomplete
        self.placeholder = placeholder
        self.sidebar = sidebar

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


class StInteger(StValue):
    """Integer value resource used for Streamlit-based widgets."""

    value = 0
    min_value: int = None
    max_value: int = None
    step: int = 1
    format: str = "%d"

    def __init__(
        self,
        id="",
        value=0,
        label="",
        help="",
        disabled: bool = False,
        label_visibility: str = "visible",
        min_value: int = None,
        max_value: int = None,
        step: int = 1,
        format: str = "%d",
        sidebar=True,
        **kwargs
    ):
        """
        Args:
            id (str):           The unique key for the resource.
            label (str):        (optional) Label used for user input display
                                elements
            help (str):         (optional) Help text used for user input
                                display elements
            value (int):        (optional) The starting value.
            disabled (bool):    (optional) If True, the input element is
                                disabled (default: False)
            label_visibility:   (optional) The visibility of the label.
                                If "hidden", the label doesn't show but there
                                is still empty space for it above the widget
                                (equivalent to label=""). If "collapsed", both
                                the label and the space are removed.
                                Default is "visible".
            min_value (int):    (optional) The minimum value used for the
                                input element
            max_value (int):    (optional) The maximum value used for the
                                input element
            step (int):         (optional) Step size for input element
            format (str):       (optional) Formatting f-string used for the
                                input element
            sidebar (bool):     Set up UI in the sidebar vs. the main container

        Returns:
            StInteger: The instantiated resource object.
        """

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            **kwargs
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.format = format
        self.sidebar = sidebar

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


class StFloat(StValue):
    """Float value resource used for Streamlit-based widgets."""

    value = 0.0
    min_value: int = None
    max_value: int = None
    step: int = None
    format: str = "%f"

    def __init__(
        self,
        id="",
        value=0.0,
        label="",
        help="",
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
                                (equivalent to label="").
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
            **kwargs
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.format = format
        self.sidebar = sidebar

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


class StSelectString(StValue):
    """
    Select-string-value-from-list resource used for Streamlit-based widgets.
    """

    value: str = None
    options: list = []
    index: int = 0

    def __init__(
        self,
        id="",
        value=None,
        label="",
        help="",
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
                                (equivalent to label=""). If "collapsed", both
                                the label and the space are removed.
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

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            **kwargs
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.options = options
        self.index = index
        self.sidebar = sidebar

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


class StMultiSelect(StValue):
    """
    Multi-select resource used for Streamlit-based widgets.
    """

    value: List[Any] = None
    options: List[Any] = []

    def __init__(
        self,
        id="",
        value: list = [],
        label="",
        help="",
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
                                (equivalent to label=""). If "collapsed", both
                                the label and the space are removed.
                                Default is "visible".
            index (int):        The index of the preselected option on first
                                render.
            sidebar (bool):     Set up UI in the sidebar vs. the main container


        Returns:
            StMultiSelect: The instantiated resource object.
        """

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            **kwargs
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.options = options
        self.sidebar = sidebar

    def run_self(self):
        """
        Read in the selected value(s) from the user.
        """

        # Increment the UI revision
        self.revision += 1

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


class StCheckbox(StValue):
    """Checkbox resource used for Streamlit-based widgets."""

    value = False

    def __init__(
        self,
        id="",
        value=False,
        label="",
        help="",
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
            **kwargs
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.sidebar = sidebar

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


class StSlider(StValue):
    """Slider resource used for Streamlit-based widgets."""

    value = False
    min_value: float = None
    max_value: float = None
    step: float = 1
    format: str = "%.2f"

    def __init__(
        self,
        id="",
        value=False,
        label="",
        help="",
        disabled: bool = False,
        label_visibility: str = "visible",
        min_value: float = None,
        max_value: float = None,
        step: float = 1,
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
            value (bool):       (optional) The starting value.
            disabled (bool):    (optional) If True, the input element is
                                disabled (default: False)
            label_visibility:   (optional) The visibility of the label.
                                If "hidden", the label doesn't show but there
                                is still empty space for it above the widget
                                (equivalent to label="").
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
            StSlider: The instantiated resource object.
        """

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            **kwargs
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.format = format
        self.sidebar = sidebar

    def run_self(self):
        """
        Read in the value from the user.
        """

        # Increment the UI revision
        self.revision += 1

        # Update the input element
        self.ui_container().slider(
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
