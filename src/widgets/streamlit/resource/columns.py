from streamlit.delta_generator import DeltaGenerator
from typing import List, Union
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.resource import Resource
from widgets.st_base.resource import StResource


class StColumns(StResource):
    """List of resources laid out in columns."""

    spec: Union[List[int], int] = None
    sidebar = True
    gap = "small"
    main_columns: List[DeltaGenerator] = []
    sidebar_columns: List[DeltaGenerator] = []

    def __init__(
        self,
        id="columns",
        children: List[Resource] = [],
        spec=None,
        sidebar=True,
        gap="small",
        disable_sidebar=False,
        **kwargs
    ) -> None:
        """
        Set up the StColumns object
        """

        # If no spec has been provided, or if an integer was provided
        if spec is None or isinstance(spec, int):

            # Just use the number of children provided
            spec = len(children)

        # If a spec has been provided
        else:

            # It must be a list
            if not isinstance(spec, list):
                msg = f"StColumns: spec must be a list, not {spec}"
                raise ResourceConfigurationException(msg)

            # Make sure that each element in the list is an int
            for i in spec:
                if not isinstance(i, int):
                    msg = f"StColumns: spec elements must be int, not {i}"
                    raise ResourceConfigurationException(msg)

            # The length must match the number of children
            if len(spec) != len(children):
                msg = "StColumns: spec length must match children"
                raise ResourceConfigurationException(msg)

        if gap not in ["small", "medium", "large"]:
            msg = "StColumns: gap must be one of small, medium, large"
            raise ResourceConfigurationException(msg)

        # Disable the sidebar for all child elements IF the sidebar flag is set to False
        kwargs["disable_sidebar"] = not sidebar

        # Set up the core attributes of the StResource
        super().__init__(
            id=id,
            children=children,
            label="",
            help="",
            spec=spec,
            gap=gap,
            sidebar=sidebar,
            **kwargs
        )

    def prep(self) -> None:
        """
        Instantiate a column container and place the children
        in those containers.
        """

        # Instantiate the base container elements
        super().prep()

        # Set up the columns
        self.main_columns = self.main_empty.columns(
            self.spec, gap=self.gap
        )
        if not self.disable_sidebar:
            self.sidebar_columns = self.sidebar_empty.columns(
                self.spec, gap=self.gap
            )

        # Set up the children within those containers
        for ix, child in enumerate(self.children):
            child.main_empty = self.main_columns[ix].empty()
            if not self.disable_sidebar:
                child.sidebar_empty = self.sidebar_columns[ix].empty()
