import streamlit as st
import pandas as pd
from widgets.base.resource import Resource


class StDataFrame(Resource):
    """DataFrame resource used in a Streamlit-based widget."""

    datatype = pd.DataFrame
    disabled: bool = False
    label_visibility: str = "visible"
    sep = ","

    def __init__(
        self,
        id="",
        default=None,
        label="",
        help="",
        disabled: bool = False,
        label_visibility: str = "visible",
        sep=","
    ):
        """
        Args:
            id (str):       The unique key used to store the resource in
                            the widget `data` object.
            label (str):    (optional) Label used for user input display
                            elements
            help (str):     (optional) Help text used for user input display
                            elements
            default:        (optional) The default Pandas DataFrame, used if
                            no saved value is present.
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
        self.sep = sep

    def user_input(self, widget_data: dict):
        """Allow the user to provide their own DataFrame from a file."""

        if not self.disabled:
            with st.sidebar:
                self.uploader = st.file_uploader(
                    self.label,
                    accept_multiple_files=False,
                    key=self.id,
                    help=self.help
                )

                # If no file was uploaded
                if self.uploader is None:

                    # Assign the default, or the value provided at the
                    # time of initialization
                    widget_data[self.id] = self.default

                # If a file was provided
                else:

                    # Read the file as a DataFrame
                    widget_data[self.id] = pd.read_csv(
                        self.uploader,
                        sep=self.sep
                    )

    def native(self, d: pd.DataFrame):
        """Return a native Python representation of the DataFrame."""
        if isinstance(d, pd.DataFrame):
            return d.to_dict(orient="list")
        else:
            return d
