from typing import Any
import streamlit as st
from widgets.base.exceptions import ResourceExecutionException
from widgets.base.resource import Resource


class StResource(Resource):
    """
    Base class for Streamlit-based resources.
    Attribute values in the session state will take precedence
    over the attributes on the resource object.
    """

    def _session_obj(self) -> Any:
        """Return the object in the session state with this id, if any."""
        return st.session_state.__dict__.get(self.id)

    def _resource_in_session_state(self) -> bool:
        """True if an object exists in the session state with a matching id."""

        return self._session_obj() is not None

    def _attr_in_session_state(self, attr) -> bool:
        """True if an attribute with this id exists in the session state."""

        if self._resource_in_session_state():
            return self._session_obj().__dict__.get(attr) is not None
        else:
            return False

    def get(self, attr) -> Any:
        """Return the value of the attribute for this resource."""

        # If the attribute exists in the session state
        if self._attr_in_session_state(attr):

            # Return that value
            return self._session_obj().__dict__.get(attr)

        # Otherwise, if the value does not exist in the session state
        else:

            # Get the value from the Resource object
            val = self.__dict__.get(attr)

            # If there is no value, raise an error
            if val is None:
                msg = f"Attribute does not exist {attr} for {self.id}"
                raise ResourceExecutionException(msg)

            return val

    def set(self, attr, val) -> None:
        """Set the value of an attribute for this resource."""

        # If the attribute exists in the session state
        if self._attr_in_session_state(attr):

            # Set the value on that object
            self._session_obj().__dict__[attr] = val

        # Otherwise, if that attribute is not in the session state
        else:

            # Set it on the resource object
            self.__dict__[attr] = val
