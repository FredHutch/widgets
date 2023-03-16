import streamlit as st
from typing import List, Type, Union
from widgets.base.exceptions import ResourceConfigurationException
import widgets.streamlit as wist


class StDuplicator(wist.StResource):
    """
    Wrapper element which will show/hide the elements in a list
    of Resources.

    To initialize the list of elements, either:

        1) The class to initialize:
            init_class: The class which should be invoked, and
            init_n:     The number of elements which should be made

        or

        2) The list of elements directly:
            children:   The list of elements which will be shown/hidden

    The `value` attribute of the StDuplicator element is a list
    of booleans which is the same length as the `children`.

    Show / Hide behavior:

    The user will be presented with one or more buttons which will
    show or hide an element in the list of children.
    The presence of each button is controlled by a boolean flag
    attribute of the StDuplicator resource.

    end_button:     Show a button after the last visible element
                    which will show the next element.
                    If no elements are visible, it will be shown
                    for the first element in the list.
    middle_button:  Show a button for every hidden element which
                    is located before a visible element.
    hide_button:    Show a button to hide any visible element.

    Note, if any of these boolean flags are provided instead as
    a list of bools, then the presence of each flag will be predicated
    on a True value at the corresponding position in that list.
    """

    init_class: Union[Type[wist.StResource], None] = None
    init_n: int = None

    end_button: Union[bool, List[bool]]
    middle_button: Union[bool, List[bool]]
    hide_button: Union[bool, List[bool]]
    remove_label = "Remove"
    add_label = "Add"

    def __init__(
        self,
        id="resource",
        value: Union[None, List[bool]] = None,
        children: Union[None, List[wist.StResource]] = None,
        label=None,
        help=None,
        init_class: Union[Type[wist.StResource], None] = None,
        init_n: int = None,
        end_button: Union[bool, List[bool]] = True,
        middle_button: Union[bool, List[bool]] = False,
        hide_button: Union[bool, List[bool]] = True,
        remove_label="Remove",
        add_label="Add"
    ):

        # If a list of children was not provided
        if children is None:

            if not isinstance(init_n, int):
                msg = f"init_n must be an int, not {type(init_n)}"
                raise ResourceConfigurationException(msg)

            # Set up the list of children
            children = [
                self._init_element(init_class, i)
                for i in range(init_n)
            ]

        else:

            if not isinstance(children, list):
                raise ResourceConfigurationException("children must be a list")

        # If the value was already provided
        if value is not None:

            # Make sure that it is a list of bools
            # with the same length as children
            self._assert_bool_list(value, 'value')

        # If no value was provided
        else:

            # Initialize the values
            value = [False for _ in children]

        # For each of the button elements
        for attr, attr_lab in [
            (end_button, 'end_button'),
            (middle_button, 'middle_button'),
            (hide_button, 'hide_button')
        ]:

            # If it is not a bool
            if not isinstance(attr, bool):

                # Make sure it is a list of bools
                self._assert_bool_list(attr, attr_lab)

        # Initialize the class
        super().__init__(
            id=id,
            value=value,
            children=children,
            label=label,
            help=help,
            init_class=init_class,
            init_n=init_n,
            end_button=end_button,
            middle_button=middle_button,
            hide_button=hide_button,
            remove_label=remove_label,
            add_label=add_label,
        )

    def _assert_bool_list(self, attr, attr_lab):

        # It must be a list of bools
        if not isinstance(attr, list):
            msg = f"{attr_lab} must be a list of bools, not {type(attr)}"
            raise ResourceConfigurationException(msg)

        for i in attr:
            if not isinstance(i, bool):
                msg = f"Elements in the {attr_lab} list must be bools, not {i}"
                raise ResourceConfigurationException(msg)

    def _init_element(self, init_class, ix: int):
        """Initialize an object from the provided class."""

        try:
            obj = init_class(
                id=f"resource_{ix}"
            )
        except Exception as e:
            msg = f"init_class must be a callable class: {str(e)}"
            raise ResourceConfigurationException(msg)

        return obj

    def run_children(self, **kwargs) -> None:
        """
        Run the .run() method for each child Resource only if the
        corresponding element in the self.value list is True.
        """

        # Add the value to the session state
        if st.session_state.get(self.key()) is None:
            st.session_state[self.key()] = self.value
        else:
            self.value = st.session_state[self.key()]

        for ix, resource in enumerate(self.children):

            # If it is enabled (shown)
            if self.value[ix]:

                # Run the element
                resource.run(**kwargs)

                # Show the hide button if it is enabled
                self._hide_button(ix)

            # If it is hidden
            else:

                # Show the show button if it is enabled
                self._show_button(ix)

    def _hide_button(self, ix):
        """Deploy the hide button if it is enabled."""

        # If the hide button is disabled, take no action
        if isinstance(self.hide_button, bool):
            if not self.hide_button:
                return
        else:
            if not self.hide_button[ix]:
                return

        col1, col2, col3 = self.main_container.columns(3)
        col2.button(
            label=self.remove_label,
            key=f"{self.key()}_hide_{ix}",
            on_click=self._toggle_element,
            args=(ix,),
            use_container_width=True
        )

    def _show_button(self, ix):
        """Deploy the show button if it is enabled."""

        # If this is at the end of the visible elements
        if self._is_end(ix):

            # If the end button is disabled, take no action
            if isinstance(self.end_button, bool):
                if not self.end_button:
                    return
            else:
                if not self.end_button[ix]:
                    return

        # If this is in the middle of the visible elements
        elif self._is_middle(ix):

            # If the middle button is disabled, take no action
            if isinstance(self.middle_button, bool):
                if not self.middle_button:
                    return
            else:
                if not self.middle_button[ix]:
                    return

        # If it is not at the end or in the middle
        else:

            # Take no action
            return

        # Implicitly, the middle/end button is enabled
        # and this position is in the middel/end
        col1, col2, col3 = self.main_container.columns(3)
        col2.button(
            label=self.add_label,
            key=f"{self.key()}_add_{ix}",
            on_click=self._toggle_element,
            args=(ix,),
            use_container_width=True
        )

    def _final_ix(self):
        """
        Return the final index position of a shown element.
        If no elements are shown, return -1.
        """
        final_ix = -1
        for i, b in enumerate(self.value):
            if b:
                final_ix = i
        return final_ix

    def _is_end(self, ix):
        """Bool: ix is immediately after the final shown element."""

        return ix == (self._final_ix() + 1)

    def _is_middle(self, ix):
        """Bool: ix is before the final shown element."""

        return ix < self._final_ix()

    def _toggle_element(self, ix):
        """Toggle the show/hide status of an element."""

        st.session_state[self.key()][ix] = not st.session_state[self.key()][ix]
        self.value = st.session_state[self.key()]
