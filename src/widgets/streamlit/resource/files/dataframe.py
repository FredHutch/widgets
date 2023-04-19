from typing import Union
import pandas as pd
from widgets.base.helpers import parse_dataframe_string
from widgets.base.helpers import encode_dataframe_string
from widgets.streamlit.resource.files.base import StFile


class StDataFrame(StFile):
    """DataFrame resource used in a Streamlit-based widget."""

    value = pd.DataFrame()
    kwargs = dict()

    def __init__(
        self,
        id="dataframe",
        value=None,
        label=None,
        help: Union[str, None] = None,
        disabled: bool = False,
        label_visibility: str = "visible",
        kwargs={},
        sidebar=True,
        show_uploader=True
    ):
        """
        Args:
            id (str):       The unique key for the resource.
            label (str):    (optional) Label used for user input display
                            elements.
            help (str):     (optional) Help text used for user input display
                            elements.
            value:          (optional) The starting Pandas DataFrame.
            kwargs (dict):  Additional keyword arguments passed to pd.read_csv.
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
            disabled=disabled,
            label_visibility=label_visibility,
            kwargs=kwargs,
            sidebar=sidebar,
            show_uploader=show_uploader,
            accept_multiple_files=False
        )

    def parse_files(self, files):
        """Parse any tabular data files uploaded by the user."""

        # Read the file as a DataFrame
        self.value = pd.read_csv(
            files,
            **self.kwargs
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
            return super()._source_val(val)
