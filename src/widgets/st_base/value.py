from streamlit.delta_generator import DeltaGenerator
from widgets.st_base.resource import StResource


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
