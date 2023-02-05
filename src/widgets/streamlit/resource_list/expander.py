from typing import List
from streamlit.delta_generator import DeltaGenerator
from widgets.base.resource import Resource
from widgets.streamlit.resource_list.base import StResourceList


class StExpander(StResourceList):
    """List of resources wrapped in an expand/collapse element."""

    expanded = False

    def __init__(
        self,
        id="root",
        resources: List[Resource] = [],
        label="",
        help="",
        expanded=False,
        **kwargs
    ) -> None:
        """
        Set up the StExpander object
        """

        # Set up the core attributes of the ResourceList
        super().__init__(
            id=id,
            resources=resources,
            label=label,
            help=help,
            expanded=expanded,
            **kwargs
        )

    def customize_container(self, container: DeltaGenerator) -> DeltaGenerator:
        """
        Instantiate a expand/collapse container
        """

        # Make sure that no parent elements are also expanders
        if self.parent is not None:

            self.parent._assert_isinstance(
                self.__class__,
                case=False,
                parent=True
            )

        return container.expander(self.label, expanded=self.expanded)
