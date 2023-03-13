from typing import Union
import streamlit as st
import pandas as pd
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.helpers import parse_dataframe_string
from widgets.base.helpers import encode_dataframe_string
from widgets.streamlit.resource.value import StValue


class StDataFrame(StValue):
    """DataFrame resource used in a Streamlit-based widget."""

    value = pd.DataFrame()
    sep = ","
    show_uploader = True

    def __init__(
        self,
        id=None,
        value=None,
        label=None,
        help: Union[str, None] = None,
        disabled: bool = False,
        label_visibility: str = "visible",
        sep=",",
        sidebar=True,
        show_uploader=True,
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
                            Default is "visible"
            sidebar (bool): Set up UI in the sidebar vs. the main container
            show_uploader:  Show / hide the uploader element

        Returns:
            StResource:     The instantiated resource object.
        """

        # Parse the provided value, converting from a gzip-compressed
        # string if necessary
        value = parse_dataframe_string(value)

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
        self.sidebar = sidebar
        self.show_uploader = show_uploader

    def run_self(self):
        """Allow the user to provide their own DataFrame from a file."""

        # If the uploader element has been enabled
        if self.show_uploader:

            # Increment the UI revision
            self.revision += 1

            # Update the input element
            self.ui_container().file_uploader(
                self.label,
                accept_multiple_files=False,
                help=self.help,
                key=self.key(),
                disabled=self.disabled,
                label_visibility=self.label_visibility
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
        That dict of list will be serialized to JSON and compressed
        with zlib to reduce the total file size.
        """

        if isinstance(val, str):
            return f'"{val}"'
        elif isinstance(val, pd.DataFrame):
            return encode_dataframe_string(val)

        else:
            return val


class StDownloadDataFrame(StValue):
    """Download button for an StDataFrame."""

    def __init__(
        self,
        target: Union[str, None] = None,
        label="",
        sidebar=True
    ):
        """
        Args:
            target (str):   The id of the StDataFrame to be downloaded.
            label (str):    (optional) Label used for download button.
            sidebar (bool): Set up UI in the sidebar vs. the main container

        Returns:
            StResource:     The instantiated resource object.
        """

        if target is None:
            raise ResourceConfigurationException("Must provide target")

        # Set up the id based on the target
        id = f"download_{target}"

        # Default behavior for the label
        if len(label) == 0:
            label = f"Download {target.title()}"

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help="",
            value=None
        )

        # Set up the specific attributes for this type of resource
        self.target = target
        self.sidebar = sidebar

    def run_self(self):
        """Give the user a button to download a DataFrame."""

        # Point to the target
        target = self.parent._get_child(self.target)

        # Get the value of the table
        csv = target.value.to_csv(index=None)

        self.ui_container().download_button(
            self.label,
            csv,
            file_name=f"{self.target}.csv",
            mime="text/csv",
            help="Download this table as a spreadsheet (csv)"
        )
