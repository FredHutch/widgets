from typing import Any
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from widgets.base.exceptions import ResourceExecutionException
from widgets.base.resource import Resource


class StResource(Resource):
    """
    Base class for Streamlit-based resources.
    Attribute values in the session state will take precedence
    over the attributes on the resource object.
    """

    # Every streamlit-based resource will set up a UI object
    ui: DeltaGenerator = None

    # Keep track of the number of times that the UI element has been updated
    ui_revision = 0

    def key(self):
        """Format a unique UI key based on the id and ui_revision."""
        return f"{self.id}_{self.ui_revision}"

    def get(self, attr) -> Any:
        """Return the value of the attribute for this resource."""

        # If there is no value, raise an error
        if attr not in self.__dict__:
            msg = f"Attribute does not exist {attr} for {self.id}"
            raise ResourceExecutionException(msg)

        return self.__dict__.get(attr)

    def set(self, attr, val, update=True) -> None:
        """Set the value of an attribute for this resource."""

        # Set the attribute value on the resource object
        self.__dict__[attr] = val

        if update and self.ui is not None:
            # Call the method to setup the input element
            self.update_ui()

    def update_ui(self) -> None:
        """Set up the UI element (overridden by child classes)."""
        pass

    def setup_ui(self):
        """
        Read in the integer value from the user.
        """

        # Set up the placeholder container
        with st.sidebar:
            self.ui = st.empty()

        # Update the element being displayed in the UI
        self.update_ui()

    def on_change(self):
        """Function optionally called when the ui element is changed."""

        # Set the value attribute on the resource
        self.value = st.session_state[self.key()]

    def get_value(self):
        """Return the updated value for the widget in the session state."""

        # If the ui has been set up
        if self.ui is not None:

            # Get the value from the ui
            self.value = st.session_state[self.key()]
            return st.session_state[self.key()]

        # If the ui has not been set up
        else:

            # Use the object attribute
            return self.value
