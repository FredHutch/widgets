import streamlit as st
from streamlit.delta_generator import DeltaGenerator
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
        """Format a unique UI key based on the id and ui revision."""

        return f"{'_'.join(self._path_to_root())}_{self.ui_revision}"

    def set(self, attr, val, update=True) -> None:
        """Set the value of an attribute for this resource."""

        # Set the attribute value on the resource object
        self.__dict__[attr] = val

        if update and self.ui is not None:

            # Call the method to setup the input element
            self.update_ui()

    def set_value(self, val, update=True, **kwargs) -> None:
        """Set the value of the 'value' attribute for this resource."""

        self.set("value", val, update=update, **kwargs)

    def update_ui(self) -> None:
        """Set up the UI element (overridden by child classes)."""
        pass

    def setup_ui(self, container: DeltaGenerator):
        """
        Read in the value from the user.
        """

        # Set up the placeholder container
        self.ui = container.empty()

        # Update the element being displayed in the UI
        self.update_ui()

    def on_change(self):
        """Function optionally called when the ui element is changed."""

        # Set the value attribute on the resource
        self.value = st.session_state[self.key()]
