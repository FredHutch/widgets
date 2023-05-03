from copy import deepcopy
from typing import List, Union
from widgets.st_base.resource import StResource
from widgets.streamlit.resource.values.selectstring import StSelectString
from widgets.base.exceptions import ResourceConfigurationException


class StSelector(StResource):
    """
    Present a drop-down menu to the user, and only show the child
    element which they select (based on the label).
    """

    options = []

    def __init__(
        self,
        id="selector",
        label="Select Resource",
        options: List[StResource] = None,
        value: Union[str, None] = None,
        disable_sidebar=False,
        **kwargs
    ):

        # The user must have provided a list of Resources to select from
        if options is None:
            if self.__class__.options is None:
                msg = f"Selector must have options provided ({id})"
                raise ResourceConfigurationException(msg)
            else:
                options = deepcopy(self.__class__.options)

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

        # Attach the options
        self.options = options

        # If no value was provided
        if value is None and len(self.options) > 0:

            # The value is the label of the first one
            value = options[0].label

        # If a value was provided
        else:

            # Make a list of the labels for the options
            option_labels = [o.label for o in options]

            # Make sure that it is in the list of options
            if value not in option_labels:
                options_str = ", ".join(option_labels)
                msg = f"value ({value}) not in options ({options_str})"
                raise ResourceConfigurationException(msg)

        super().__init__(
            id=id,
            value=value,
            label=label,
            children=[
                StSelectString(
                    id='_selector_menu',
                    label=label,
                    options=label_list,
                    value=value
                )
            ] + options,
            disable_sidebar=disable_sidebar,
            **kwargs
        )

    def all_values(self, path=[], flatten=False, **kwargs) -> dict:
        """
        Return the .all_values() call of the child resource
        which is currently selected.
        """

        for r in self.children:
            if r.label == self.get(['_selector_menu']):
                return r.all_values(
                    path=path,
                    flatten=flatten,
                    **kwargs
                )

    def set_value(self, val, **kwargs) -> None:
        """Set the value of the selector menu."""

        self._get_child("_selector_menu").set_value(val, **kwargs)

    def get_value(self, **kwargs) -> str:
        """Get the value of the selector menu."""

        return self._get_child("_selector_menu").get_value(**kwargs)

    def run_children(self, **kwargs) -> None:
        """Only run the selected child element."""

        for ix, r in enumerate(self.children):
            if ix == 0 or r.label == self.get_value():
                r.run(**kwargs)
