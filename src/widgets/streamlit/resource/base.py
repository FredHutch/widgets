from typing import Any, Generator, List, Union
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from widgets.base.exceptions import ResourceExecutionException
from widgets.base.resource import Resource


class StResource(Resource):
    """
    Base class for Streamlit-based resources.
    In the main and sidebar containers of the parent, this Resource
    will set up:
        1. An st.empty() object, which will be used to house
        2. An st.container() object.
    Calling self.reset_container() will replace the contents of
    the top-level st.empty() object with a new container which
    does not contain any elements.
    """

    # Child element will all be StResources
    children: List['StResource'] = list()

    # Every streamlit-based resource will attach UI containers
    # which will be used to house the browser elements which
    # allow the user to modify the Resource value
    main_empty: DeltaGenerator = None
    main_container: DeltaGenerator = None
    sidebar_empty: DeltaGenerator = None
    sidebar_container: DeltaGenerator = None

    # If set to True, then the contents of the sidebar_ elements
    # will never be populated.
    # Additionally, all children will have .sidebar=False assigned.
    disable_sidebar = False

    # Keep track of the number of times that the UI element has been updated
    revision = 0

    # Parent element (if any)
    parent: Union['StResource', None] = None

    def __init__(
        self,
        id="resource",
        value: Union[Any, None] = None,
        children: List['StResource'] = [],
        label: Union[str, None] = None,
        help: Union[str, None] = None,
        disable_sidebar=None,
        **kwargs
    ) -> None:

        if disable_sidebar is not None:
            kwargs['disable_sidebar'] = disable_sidebar
        else:
            kwargs['disable_sidebar'] = self.__class__.disable_sidebar

        super().__init__(
            id=id,
            value=value,
            children=children,
            label=label,
            help=help,
            **kwargs
        )

    def _get_ui_element(self, sidebar=False, empty=False):
        """Return the appropriate UI element."""

        if sidebar and not self.disable_sidebar:
            if empty:
                return self.sidebar_empty
            else:
                return self.sidebar_container
        else:
            if empty:
                return self.main_empty
            else:
                return self.main_container

    def key(self):
        """Format a unique UI key based on the id and ui revision."""

        return f"{'_'.join(self._path_to_root())}_{self.revision}"

    def prep(self):
        """
        If this Resource is housed within a parent Resource / Widget,
        then self.main_container and self.sidebar_container will be created
        within the corresponding elements of the parent.
        Otherwise, if this Resource has no parent, then those
        containers will be instantiated in the top-level namespace.
        """

        # If there is a parent element assigned
        if self.parent is not None:

            # Set up the main and sidebar containers inside the parent
            # If they have not already been assigned
            if self.main_empty is None:
                if self.parent.main_container is None:
                    pid = self.parent.id
                    msg = f"Parent ({pid}) of {self.id} is not prepared"
                    raise ResourceExecutionException(msg)
                self.main_empty = self.parent.main_container.empty()

            # If the parent element has .disable_sidebar=True
            if self.parent.disable_sidebar:

                # Set the same attribute on this resource
                self.disable_sidebar = True

                # Also disable the sidebar flag on this element
                self.sidebar = False

            # If the sidebar has not been disabled
            if not self.disable_sidebar:

                if self.sidebar_empty is None:
                    self.sidebar_empty = self.parent.sidebar_container.empty()

        # If there is no parent
        else:

            # Set up the main and sidebar containers in the global namespace
            self.main_empty = st.empty()

            # Only if the sidebar has not been disabled
            if not self.disable_sidebar:
                self.sidebar_empty = st.sidebar.empty()

        # Set up a new container inside the top-level st.empty() objects
        self.reset_container()

    def reset_container(self, main=True, sidebar=True):
        """Replace the contents of the top-level st.empty() object."""

        if main:
            self.main_container = self.main_empty.container()

        if sidebar:
            if not self.disable_sidebar:
                self.sidebar_container = self.sidebar_empty.container()

    def on_change(self):
        """Function optionally called when the ui element is changed."""

        # Set the value attribute on the resource
        self.value = st.session_state[self.key()]

    def _find_child(self, id) -> Generator['StResource', None, None]:
        """Yield all nested child elements with the matching id."""
        yield from super()._find_child(id)
