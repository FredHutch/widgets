import streamlit as st
from widgets.base.resource import Resource
from widgets.base.exceptions import ResourceConfigurationException


class StString(Resource):
    """String value resource used for Streamlit-based widgets."""

    datatype = str
    max_chars: int = None
    type = "default"
    autocomplete = None
    placeholder = None

    def __init__(
        self,
        id="",
        default=None,
        label="",
        help="",
        disabled: bool = False,
        label_visibility: str = "visible",
        max_chars: int = None,
        type: str = "default",
        autocomplete=None,
        placeholder: str = None
    ):
        """
        Args:
            id (str):           The unique key used to store the resource in
                                the widget `data` object.
            label (str):        (optional) Label used for user input
                                display elements
            help (str):         (optional) Help text used for user input
                                display elements
            default (int):      (optional) The default float, used if no saved
                                value is present.
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

        Returns:
            Resource: The instantiated resource object.
        """

        # Set up the resource attributes
        self.setup(
            id=id,
            label=label,
            help=help,
            default=default
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.max_chars = max_chars
        self.type = type
        self.autocomplete = autocomplete
        self.placeholder = placeholder

    def user_input(self, widget_data: dict = {}):
        """
        Read in the string value from the user.
        """

        if not self.disabled:
            with st.sidebar:
                widget_data[self.id] = st.text_input(
                    self.label,
                    value=widget_data.get(self.id),
                    key=self.id,
                    help=self.help,
                    max_chars=self.max_chars,
                    type=self.type,
                    autocomplete=self.autocomplete,
                    placeholder=self.placeholder,
                    disabled=self.disabled,
                    label_visibility=self.label_visibility,
                )


class StInteger(Resource):
    """Integer value resource used for Streamlit-based widgets."""

    datatype = int
    disabled: bool = False
    label_visibility: str = "visible"
    min_value: int = None
    max_value: int = None
    step: int = 1
    format: str = "%d"

    def __init__(
        self,
        id="",
        default=None,
        label="",
        help="",
        disabled: bool = False,
        label_visibility: str = "visible",
        min_value: int = None,
        max_value: int = None,
        step: int = 1,
        format: str = "%d",
    ):
        """
        Args:
            id (str):           The unique key used to store the resource in
                                the widget `data` object.
            label (str):        (optional) Label used for user input display
                                elements
            help (str):         (optional) Help text used for user input
                                display elements
            default (int):      (optional) The default integer, used if no
                                saved value is present.
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

        Returns:
            Resource: The instantiated resource object.
        """

        # Set up the resource attributes
        self.setup(
            id=id,
            label=label,
            help=help,
            default=default
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.format = format

    def user_input(self, widget_data: dict):
        """
        Read in the integer value from the user.
        """

        if not self.disabled:
            with st.sidebar:
                widget_data[self.id] = self.datatype(
                    st.number_input(
                        self.label,
                        value=widget_data.get(self.id),
                        key=self.id,
                        help=self.help,
                        min_value=self.min_value,
                        max_value=self.max_value,
                        step=self.step,
                        format=self.format,
                        label_visibility=self.label_visibility,
                    )
                )


class StFloat(Resource):
    """Integer value resource used for Streamlit-based widgets."""

    datatype = float
    disabled: bool = False
    label_visibility: str = "visible"
    min_value: int = None
    max_value: int = None
    step: int = None
    format: str = "%f"

    def __init__(
        self,
        id="",
        default=None,
        label="",
        help="",
        disabled: bool = False,
        label_visibility: str = "visible",
        min_value: int = None,
        max_value: int = None,
        step: int = None,
        format: str = "%f",
    ):
        """
        Args:
            id (str):           The unique key used to store the resource in
                                the widget `data` object.
            label (str):        (optional) Label used for user input
                                display elements
            help (str):         (optional) Help text used for user input
                                display elements
            default (int):      (optional) The default float, used if no saved
                                value is present.
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

        Returns:
            Resource: The instantiated resource object.
        """

        # Set up the resource attributes
        self.setup(
            id=id,
            label=label,
            help=help,
            default=default
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.format = format

    def user_input(self, widget_data: dict = {}):
        """
        Read in the integer value from the user.
        """

        if not self.disabled:
            with st.sidebar:
                widget_data[self.id] = self.datatype(
                    st.number_input(
                        self.label,
                        value=widget_data.get(self.id),
                        key=self.id,
                        help=self.help,
                        min_value=self.min_value,
                        max_value=self.max_value,
                        step=self.step,
                        format=self.format,
                        label_visibility=self.label_visibility,
                    )
                )


class StSelectString(Resource):
    """
    Select-string-value-from-list resource used for Streamlit-based widgets.
    """

    datatype = str
    disabled: bool = False
    label_visibility: str = "visible"
    options: list = []
    index: int = 0

    def __init__(
        self,
        id="",
        default=None,
        label="",
        help="",
        disabled: bool = False,
        label_visibility: str = "visible",
        options: list = [],
        index: int = 0
    ):
        """
        Args:
            id (str):           The unique key used to store the resource in
                                the widget `data` object.
            label (str):        (optional) Label used for user input
                                display elements
            help (str):         (optional) Help text used for user input
                                display elements
            default (int):      (optional) The default float, used if no saved
                                 value is present.
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

            Note:
            The default value may be defined either using the index position
            or the default value.
            The default value will override the index value if they happen
            to differ.

        Returns:
            Resource: The instantiated resource object.
        """

        # Set up the resource attributes
        self.setup(
            id=id,
            label=label,
            help=help,
            default=default
        )

        # Set up the specific attributes for this type of resource
        self.disabled = disabled
        self.label_visibility = label_visibility
        self.options = options
        self.index = index

    def _setup_extra(self):
        """
        The default values for this resource need to be set up in a different
        way than the other resources.
        The streamlit selectbox input element sets up the default value by
        indicating which index position in the list of options to use.
        To set up the default, we need to (1) make sure that the default value
        is in the list of options, and (2) set the index variable to the
        position of that element.
        """

        # There must be a list of options provided
        if self.options is None or not isinstance(self.options, list):
            msg = f"Resource {self.id} must have a list of options defined"
            raise ResourceConfigurationException(msg)

        # That list must contain elements
        if len(self.options) == 0:
            msg = f"Resource {self.id} options may not be empty"
            raise ResourceConfigurationException(msg)

        # If there is no default option set
        if self.default is None:

            # There must be an index defined
            if self.index is None or not isinstance(self.index, int):
                msg = f"Resource {self.id} must have an index defined"
                raise ResourceConfigurationException(msg)

            # The index must be a valid indeger
            if self.index < 0 or self.index >= len(self.options):
                msg = f"Resource {self.id} must have an index defined in the valid range" # noqa
                raise ResourceConfigurationException(msg)

            # Set the default using the index position from the list
            self.default = self.options[self.index]

        # The default element must be present in the list of options
        if self.default not in self.options:
            msg = f"Default {self.default} not found in list of options: {', '.join(self.options)}" # noqa
            raise ResourceConfigurationException(msg)

        # Set the index position of the default element
        self.index = self.options.index(self.default)

    def user_input(self, widget_data: dict = {}):
        """
        Read in the integer value from the user.
        """

        # Start with the default value
        widget_data[self.id] = self.default

        # Reset the index value
        self._setup_extra()

        if not self.disabled:
            with st.sidebar:
                widget_data[self.id] = st.selectbox(
                    self.label,
                    options=self.options,
                    key=self.id,
                    help=self.help,
                    label_visibility=self.label_visibility,
                )
