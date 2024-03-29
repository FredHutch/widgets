from typing import List
from widgets.base.resource import Resource
from widgets.st_base.resource import StResource


class StExpander(StResource):
    """List of resources wrapped in an expand/collapse element."""

    expanded = False
    sidebar = True

    def __init__(
        self,
        id="expander",
        children: List[Resource] = [],
        label=None,
        help=None,
        expanded=False,
        sidebar=True,
        **kwargs
    ) -> None:
        """
        Set up the StExpander object
        """

        # Disable the sidebar for all child elements
        # IF the sidebar flag is set to False
        kwargs["disable_sidebar"] = not sidebar

        # Set up the core attributes of the StResource
        super().__init__(
            id=id,
            children=children,
            label=label,
            help=help,
            expanded=expanded,
            sidebar=sidebar,
            **kwargs
        )

    def prep(self) -> None:
        """
        Instantiate a expand/collapse container
        """

        # Instantiate the base container elements
        super().prep()

        if self.sidebar and not self.disable_sidebar:
            self.sidebar_container = self.sidebar_empty.expander(
                self.label,
                expanded=self.expanded
            )
        else:
            self.main_container = self.main_empty.expander(
                self.label,
                expanded=self.expanded
            )
