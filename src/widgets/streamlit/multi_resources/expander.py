from typing import List
from widgets.streamlit.resources.base import StResource


class StExpander(StResource):
    """Resource which contains other resources within an expander element."""

    resouces: List[StResource] = []

    def __init__(
        self,
        id="",
        resources: List[StResource] = [],
        label="",
        help=""
    ):
        """
        Args:
            id (str):           The unique key for the resource.
            resources (list):   List of Resources included in the expander.
            label (str):        (optional) Label used for user input
                                display elements
            help (str):         (optional) Help text used for user input
                                display elements
        """

        pass
