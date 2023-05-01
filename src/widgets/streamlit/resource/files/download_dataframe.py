from typing import Union
from widgets.base.exceptions import ResourceConfigurationException
from widgets.streamlit.resource.values.slider import StValue


class StDownloadDataFrame(StValue):
    """Download button for an StDataFrame."""

    index = None

    def __init__(
        self,
        target: Union[str, None] = None,
        label="",
        sidebar=True,
        index=None
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
            value=None,
            index=index
        )

        # Set up the specific attributes for this type of resource
        self.target = target
        self.sidebar = sidebar

    def run_self(self):
        """Give the user a button to download a DataFrame."""

        # Point to the target
        target = self.parent._get_child(self.target)

        # Get the value of the table
        csv = target.value.to_csv(index=self.index)

        self.ui_container().download_button(
            self.label,
            csv,
            file_name=f"{self.target}.csv",
            mime="text/csv",
            help="Download this table as a spreadsheet (csv)"
        )
