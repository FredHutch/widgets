from streamlit.delta_generator import DeltaGenerator
from widgets.streamlit.resource_list import StResourceList


class StExpander(StResourceList):
    """List of resources wrapped in an expand/collapse element."""

    expanded = False

    def customize_container(self, container: DeltaGenerator) -> DeltaGenerator:
        """
        Instantiate a expand/collapse container
        """
        return container.expander(self.label, expanded=self.expanded)
