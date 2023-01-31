# import streamlit as st
# from widgets.streamlit.resource_list import StResourceList
# from streamlit.delta_generator import DeltaGenerator


# class StMultiResource(StResourceList):
#     """
#     A MultiResource object is included in the list of Resources
#     used by a Widget.
#     However, it contains multiple Resource objects within it.
#     Importantly, it can be accessed and manipulated with the
#     class functions which are available on Resources:
#         - get(attr) -> returns a Resource
#         - get_value()
#         - set(attr, val)

#     The 'attributes' of a MultiResource are the component
#     Resources, identified by their .id string.
#     """

#     def update_ui(self) -> None:
#         """Set up the UI element (overridden by child classes)."""
#         pass

#     def get_value(self):
#         """Return the updated value for the widget in the session state."""

#         # If the ui has been set up
#         if self.ui is not None:

#             # Get the value from the ui
#             self.value = st.session_state[self.key()]
#             return st.session_state[self.key()]

#         # If the ui has not been set up
#         else:

#             # Use the object attribute
#             return self.value
