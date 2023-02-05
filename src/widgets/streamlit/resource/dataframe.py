from typing import Union
import streamlit as st
import pandas as pd
from widgets.base.exceptions import ResourceConfigurationException
from widgets.streamlit.resource.base import StResource


class StDataFrame(StResource):
    """DataFrame resource used in a Streamlit-based widget."""

    value = pd.DataFrame()
    disabled: bool = False
    label_visibility: str = "visible"
    sep = ","

    def __init__(
        self,
        id="",
        value=None,
        label="",
        help: Union[str, None] = None,
        disabled: bool = False,
        label_visibility: str = "visible",
        sep=",",
        **kwargs
    ):
        """
        Args:
            id (str):       The unique key for the resource.
            label (str):    (optional) Label used for user input display
                            elements.
            help (str):     (optional) Help text used for user input display
                            elements.
            value:          (optional) The starting Pandas DataFrame.
            sep (str):      Separator value used when reading from a file
            disabled (bool):  (optional) If True, the input element is
                            disabled (default: False)
            label_visibility: (optional) The visibility of the label.
                            If "hidden", the label doesn't show but there is
                            still empty space for it above the widget
                            (equivalent to label=""). If "collapsed", both
                            the label and the space are removed.
                            Default is "visible".

        Returns:
            StreamlitResource: The instantiated resource object.
        """

        # If the value is a dict, convert it
        if isinstance(value, dict):
            try:
                value = pd.DataFrame(value)
            except Exception as e:
                msg = f"value could not be converted to DataFrame ({str(e)})"
                raise ResourceConfigurationException(msg)
        # If the value is a DataFrame, keep it
        elif isinstance(value, pd.DataFrame):
            pass
        # If the value is None, make an empty DataFrame
        elif value is None:
            value = pd.DataFrame()
        else:
            msg = f"value must be None, dict, or DataFrame, not {type(value)}"
            raise ResourceConfigurationException(msg)

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
        self.sep = sep

    def update_ui(self):
        """Allow the user to provide their own DataFrame from a file."""

        # Increment the UI revision
        self.ui_revision += 1

        # Update the input element
        self.ui.file_uploader(
            self.label,
            accept_multiple_files=False,
            help=self.help,
            key=self.key(),
            disabled=self.disabled
        )

        # If a file was provided
        if st.session_state[self.key()] is not None:

            # Read the file as a DataFrame
            self.value = pd.read_csv(
                st.session_state[self.key()],
                sep=self.sep
            )

    def _source_val(self, val, **kwargs):
        """
        Return a string representation of an attribute value
        which can be used in source code initializing this resource.
        The value attribute is a DataFrame which can be serialized
        as a dict of lists.
        """

        if isinstance(val, str):
            return f'"{val}"'
        elif isinstance(val, pd.DataFrame):
            return val.to_dict(orient="list")
        else:
            return val
