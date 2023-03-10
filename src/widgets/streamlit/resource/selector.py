from typing import List
from widgets.streamlit.resource.base import StResource
from widgets.streamlit.resource.value import StSelectString
from widgets.base.exceptions import ResourceConfigurationException


class StSelector(StResource):
    """
    Present a drop-down menu to the user, and only show the child
    element which they select (based on the label).
    """

    def __init__(
        self,
        id="selector",
        label="Select Resource",
        options: List[StResource] = None
    ):

        # The user must have provided a list of Resources to select from
        if options is None:
            msg = f"Selector must have options provided ({id})"
            raise ResourceConfigurationException(msg)

        if not isinstance(options, list):
            msg = f"Selector options must be a list ({id})"
            raise ResourceConfigurationException(msg)

        if any([isinstance(i, StResource) is False for i in options]):
            msg = f"Selector options must be a list of Resources ({id})"
            raise ResourceConfigurationException(msg)

        label_list = [r.label for r in options]

        # The labels must all be unique
        if len(set(label_list)) < len(options):
            msg = "Selector options must have unique labels"
            raise ResourceConfigurationException(msg)

        # The value is the label of the first one
        value = options[0].label

        super().__init__(
            id=id,
            value=value,
            children=[
                StSelectString(
                    id='_selector_menu',
                    label=label,
                    options=label_list,
                    value=value
                )
            ] + options
        )

    def run_children(self, **kwargs) -> None:
        """Only run the selected child element."""

        for ix, r in enumerate(self.children):
            if ix == 0 or r.label == self.get(['_selector_menu']):
                r.run(**kwargs)
