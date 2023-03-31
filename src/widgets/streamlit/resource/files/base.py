from typing import Union
import streamlit as st
from widgets.streamlit.resource.values.slider import StValue


class StFile(StValue):
    """Base class used for resources based on file uploads."""

    show_uploader = True
    accept_multiple_files = False

    def __init__(
        self,
        id='file',
        value=None,
        label=None,
        help: Union[str, None] = None,
        disabled: bool = False,
        label_visibility: str = "visible",
        sidebar=True,
        show_uploader=True,
        accept_multiple_files=False,
        **kwargs
    ):
        """
        Args:
            id (str):       The unique key for the resource.
            label (str):    (optional) Label used for user input display
                            elements.
            help (str):     (optional) Help text used for user input display
                            elements.
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
            accept_multiple_files:
                            Whether multiple files should be accepted

        Returns:
            StFile:         The instantiated resource object.
        """

        # Set up the resource attributes
        super().__init__(
            id=id,
            label=label,
            help=help,
            value=value,
            disabled=disabled,
            label_visibility=label_visibility,
            sidebar=sidebar,
            show_uploader=show_uploader,
            accept_multiple_files=accept_multiple_files,
            **kwargs
        )

    def run_self(self):
        """Allow the user to provide their own DataFrame from a file."""

        # If the uploader element has been enabled
        if self.show_uploader:

            # Increment the UI revision
            self.revision += 1

            # Update the input element
            self.ui_container().file_uploader(
                self.label,
                accept_multiple_files=self.accept_multiple_files,
                help=self.help,
                key=self.key(),
                disabled=self.disabled,
                label_visibility=self.label_visibility
            )

            # If a file was provided
            if st.session_state[self.key()] is not None:

                # Run the function used to parse the file(s)
                self.parse_files(st.session_state[self.key()])

    def parse_files(self, files):
        """Stub used by derivative classes to parse the file inputs."""
        pass
